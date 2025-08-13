import requests
import json
import uuid
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class ContaboAPIError(Exception):
    """Custom exception for Contabo API errors"""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)

class ContaboAPIClient:
    """Contabo API client for VPS management"""
    
    def __init__(self):
        self.client_id = settings.CONTABO_CLIENT_ID
        self.client_secret = settings.CONTABO_CLIENT_SECRET
        self.api_user = settings.CONTABO_API_USER
        self.api_password = settings.CONTABO_API_PASSWORD
        self.auth_url = settings.CONTABO_AUTH_URL
        self.base_url = settings.CONTABO_API_BASE_URL
        self.access_token = None
        self.token_expires_at = None
        
    def _get_access_token(self) -> str:
        """Get or refresh access token"""
        # Check if token is cached and still valid
        cached_token = cache.get('contabo_access_token')
        if cached_token:
            return cached_token
            
        try:
            # Request new token
            auth_data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'username': self.api_user,
                'password': self.api_password,
                'grant_type': 'password'
            }
            
            response = requests.post(self.auth_url, data=auth_data, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            access_token = token_data.get('access_token')
            expires_in = token_data.get('expires_in', 3600)
            
            if not access_token:
                raise ContaboAPIError("Failed to obtain access token")
            
            # Cache token for 90% of its lifetime
            cache_timeout = int(expires_in * 0.9)
            cache.set('contabo_access_token', access_token, cache_timeout)
            
            logger.info("Successfully obtained Contabo access token")
            return access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get Contabo access token: {e}")
            raise ContaboAPIError(f"Authentication failed: {e}")
    
    def _make_request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        """Make authenticated API request"""
        access_token = self._get_access_token()
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'x-request-id': str(uuid.uuid4()),
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=60)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, params=params, timeout=60)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data, params=params, timeout=60)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, headers=headers, json=data, params=params, timeout=60)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, params=params, timeout=60)
            else:
                raise ContaboAPIError(f"Unsupported HTTP method: {method}")
            
            # Log the request
            logger.info(f"Contabo API {method} {endpoint} - Status: {response.status_code}")
            
            if response.status_code == 401:
                # Token might be expired, clear cache and retry once
                cache.delete('contabo_access_token')
                access_token = self._get_access_token()
                headers['Authorization'] = f'Bearer {access_token}'
                
                if method.upper() == 'GET':
                    response = requests.get(url, headers=headers, params=params, timeout=60)
                elif method.upper() == 'POST':
                    response = requests.post(url, headers=headers, json=data, params=params, timeout=60)
                # ... (repeat for other methods if needed)
            
            if not response.ok:
                error_data = {}
                try:
                    error_data = response.json()
                except:
                    pass
                
                error_message = error_data.get('message', f"HTTP {response.status_code}")
                logger.error(f"Contabo API error: {error_message}")
                raise ContaboAPIError(error_message, response.status_code, error_data)
            
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Contabo API request failed: {e}")
            raise ContaboAPIError(f"Request failed: {e}")
    
    # VPS Instance Management Methods
    
    def get_instances(self, page: int = 1, size: int = 25) -> dict:
        """Get list of VPS instances"""
        params = {'page': page, 'size': size}
        return self._make_request('GET', '/compute/instances', params=params)
    
    def get_instance(self, instance_id: str) -> dict:
        """Get specific VPS instance details"""
        return self._make_request('GET', f'/compute/instances/{instance_id}')
    
    def create_instance(self, instance_data: dict) -> dict:
        """Create a new VPS instance"""
        return self._make_request('POST', '/compute/instances', data=instance_data)
    
    def start_instance(self, instance_id: str) -> dict:
        """Start a VPS instance"""
        return self._make_request('POST', f'/compute/instances/{instance_id}/start')
    
    def stop_instance(self, instance_id: str) -> dict:
        """Stop a VPS instance"""
        return self._make_request('POST', f'/compute/instances/{instance_id}/stop')
    
    def restart_instance(self, instance_id: str) -> dict:
        """Restart a VPS instance"""
        return self._make_request('POST', f'/compute/instances/{instance_id}/restart')
    
    def delete_instance(self, instance_id: str) -> dict:
        """Delete a VPS instance"""
        return self._make_request('DELETE', f'/compute/instances/{instance_id}')
    
    def rebuild_instance(self, instance_id: str, image_id: str, ssh_keys: List[str] = None) -> dict:
        """Rebuild a VPS instance with new image"""
        data = {'imageId': image_id}
        if ssh_keys:
            data['sshKeys'] = ssh_keys
        return self._make_request('POST', f'/compute/instances/{instance_id}/rebuild', data=data)
    
    def resize_instance(self, instance_id: str, product_id: str) -> dict:
        """Resize a VPS instance"""
        data = {'productId': product_id}
        return self._make_request('POST', f'/compute/instances/{instance_id}/resize', data=data)
    
    # Image Management Methods
    
    def get_images(self, page: int = 1, size: int = 25) -> dict:
        """Get available images"""
        params = {'page': page, 'size': size}
        return self._make_request('GET', '/compute/images', params=params)
    
    def get_image(self, image_id: str) -> dict:
        """Get specific image details"""
        return self._make_request('GET', f'/compute/images/{image_id}')
    
    # Product/Package Management Methods
    
    def get_products(self) -> dict:
        """Get available VPS products/packages"""
        return self._make_request('GET', '/compute/products')
    
    def get_product(self, product_id: str) -> dict:
        """Get specific product details"""
        return self._make_request('GET', f'/compute/products/{product_id}')
    
    # SSH Key Management Methods
    
    def get_ssh_keys(self, page: int = 1, size: int = 25) -> dict:
        """Get SSH keys"""
        params = {'page': page, 'size': size}
        return self._make_request('GET', '/compute/ssh-keys', params=params)
    
    def create_ssh_key(self, name: str, public_key: str) -> dict:
        """Create SSH key"""
        data = {'name': name, 'publicKey': public_key}
        return self._make_request('POST', '/compute/ssh-keys', data=data)
    
    def delete_ssh_key(self, ssh_key_id: str) -> dict:
        """Delete SSH key"""
        return self._make_request('DELETE', f'/compute/ssh-keys/{ssh_key_id}')
    
    # Secret/Password Management Methods
    
    def get_secrets(self, page: int = 1, size: int = 25) -> dict:
        """Get secrets (passwords)"""
        params = {'page': page, 'size': size}
        return self._make_request('GET', '/secrets', params=params)
    
    def create_secret(self, name: str, value: str, secret_type: str = 'password') -> dict:
        """Create a secret (password)"""
        data = {'name': name, 'value': value, 'type': secret_type}
        return self._make_request('POST', '/secrets', data=data)
    
    def get_secret(self, secret_id: str) -> dict:
        """Get specific secret"""
        return self._make_request('GET', f'/secrets/{secret_id}')
    
    def delete_secret(self, secret_id: str) -> dict:
        """Delete a secret"""
        return self._make_request('DELETE', f'/secrets/{secret_id}')
    
    # Snapshot/Backup Methods
    
    def get_snapshots(self, instance_id: str) -> dict:
        """Get snapshots for an instance"""
        return self._make_request('GET', f'/compute/instances/{instance_id}/snapshots')
    
    def create_snapshot(self, instance_id: str, name: str, description: str = '') -> dict:
        """Create a snapshot"""
        data = {'name': name, 'description': description}
        return self._make_request('POST', f'/compute/instances/{instance_id}/snapshots', data=data)
    
    def restore_snapshot(self, instance_id: str, snapshot_id: str) -> dict:
        """Restore from snapshot"""
        data = {'snapshotId': snapshot_id}
        return self._make_request('POST', f'/compute/instances/{instance_id}/snapshots/{snapshot_id}/restore', data=data)
    
    def delete_snapshot(self, instance_id: str, snapshot_id: str) -> dict:
        """Delete a snapshot"""
        return self._make_request('DELETE', f'/compute/instances/{instance_id}/snapshots/{snapshot_id}')
    
    # Monitoring and Stats Methods
    
    def get_instance_stats(self, instance_id: str, period: str = '1h') -> dict:
        """Get instance statistics"""
        params = {'period': period}
        return self._make_request('GET', f'/compute/instances/{instance_id}/stats', params=params)
    
    # Data Center and Region Methods
    
    def get_data_centers(self) -> dict:
        """Get available data centers"""
        return self._make_request('GET', '/compute/data-centers')
    
    # Helper Methods for VPS Creation
    
    def prepare_instance_creation_data(self, package_data: dict, user_config: dict) -> dict:
        """Prepare data for VPS instance creation"""
        creation_data = {
            'imageId': package_data.get('contabo_image_id'),
            'productId': package_data.get('contabo_product_id'),
            'region': user_config.get('region', 'EU'),
            'period': user_config.get('period', 1),
            'displayName': user_config.get('hostname'),
            'defaultUser': 'root'
        }
        
        # Add SSH keys if provided
        if user_config.get('ssh_keys'):
            creation_data['sshKeys'] = user_config['ssh_keys']
        
        # Add password if provided
        if user_config.get('root_password'):
            # Create secret for password
            secret_name = f"password-{user_config['hostname']}-{uuid.uuid4().hex[:8]}"
            secret_response = self.create_secret(secret_name, user_config['root_password'])
            if secret_response.get('secretId'):
                creation_data['rootPassword'] = secret_response['secretId']
        
        return creation_data
    
    def get_instance_status(self, instance_id: str) -> str:
        """Get simplified instance status"""
        try:
            instance_data = self.get_instance(instance_id)
            status = instance_data.get('status', 'unknown').lower()
            
            # Map Contabo statuses to our internal statuses
            status_mapping = {
                'running': 'active',
                'stopped': 'stopped',
                'installing': 'creating',
                'error': 'error',
                'suspended': 'suspended'
            }
            
            return status_mapping.get(status, status)
            
        except ContaboAPIError as e:
            logger.error(f"Failed to get instance status for {instance_id}: {e}")
            return 'error'

# Singleton instance
contabo_client = ContaboAPIClient()
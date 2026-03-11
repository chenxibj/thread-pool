#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RSA Utility Module

SECURITY NOTICE:
- Never commit private keys to version control
- Store private keys in secure secret management systems
- Use environment variables or vault services for key storage

Usage:
    Set RSA_PRIVATE_KEY environment variable with your private key content.
    Or use a secret management service (AWS Secrets Manager, HashiCorp Vault, etc.)
"""

import os
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def get_private_key():
    """
    Load RSA private key from environment variable.
    
    Returns:
        Private key object or None if not configured
        
    Raises:
        ValueError: If key format is invalid
    """
    key_data = os.environ.get('RSA_PRIVATE_KEY')
    
    if not key_data:
        # Return None instead of raising error to allow graceful degradation
        # In production, you should handle this appropriately
        return None
    
    try:
        # Try to decode if it's base64 encoded
        try:
            decoded_key = base64.b64decode(key_data)
            private_key = serialization.load_pem_private_key(
                decoded_key,
                password=None,
                backend=default_backend()
            )
        except Exception:
            # Try loading as plain PEM
            private_key = serialization.load_pem_private_key(
                key_data.encode('utf-8'),
                password=None,
                backend=default_backend()
            )
        return private_key
    except Exception as e:
        raise ValueError(f"Invalid RSA private key format: {str(e)}")


def get_public_key(private_key):
    """
    Extract public key from private key.
    
    Args:
        private_key: RSA private key object
        
    Returns:
        Public key bytes in PEM format
    """
    if private_key is None:
        return None
    
    public_key = private_key.public_key()
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


# Example usage:
# if __name__ == "__main__":
#     private_key = get_private_key()
#     if private_key:
#         public_key_pem = get_public_key(private_key)
#         print(public_key_pem.decode('utf-8'))
#     else:
#         print("RSA_PRIVATE_KEY environment variable not set")

import os
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.exceptions import ValidationError
import magic

def get_encryption_key():
    key = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)
    if not key:
        # Fallback to a key derived from SECRET_KEY if not provided
        # In production, this should be set in environment variables
        import base64
        from django.utils.encoding import force_bytes
        key = base64.urlsafe_b64encode(force_bytes(settings.SECRET_KEY[:32]))
    return key

def encrypt_data(data):
    if not data:
        return data
    f = Fernet(get_encryption_key())
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    if not encrypted_data:
        return encrypted_data
    try:
        f = Fernet(get_encryption_key())
        return f.decrypt(encrypted_data.encode()).decode()
    except Exception:
        return "[Decryption Error]"

def validate_image_file(file):
    # Check file size (max 5MB)
    filesize = file.size
    if filesize > 5 * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")

    # Check file extension
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

    # Deep check MIME type using magic numbers
    # We read the first 2048 bytes to determine the type
    file_content = file.read(2048)
    file.seek(0)
    mime = magic.from_buffer(file_content, mime=True)
    
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if mime not in valid_mime_types:
        raise ValidationError(f'Malicious file detected or invalid image format (%s)' % mime)

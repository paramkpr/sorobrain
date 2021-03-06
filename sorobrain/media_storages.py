from storages.backends.s3boto3 import S3Boto3Storage

from sorobrain import settings


class PublicMediaStorage(S3Boto3Storage):
    location = 'media/public'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    default_acl = 'private'
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = False

import os
import uuid
import boto3
from django.core.files.storage import Storage
from django.core.files.base import ContentFile



import os

from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')


def get_user_id(self):
    return self.user_id

class S3Storage(Storage):
    def __init__(self, user_id=None, *args, **kwargs):
        super().__init__()
        self.user_id = user_id
        self.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.aws_storage_bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        self.aws_s3_endpoint_url = os.environ.get( 'https://storage.yandexcloud.net')

    def _open(self, name, mode='rb'):
        with self._get_s3_client() as s3:
            response = s3.get_object(Bucket=self.aws_storage_bucket_name, Key=name)
            return ContentFile(response['Body'].read())

    def _save(self, name, content):
        user_id = self.get_user_id()
        if user_id is None:
            raise Exception("Невозможно определить ID пользователя.")
        unique_filename = f"{user_id}/{uuid.uuid4()}{os.path.basename(name)}"
        with self._get_s3_client() as s3:
            s3.upload_fileobj(content, self.aws_storage_bucket_name, unique_filename, ExtraArgs={'ACL': 'public-read'})
        return unique_filename

    def delete(self, name):
        with self._get_s3_client() as s3:
            s3.delete_object(Bucket=self.aws_storage_bucket_name, Key=name)

    def exists(self, name):
        with self._get_s3_client() as s3:
            try:
                s3.head_object(Bucket=self.aws_storage_bucket_name, Key=name)
                return True
            except s3.exceptions.NoSuchKey:
                return False
            except Exception as e:
                print(f"Ошибка проверки существования файла на S3: {e}")
                return False

    def url(self, name):
        with self._get_s3_client() as s3:
            return s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': self.aws_storage_bucket_name, 'Key': name},
                ExpiresIn=3600,
            )

    def _get_s3_client(self):
        return boto3.client(
            service_name='s3',
            endpoint_url=self.aws_s3_endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )


    def get_user_id(self):
        try:
            return self.request.user.id
        except AttributeError:
            return None


import boto3.session

class s3_client:
    def __init__(_self, _endpoint: str, _access_key: str, _secret_key: str) -> None:
        s3Session = boto3.session.Session()
        _self.client = s3Session.client(
            service_name = 's3',
            endpoint_url = _endpoint,
            aws_access_key_id = _access_key,
            aws_secret_access_key = _secret_key,
        )

    def upload(_self, _bucketName: str, _filePath: str, _remotePath: str) -> None:
        _self.client.upload_file(_filePath, _bucketName, _remotePath)
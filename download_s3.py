import boto3
import os

from cognito_auth import *

if __name__ == "__main__":

    # Auth anonymously
    creds = get_temp_credentials_anonymous(os.environ['AWS_ACCOUNT_ID'], os.environ['COGNITO_IDENTITY_POOL_ID'])

    s3 = boto3.resource('s3',
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretKey'],
        aws_session_token=creds['SessionToken']
    )

    bucket = s3.Bucket(os.environ['S3_BUCKET'])
    bucket.download_file("hello.txt", "./hello.txt")

    # Auth using User Pool
    id_token = cognito_idp_auth(os.environ['USERNAME'], os.environ['PASSWORD'], os.environ['COGNITO_USER_POOL_ID'])

    creds = get_temp_credentials(
        os.environ['AWS_ACCOUNT_ID'], 
        os.environ['COGNITO_IDENTITY_POOL_ID'], 
        os.environ['COGNITO_IDENTITY_POOL_LONG_ID'], 
        id_token 
    )

    s3 = boto3.resource('s3',
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretKey'],
        aws_session_token=creds['SessionToken']
    )

    bucket = s3.Bucket(os.environ['S3_BUCKET'])
    bucket.download_file("hello.txt", "./hello.txt")
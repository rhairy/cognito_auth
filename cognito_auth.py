import boto3
import os

def cognito_idp_auth(username: str, password: str, cognito_user_pool_id: str):
    client = boto3.client("cognito-idp")

    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        },
        ClientId=cognito_user_pool_id
    )

    id_token = response['AuthenticationResult']['IdToken']

    return id_token

def get_temp_credentials(aws_account_id: str, cognito_identity_pool_id: str, cognito_identity_pool_long_id: str, id_token: str):
    client = boto3.client('cognito-identity')
        
    response = client.get_id(
        AccountId=aws_account_id,
        IdentityPoolId=cognito_identity_pool_id,
        Logins={
            cognito_identity_pool_long_id: id_token
        }
    )

    identity_id = response['IdentityId']

    response = client.get_credentials_for_identity(
        IdentityId = identity_id,
        Logins={
            cognito_identity_pool_long_id: id_token
        }
    )

    creds = response['Credentials']

    return creds

def get_temp_credentials_anonymous(account_id: str, identity_pool_id: str) -> dict:
    client = boto3.client('cognito-identity')
        
    response = client.get_id(
        AccountId=account_id,
        IdentityPoolId=identity_pool_id
    )

    identity_id = response['IdentityId']

    response = client.get_credentials_for_identity(
        IdentityId = identity_id
    )

    credentials = response['Credentials']

    return credentials
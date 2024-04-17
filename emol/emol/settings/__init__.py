import boto3

def get_parameter(key, ssm_client):
    """Get a parameter from AWS SSM Parameter Store
    
    Args:
        key (str): The name of the parameter to get
        ssm_client (boto3.client): An SSM client
    Returns:
        str: The value of the parameter
    Raises:
        botocore.exceptions.ClientError: If the parameter does not exist
    """
    response = ssm_client.get_parameter(Name=key, WithDecryption=True)
    return response["Parameter"]["Value"]

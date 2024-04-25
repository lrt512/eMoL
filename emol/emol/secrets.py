import boto3

ssm = boto3.client("ssm", region_name="your-aws-region")


def get_secret(parameter_name):
    """Retrieve secret from AWS Parameter Store"""
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response["Parameter"]["Value"]

import json

import boto3

def get_secret(parameter_name):
    try:
        with open("/usr/local/etc/emol_credentials.json", "r") as f:
            credentials = json.load(f)

        session = boto3.Session(**credentials)
        ssm = session.client("ssm")

        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response["Parameter"]["Value"]
    except ssm.exceptions.ParameterNotFound as exc:
        print(f"Parameter {parameter_name} not found: {exc}")
        return None
    except Exception as e:
        print(f"Error retrieving parameter {parameter_name}: {str(e)}")
        return None
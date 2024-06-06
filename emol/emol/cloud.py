from functools import lru_cache
import logging
import os

import boto3

logger = logging.getLogger(__name__)

@lru_cache(maxsize=32)
def get_secret(name):
    ssm_kwargs = {}
    if os.environ.get("SSM_ENDPOINT_URL"):
        ssm_kwargs["endpoint_url"] = os.environ.get("SSM_ENDPOINT_URL")
    
    ssm = boto3.client("ssm", **ssm_kwargs)    

    try:
        response = ssm.get_parameter(Name=name, WithDecryption=True)
        return response["Parameter"]["Value"]
    except ssm.exceptions.ParameterNotFound as exc:
        logger.error(f"Parameter '{name}' not found: {exc}")
        return None
    except Exception as e:
        logger.error(f"Error retrieving parameter '{name}': {str(e)}")
        return None
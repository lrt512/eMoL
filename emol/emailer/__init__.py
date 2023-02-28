# -*- coding: utf-8 -*-

import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings

logger = logging.getLogger(__name__)


class Emailer:
    """A simple emailing facility

    SES configuration in settings.py:
        AWS_REGION = your AWS region
        MAIL_DEFAULT_SENDER = 'eMoL <emol@example.com>'

    """

    CHARSET = "UTF-8"

    @classmethod
    def send_email(cls, recipient, subject, body):
        """Send an email.

        Args:
            recipient: Recipient's email address
            subject: The email's subject
            body: Email message text

        Returns:
            True if the message was delivered

        """
        if settings.SEND_EMAIL is False:
            logger.debug(f"Not sending email to {recipient}")
            logger.debug(subject)
            logger.debug(body)
            return True

        sender = settings.MAIL_DEFAULT_SENDER
        aws_region = settings.AWS_REGION

        client = boto3.client("ses", region_name=aws_region)
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    "ToAddresses": [
                        recipient,
                    ],
                },
                Message={
                    "Body": {
                        "Text": {"Charset": cls.CHARSET, "Data": body},
                    },
                    "Subject": {
                        "Charset": cls.CHARSET,
                        "Data": subject,
                    },
                },
                Source=sender,
                # If you are not using a configuration set, comment or delete the
                # following line
                # ConfigurationSetName=CONFIGURATION_SET,
            )
        except ClientError as exc:
            logger.error(f"Error sending mail to {recipient}")
            logger.exception(exc)
        else:
            logger.debug(
                f"Email {subject} sent to {recipient}.  Message ID: {response['MessageId']}"
            )
            return True

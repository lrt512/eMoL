# -*- coding: utf-8 -*-

import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings

logger = logging.getLogger("cards")


class AWSEmailer:
    """A simple emailing facility that uses AWS SES

    SES configuration in settings.py:
        AWS_REGION = your AWS region
        MAIL_DEFAULT_SENDER = 'eMoL <emol@example.com>'

    """

    CHARSET = "UTF-8"

    @classmethod
    def send_email(cls, recipient, subject, body):
        """Send an email

        Args:
            recipient: Recipient's email address
            subject: The email's subject
            body: Email message text

        Returns:
            True if the message was delivered

        """
        if settings.SEND_EMAIL is False:
            logger.info("Not sending email to %s", recipient)
            logger.info(subject)
            logger.info(body)
            return True
        else:
            logger.info("Sending email to %s: %s", recipient, subject)

        sender = f"Ealdormere eMoL <{settings.MAIL_DEFAULT_SENDER}>"
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

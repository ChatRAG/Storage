import json
import boto3
import mimetypes
import logging
import os
import base64
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the S3 client
s3 = boto3.client('s3')


def handler(event, context):
    # Get the bucket name and file key from the event
    bucket_name = os.environ['BUCKET_NAME']
    file_data = event['FileData']  # assuming it's base64 encoded
    file_name = event['FileName']
    file_key = f'uploads/{file_name}'

    try:
        logger.debug(f"Checking if {file_key} exists in bucket: {bucket_name}")

        # Pre-check: does the file already exist?
        try:
            s3.head_object(Bucket=bucket_name, Key=file_key)
            # If no exception, the file exists
            return {
                'statusCode': 409,  # Conflict
                'body': json.dumps({
                    'error': f"File {file_name} already exists.",
                    'key': file_key
                })
            }
        except ClientError as e:
            if e.response['ResponseMetadata']['HTTPStatusCode'] != 404:
                raise  # Raise other errors (e.g. permission denied)

        logger.debug(f"Uploading {file_name} to bucket: {bucket_name}")

        # Decode the file data from base64
        file_content = base64.b64decode(file_data['base64_data'])

        # Upload the file to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=file_content,
            ContentType=mimetypes.guess_type(file_name)[0] or 'application/octet-stream'
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'key': file_key,
                'message': f"File {file_name} uploaded successfully.",
            })
        }
    except Exception as e:
        logger.error(f"Error uploading document {file_name} to bucket {bucket_name}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

import json
import boto3
import mimetypes
import logging
import os
import base64

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

    try:
        logger.debug(f"Uploading {file_name} to bucket: {bucket_name}")

        # Decode the file data from base64 if necessary
        file_content = base64.b64decode(file_data['base64_data'])
        file_key = f'uploads/{file_name}'

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
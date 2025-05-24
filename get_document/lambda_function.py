import boto3
import json
import logging
import os

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the S3 client
s3 = boto3.client('s3')

def handler(event, context):
    # Get the bucket name and file key from the event
    bucket_name = os.environ['BUCKET_NAME']
    file_key = event['FileKey']

    try:
        logger.debug(f"Checking if file exists: s3://{bucket_name}/{file_key}")

        # Check if the object exists
        s3.head_object(Bucket=bucket_name, Key=file_key)

        logger.debug(f"Retrieving URL for file: s3://{bucket_name}/{file_key}")

        # Generate a pre-signed URL to access the file
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': file_key},
            ExpiresIn=3600  # URL will be valid for 1 hour
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'file_url': url})
        }

    except s3.exceptions.ClientError as e:
        # If the object does not exist, a ClientError will be raised
        logger.error(f"Error retrieving document {file_key} from bucket {bucket_name}: {str(e)}")
        return {
            'statusCode': 404,
            'body': json.dumps({'error': f"File not found: {file_key}"})
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

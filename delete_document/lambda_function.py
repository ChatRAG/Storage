import json
import boto3
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
        logger.info(f"Deleting document: s3://{bucket_name}/{file_key}")

        # Delete the file from S3
        s3.delete_object(Bucket=bucket_name, Key=file_key)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f"File {file_key} deleted successfully."})
        }
    except Exception as e:
        logger.error(f"Error deleting document {file_key} from bucket {bucket_name}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

# Initialize S3 client with credentials from .env
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

s3_resource = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)


def list_buckets():
    """List all S3 buckets"""
    try:
        response = s3_client.list_buckets()
        print("\n=== Available S3 Buckets ===")
        for bucket in response['Buckets']:
            print(f"  - {bucket['Name']} (Created: {bucket['CreationDate']})")
        return response['Buckets']
    except ClientError as e:
        print(f"Error listing buckets: {e}")
        return []


def create_bucket(bucket_name, region='us-east-1'):
    """Create a new S3 bucket"""
    try:
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"\nBucket '{bucket_name}' created successfully!")
        return True
    except ClientError as e:
        print(f"Error creating bucket: {e}")
        return False


def upload_file(file_path, bucket_name, object_name=None):
    """Upload a file to S3 bucket"""
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"\nFile '{file_path}' uploaded to '{bucket_name}/{object_name}' successfully!")
        return True
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return False
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return False


def download_file(bucket_name, object_name, file_path):
    """Download a file from S3 bucket"""
    try:
        s3_client.download_file(bucket_name, object_name, file_path)
        print(f"\nFile '{object_name}' downloaded from '{bucket_name}' to '{file_path}' successfully!")
        return True
    except ClientError as e:
        print(f"Error downloading file: {e}")
        return False


def list_bucket_objects(bucket_name):
    """List all objects in an S3 bucket"""
    try:
        # First verify the bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        if 'Contents' not in response:
            print(f"\nBucket '{bucket_name}' is empty")
            return []
        
        print(f"\n=== Objects in bucket '{bucket_name}' ===")
        for obj in response['Contents']:
            print(f"  - {obj['Key']} (Size: {obj['Size']} bytes, Last Modified: {obj['LastModified']})")
        return response['Contents']
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404' or error_code == 'NoSuchBucket':
            print(f"\n❌ Error: Bucket '{bucket_name}' does not exist!")
            print("Please check the bucket name or create it first.")
        else:
            print(f"Error listing objects: {e}")
        return []


def list_folder_objects(bucket_name, folder_prefix):
    """List all objects in a specific folder/prefix in S3 bucket"""
    try:
        # Ensure folder_prefix ends with / if not empty
        if folder_prefix and not folder_prefix.endswith('/'):
            folder_prefix += '/'
        
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
        
        if 'Contents' not in response:
            print(f"\nNo objects found in folder '{folder_prefix}'")
            return []
        
        print(f"\n=== Objects in folder '{folder_prefix}' ===")
        for obj in response['Contents']:
            # Skip the folder itself (if it's listed as an object)
            if obj['Key'] == folder_prefix:
                continue
            print(f"  - {obj['Key']} (Size: {obj['Size']} bytes, Last Modified: {obj['LastModified']})")
        
        count = len(response['Contents']) - (1 if folder_prefix in [obj['Key'] for obj in response['Contents']] else 0)
        print(f"\nTotal: {count} objects")
        return response['Contents']
    except ClientError as e:
        print(f"Error listing folder objects: {e}")
        return []


def delete_object(bucket_name, object_name):
    """Delete an object from S3 bucket"""
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        print(f"\nObject '{object_name}' deleted from '{bucket_name}' successfully!")
        return True
    except ClientError as e:
        print(f"Error deleting object: {e}")
        return False


def delete_bucket(bucket_name):
    """Delete an S3 bucket (must be empty)"""
    try:
        # First, delete all objects in the bucket
        bucket = s3_resource.Bucket(bucket_name)
        bucket.objects.all().delete()
        
        # Then delete the bucket
        bucket.delete()
        print(f"\nBucket '{bucket_name}' deleted successfully!")
        return True
    except ClientError as e:
        print(f"Error deleting bucket: {e}")
        return False


def upload_directory(directory_path, bucket_name, s3_prefix=''):
    """Upload an entire directory to S3 bucket"""
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, directory_path)
                s3_path = os.path.join(s3_prefix, relative_path).replace('\\', '/')
                
                print(f"Uploading {local_path} to {bucket_name}/{s3_path}")
                s3_client.upload_file(local_path, bucket_name, s3_path)
        
        print(f"\nDirectory '{directory_path}' uploaded to '{bucket_name}' successfully!")
        return True
    except ClientError as e:
        
        print(f"Error uploading directory: {e}")
        return False


def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL for an S3 object"""
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
        print(f"\nPresigned URL for '{object_name}':")
        print(url)
        return url
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None


def copy_object(source_bucket, source_key, dest_bucket, dest_key):
    """Copy an object from one location to another in S3"""
    try:
        copy_source = {'Bucket': source_bucket, 'Key': source_key}
        s3_client.copy_object(CopySource=copy_source, Bucket=dest_bucket, Key=dest_key)
        print(f"\nObject copied from '{source_bucket}/{source_key}' to '{dest_bucket}/{dest_key}' successfully!")
        return True
    except ClientError as e:
        print(f"Error copying object: {e}")
        return False


def main():
    """Main function demonstrating S3 operations"""
    print("=" * 50)
    print("AWS S3 Operations Demo")
    print("=" * 50)
    
    # First, show available buckets
    print("\nFetching your available buckets...")
    buckets = list_buckets()
    
    # Get bucket name from environment or ask user
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    if not BUCKET_NAME:
        BUCKET_NAME = input("\nEnter your S3 bucket name (copy from the list above): ").strip()
    else:
        print(f"\nUsing bucket from .env: {BUCKET_NAME}")
        change = input("Press Enter to continue or type a different bucket name: ").strip()
        if change:
            BUCKET_NAME = change
    
    # Verify bucket exists
    bucket_exists = False
    for bucket in buckets:
        if bucket['Name'] == BUCKET_NAME:
            bucket_exists = True
            break
    
    if not bucket_exists and buckets:
        print(f"\n⚠️  Warning: '{BUCKET_NAME}' was not found in your bucket list!")
        print("Make sure you typed it correctly (bucket names are case-sensitive).")
    
    while True:
        print("\n" + "=" * 50)
        print("Choose an operation:")
        print("1. List all buckets")
        print("2. List all objects in bucket")
        print("3. List objects in a specific folder")
        print("4. Upload a file")
        print("5. Download a file")
        print("6. Delete an object")
        print("7. Upload a directory")
        print("8. Generate presigned URL")
        print("9. Copy an object")
        print("10. Create a new bucket")
        print("11. Delete a bucket")
        print("0. Exit")
        print("=" * 50)
        
        choice = input("\nEnter your choice (0-11): ").strip()
        
        if choice == '1':
            list_buckets()
        
        elif choice == '2':
            list_bucket_objects(BUCKET_NAME)
        
        elif choice == '3':
            folder_path = input("Enter the folder path (e.g., courses/CS101/weeks/): ").strip()
            list_folder_objects(BUCKET_NAME, folder_path)
        
        elif choice == '4':
            file_path = input("Enter the local file path to upload: ").strip()
            object_name = input("Enter the object name in S3 (press Enter to use filename): ").strip()
            object_name = object_name if object_name else None
            upload_file(file_path, BUCKET_NAME, object_name)
        
        elif choice == '5':
            object_name = input("Enter the object name to download: ").strip()
            file_path = input("Enter the local file path to save: ").strip()
            download_file(BUCKET_NAME, object_name, file_path)
        
        elif choice == '6':
            object_name = input("Enter the object name to delete: ").strip()
            confirm = input(f"Are you sure you want to delete '{object_name}'? (yes/no): ").strip().lower()
            if confirm == 'yes':
                delete_object(BUCKET_NAME, object_name)
        
        elif choice == '7':
            directory_path = input("Enter the directory path to upload: ").strip()
            s3_prefix = input("Enter S3 prefix (folder path, press Enter for root): ").strip()
            upload_directory(directory_path, BUCKET_NAME, s3_prefix)
        
        elif choice == '8':
            object_name = input("Enter the object name: ").strip()
            expiration = input("Enter expiration time in seconds (default 3600): ").strip()
            expiration = int(expiration) if expiration else 3600
            generate_presigned_url(BUCKET_NAME, object_name, expiration)
        
        elif choice == '9':
            source_key = input("Enter the source object key: ").strip()
            dest_key = input("Enter the destination object key: ").strip()
            copy_object(BUCKET_NAME, source_key, BUCKET_NAME, dest_key)
        
        elif choice == '10':
            new_bucket_name = input("Enter new bucket name: ").strip()
            region = input("Enter region (default us-east-2): ").strip()
            region = region if region else 'us-east-2'
            create_bucket(new_bucket_name, region)
        
        elif choice == '11':
            bucket_to_delete = input("Enter bucket name to delete: ").strip()
            confirm = input(f"Are you sure you want to delete '{bucket_to_delete}' and all its contents? (yes/no): ").strip().lower()
            if confirm == 'yes':
                delete_bucket(bucket_to_delete)
        
        elif choice == '0':
            print("\nExiting... Goodbye!")
            break
        
        else:
            print("\nInvalid choice! Please try again.")


if __name__ == "__main__":
    main()

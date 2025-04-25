from google.cloud import storage

# Replace these with your actual bucket name and file paths
bucket_name = 'your-bucket-name'
file_path = 'path/to/local/file.txt'
destination_blob_name = 'uploaded-file.txt'  # Destination file in GCS
source_blob_name = 'uploaded-file.txt'  # File to download from GCS
download_file_name = 'downloaded-file.txt'  # Local destination for downloaded file

# Function to upload a file to Google Cloud Storage
def upload_file_to_gcs(bucket_name, file_path, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(file_path)
    print(f"File {file_path} uploaded to {destination_blob_name}.")

# Function to download a file from Google Cloud Storage
def download_file_from_gcs(bucket_name, source_blob_name, download_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    # Download the file
    blob.download_to_filename(download_file_name)
    print(f"Downloaded {source_blob_name} to {download_file_name}.")

# Call the functions (you can comment/uncomment based on need)
upload_file_to_gcs(bucket_name, file_path, destination_blob_name)
# download_file_from_gcs(bucket_name, source_blob_name, download_file_name)  # Uncomment this line to test downloading

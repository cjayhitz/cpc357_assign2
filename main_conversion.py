import os
import json
import csv
from google.cloud import storage

def json_to_csv(bucket_name, json_file, csv_file):
    """Convert JSON file in GCS to CSV file."""
    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(json_file)

    # Download JSON content
    json_content = blob.download_as_text()
    json_data = [json.loads(line) for line in json_content.splitlines()]

    # Define CSV header based on JSON structure
    csv_header = ["_id", "timestamp", "topic", "data"]

    # Create CSV file locally
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        writer.writeheader()

        for item in json_data:
            # Flatten _id field to extract $oid
            csv_row = {
                "_id": item["_id"]["$oid"],
                "timestamp": item["timestamp"],
                "topic": item.get("topic", ""),  # Default to empty string if topic is missing
                "data": item["data"],
            }
            writer.writerow(csv_row)

    print(f"Converted JSON to CSV: {csv_file}")

def upload_csv_to_gcs(bucket_name, csv_file, destination_blob_name):
    """Upload the CSV file to GCS."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(csv_file)
    print(f"Uploaded CSV to GCS: {destination_blob_name}")

def main(request):
    """Cloud Run entry point."""
    request_json = request.get_json()
    bucket_name = request_json.get("bucket_name")
    json_file = request_json.get("json_file")
    csv_file = "/tmp/output.csv"  # Temporary local file
    destination_blob_name = request_json.get("csv_file")

    if not bucket_name or not json_file or not destination_blob_name:
        return "Error: 'bucket_name', 'json_file', and 'csv_file' must be provided.", 400

    # Convert JSON to CSV
    json_to_csv(bucket_name, json_file, csv_file)

    # Upload CSV back to GCS
    upload_csv_to_gcs(bucket_name, csv_file, destination_blob_name)

    return "JSON converted to CSV and uploaded successfully.", 200

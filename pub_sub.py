#MQTT Pub-Sub

import paho.mqtt.client as mqtt
import pandas as pd
import io
from google.cloud import storage
from google.cloud import pubsub_v1
import json

# GCP Configuration
project_id = "cpc357assign2"
bucket_name = "dummy-sensor-data"
topic_id = "sensor-data"

# MQTT Configuration
broker = "mqtt.eclipseprojects.io" #testing
port = 1883
mqtt_topic = "demo/iot"

# Initialize GCP clients
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# List all CSV files in the bucket
def list_csv_files(bucket_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        return [blob.name for blob in bucket.list_blobs() if blob.name.endswith(".csv")]
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

# Read a CSV file from Cloud Storage
def read_csv_from_bucket(bucket_name, file_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data = blob.download_as_text()
        return pd.read_csv(io.StringIO(data))
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

# Publish CSV data to MQTT
def publish_data_to_mqtt(client, data, sensor_name):
    for index, row in data.iterrows():
        message = row.to_dict()
        message["sensor"] = sensor_name  # Add sensor identifier
        json_message = json.dumps(message)

        # Publish to MQTT
        client.publish(mqtt_topic, json_message)
        print(f"Published MQTT message: {json_message}")

        # Forward to Pub/Sub
        publisher.publish(topic_path, json_message.encode())
        print(f"Published message to Pub/Sub: {json_message}")

# Main function
if __name__ == "__main__":
    # List CSV files in the bucket
    print("Listing CSV files in the bucket...")
    csv_files = list_csv_files(bucket_name)

    if csv_files:
        print(f"Found CSV files: {csv_files}")

        # Setup MQTT client
        client = mqtt.Client()
        client.on_connect = on_connect

        try:
            # Connect to MQTT broker
            client.connect(broker, port, 60)

            # Process each CSV file
            for file_name in csv_files:
                print(f"Processing file: {file_name}")
                csv_data = read_csv_from_bucket(bucket_name, file_name)

                if csv_data is not None:
                    sensor_name = file_name.split("_")[0]  # Extract sensor name from file name
                    publish_data_to_mqtt(client, csv_data, sensor_name)
                else:
                    print(f"Failed to read data from {file_name}")
            
            client.loop_forever()
        except KeyboardInterrupt:
            print("Stopping MQTT client...")
            client.disconnect()
    else:
        print("No CSV files found in the bucket.")

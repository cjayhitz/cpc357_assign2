### Smart Environment Monitoring System
Overview
This repository contains the implementation files for a Smart Environment Monitoring System designed to monitor environmental conditions in a data center. It leverages IoT sensors, Google Cloud Platform (GCP) services, and various processing pipelines to ensure optimal data center operation.

### Files and Directories
Source Code
Script.py
Python script for interacting with MongoDB, managing sensor data ingestion, and basic processing tasks.

main_conversion.py
Cloud Function script for transforming raw JSON data into structured CSV format.

pub_sub.py
Script to manage Cloud Pub/Sub topics and handle data flow between ingestion and processing pipelines.

hardware.ino
Arduino code for interfacing with IoT sensors (temperature, humidity, PIR, light sensors) and transmitting data.

Data
dummy_data_latest.csv
Sample processed data file for testing and visualization purposes.

Infrastructure
dev.tf
Terraform configuration file for deploying GCP resources, including Cloud Pub/Sub, Cloud Functions, and BigQuery.

Documentation
Data_Visualization.pdf
Generated visualization report demonstrating insights from the monitored data via Google Looker Studio.

### Setup Instructions
Prerequisites
1. IoT Sensors: Temperature, humidity, PIR, and light sensors connected to an Arduino-compatible board.
2. Google Cloud Platform Account: Access to GCP services such as Cloud Storage, Pub/Sub, Dataflow, and BigQuery.
3. Python Environment: Ensure Python 3.x is installed with necessary dependencies.

### Deployment
1. Hardware Setup: Flash hardware.ino to your IoT device and connect the sensors.
2. Terraform Setup: Run dev.tf to set up the required GCP resources:
3. Cloud Functions: Deploy main_conversion.py as a Cloud Function triggered by data uploads to a Cloud Storage bucket.
4. Pub/Sub Setup: Use pub_sub.py to create and manage Pub/Sub topics for data transmission.
5. MongoDB: Execute Script.py to manage data ingestion into MongoDB.

@@@ Running the Application
Start the IoT sensors and monitor data flow to the MQTT broker.
Ingest data using Script.py.
Trigger data transformations and load data into BigQuery using the Cloud Function and Dataflow pipelines.
Use Looker Studio for data visualization.

### Security Measures
Data Encryption: TLS for data in transit; GCP's KMS for data at rest.
Access Control: IAM roles for restricting access to resources.
Data Masking: Sensitive data anonymized before visualization.

### Authors
Veytri Yogan
Naqib Naqiuddin Iswardi

### License
This repository is released under MIT License.

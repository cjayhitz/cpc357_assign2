provider "google" {
  project = cpc357assign2
  region  = us-central1
}

resource "google_pubsub_topic" "data_topic" {
  name = "data-topic"
}

resource "google_pubsub_subscription" "data_subscription" {
  name  = "data-subscription"
  topic = google_pubsub_topic.data_topic.id

  ack_deadline_seconds = 20
}

resource "google_storage_bucket" "raw_data" {
  name     = "raw-data-bucket-${var.project_suffix}"
  location = var.region

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age = 30
    }
  }
}

resource "google_storage_bucket" "processed_data" {
  name     = "processed-data-bucket-${var.project_suffix}"
  location = var.region

  versioning {
    enabled = true
  }
}

resource "google_bigquery_dataset" "iot_dataset" {
  dataset_id = "iot_dataset"
  location   = var.region
}

resource "google_bigquery_table" "iot_table" {
  dataset_id = google_bigquery_dataset.iot_dataset.dataset_id
  table_id   = "iot_data"

  schema = jsonencode([
    {
      "name": "sensor_id",
      "type": "STRING",
      "mode": "REQUIRED"
    },
    {
      "name": "timestamp",
      "type": "TIMESTAMP",
      "mode": "REQUIRED"
    },
    {
      "name": "temperature",
      "type": "FLOAT",
      "mode": "NULLABLE"
    },
    {
      "name": "humidity",
      "type": "FLOAT",
      "mode": "NULLABLE"
    }
  ])
}

resource "google_cloudfunctions_function" "data_processor" {
  name        = "data-processor"
  runtime     = "python310"
  entry_point = "process_data"
  region      = var.region

  source_archive_bucket = google_storage_bucket.raw_data.name
  source_archive_object = "functions/source_code.zip"

  trigger_http = false
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.data_topic.id
  }
}

resource "google_dataflow_job" "data_transform" {
  name       = "data-transform-job"
  template_gcs_path = "gs://dataflow-templates/latest/Stream_BigQuery"

  parameters = {
    inputTopic  = google_pubsub_topic.data_topic.id
    outputTable = "${google_bigquery_dataset.iot_dataset.dataset_id}.${google_bigquery_table.iot_table.table_id}"
    tempLocation = "gs://${google_storage_bucket.processed_data.name}/temp/"
  }
}

variable "project_suffix" {
  description = "Suffix for unique resource naming."
  type        = string
}

variable "region" {
  description = "Region for resources."
  type        = string
  default     = "us-central1"
}

output "pubsub_topic" {
  value = google_pubsub_topic.data_topic.name
}

output "storage_bucket_raw" {
  value = google_storage_bucket.raw_data.name
}

output "storage_bucket_processed" {
  value = google_storage_bucket.processed_data.name
}

output "bigquery_table" {
  value = google_bigquery_table.iot_table.table_id
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  # ✅ 我帮你填好了你截图里的真实 ID
  project = "project-b02a6651-dfc9-4c25-a5f"
  region  = "us-central1"
}

# 1. 创建 Bucket
resource "google_storage_bucket" "homework_bucket" {
  # ✅ 我帮你改成了一个肯定唯一的名字（加了你的名字）
  name          = "zoomcamp-2026-hw3-bucket-jiazhen-0208-final"
  location      = "US"
  force_destroy = true
  uniform_bucket_level_access = true
}

# 2. 创建 BigQuery Dataset
resource "google_bigquery_dataset" "homework_dataset" {
  dataset_id = "zoomcamp_hw3_dataset"
  location   = "US"
}
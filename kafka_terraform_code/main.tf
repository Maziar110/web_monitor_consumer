resource "aiven_kafka" "kafka_sre_europe-west1" {
  project                 = data.aiven_project.project.project
  cloud_name              = var.aiven_kafka_cloud
  plan                    = var.aiven_kafka_service_plan
  service_name            = var.aiven_kafka_service_name
  maintenance_window_dow  = "tuesday"
  maintenance_window_time = "01:00:00"
  kafka_user_config {
    kafka_version   = "3.7"
    kafka_rest = true
  }
}

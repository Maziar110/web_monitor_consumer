variable "aiven_api_token" {
    type = string
    description = "Token being used for Aiven authentication"
  
}
variable "aiven_kafka_service_plan" {
  default = "startup-2"
}
variable "aiven_kafka_cloud" {
  default = "google-europe-west1"
}
variable "aiven_kafka_service_name" {
  default = "kafka-sre-test"
}
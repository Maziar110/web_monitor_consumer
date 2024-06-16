terraform {

  required_version = "1.3.7"

  required_providers {
    aiven = {
      source  = "aiven/aiven"
      version = "~> 4.18.0"
    }
  }
  
}
provider "aiven" {
  api_token = var.aiven_api_token
}
## Kafka installation
In this directory, you can find Terraform code to provision a Kafka service in Aiven.
If you have your own Kafka instance, simply provide its connection specifications in the .env file.

## How to use it

You need the correct version of Terraform.

Export `Aiven Token` as a terraform environment variable: 
`export TF_VAR_aiven_api_token `

Run `terraform init`

Run `terraform plan` to identify the changes

run `terraform apply`

## Improvements

1. Add a remote backend to sore terraform state in cloud.
2. Add provisioning to code if the management of resources needs to be handled on the fly or with each run of application.
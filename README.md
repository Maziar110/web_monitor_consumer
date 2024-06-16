## Web Monitor Application
This application is able to monitor the state of web URLs and then it will send the result into a Kafka instance.

## What to expect
The project has two parts.

1. **Infrastructure**

There is a folder called `kafka_terraform_code`, the terraform code is designed to provision a Kafka service in (Aiven)["https://aiven.io], to familiar yourself with terraform code and learn how to run it, read the (README)[/kafka_terraform_code/README.md]. 

2. **Application**

The application is responsible to monitor and push/produce the web monitor's status into a Kafka instance. You can provision your Aiven Kafka through the terraform code or provide your own instance's specifications to make it work. 
To learn how to use the application, read the (README)["/application/README.md"] in its folder.
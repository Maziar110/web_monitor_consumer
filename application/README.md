
## How to run the application

1. The application is only able to authenticate to Kafka through SSL protocol, prepare certificates and store them in a folder that is accessible for python app to read from. 
2.  Look at the `.env_template` and set the needed Environment variables in your environment. For directly on the OS, run `export <ENV_NAME>=<ENV_VALUE>` - Make sure for certificates, you are pointing to the right path.
3. Run `pip3 install requirements.txt`
4. Run `python3 main.py`


## How to test the app

Run `python -m unittest` to test all the functionalities or `python -m unittest tests.test_aiven_kafka_producer` for a specific test!


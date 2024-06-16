from website_health_monitor import web_monitor
import logging
from kafka_producer import aiven_kafka_producer
import time
import utils

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


if __name__ == "__main__":
    config_file = utils.load_config_file(config_file_path="./config.yaml")
    if not config_file:
        logging.raiseExceptions("There is no config file to load!")
        # Monitors the define websites and will pack the reult in an arra.
    monitor = web_monitor.WebMonitor(config_file)
    web_monitor_status = monitor.check_websites_urls()
    if not web_monitor_status:
        logging.raiseExceptions("Unable to monitor, you might need to check the config file!")
    # Creates a topic if doesn't exist and passes the pack of array to get produced.
    kafka = aiven_kafka_producer.AivenKafkaProducer()
    message_produced = False
    if kafka.create_topic_if_not_exists():
        producer = kafka.create_producer()
        message_produced = kafka.produce_balk_messages(
            messages=web_monitor_status, 
            message_key="url", 
            producer=producer
            )
    if not message_produced:
        logging.error("Messages didn't produce!")

    # Runs the application periodically based on defined config!   
    time.sleep(config_file["app_run_period_second"])


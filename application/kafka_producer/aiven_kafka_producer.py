from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import os
import json
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


class AivenKafkaProducer:


    def __init__(self):
        '''
        The module is responsible for creating a producer and
        store messages in the specified topics.
        To have this module work, you need to set below environment variables:
         - SERVICE_URI
         - CA_FILE
         - CERTFILE
         - KEYFILE
         - KAFKA_TOPIC
        The module only supports SSL authentication mode.
        '''
        if os.getenv("APP_ENV") == "development":
            load_dotenv()
        self.kafka_config = {
            "bootstrap.servers": os.getenv("SERVICE_URI"),
            "security.protocol": "SSL", 
            "ssl.ca.location": os.getenv("CA_FILE"),
            "ssl.certificate.location": os.getenv("CERTFILE"),
            "ssl.key.location": os.getenv("KEYFILE") 
        }
        self.topic_name = os.getenv("KAFKA_TOPIC")


    def create_topic_if_not_exists(self) -> bool:
        '''
        This methode creates the topic we want to store 
        messages in, if it does not exist.
        '''
        try:
            print(os.path.isfile(str(os.getenv("CERTFILE"))))
            if not os.path.isfile(str(os.getenv("CERTFILE"))):
                logging.error(f"Unable to find the file {str(os.getenv('CERTFILE'))}")
                return False
            admin_client = AdminClient(self.kafka_config)
        except Exception as e:
            logging.error("Unable to authorize to KafKa, make sure certificates are added!")
            return False
        try:
            current_topics = admin_client.list_topics(timeout=5)
            # Expects a dictionary of which the keys are topic name! 
            if self.topic_name in current_topics.topics:
                logging.info(f"The topic {self.topic_name} already exists!")
                return True
            new_topic = NewTopic(
                self.topic_name
            )
            fs = admin_client.create_topics([new_topic])
            # Creates the topic/topics here
            for topic, f in fs.items():
                f.result()
                logging.info(f"The topic {topic} created successfully!")
                return True
        except Exception as e:
            logging.error("Could not list/create the topic: ", e)
            return False
        
    
    def create_producer(self) -> Producer|None:
        '''
        Creates and returns the producer
        '''
        try:
            producer = Producer(self.kafka_config)
            return producer
        except Exception as e:
            logging.error("unable to create the producer, error:", e)
            return None

    def produce_balk_messages(self, messages: list[dict], message_key:str, producer):
        '''
        This method iterates over the list and finds a variable 
        in the dictionary with the key = message_key and uses this as
        the key of message in the topic.
        :params: messages, A list of dictionaries representing messages
        :params: message_key, The key in each message dictionary to use as the Kafka message key.
        :returns: bool
        '''
        try: 
            for message in messages:
                key = message.get(message_key)  # Use get() for safer key access
                if key is None:
                    logging.warning(f"Message key '{message_key}' not found in message: {message}")
                
                producer.produce(self.topic_name, 
                                 key=str(key), 
                                 value=json.dumps(message).encode("utf-8"), # The result is a serialized json encoded and converted to byte
                                 callback=self.acked
                                 )
                producer.poll(1)
            return True
        except Exception as e:
            logging.error(f"Unable to produce the message {message}, error:", e)
            return False


    # This function is being called if any error happen while producing the message
    def acked(self, err, msg):
        if err is not None:
            logging.error(f"Failed to deliver message: {str(msg)} error: ", err)
        else:
            logging.info(f"Message produced: {str(msg)}")


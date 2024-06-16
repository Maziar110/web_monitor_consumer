import validators
import requests
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


class WebMonitor():
    '''
    This module monitors the defined URLs and returns their status
    '''

    def __init__(self, config_file: dict):
        self.config = config_file


    def check_websites_urls(self) -> list[dict]|None:
        '''
        Checks the website and returns the status as dict/json
        :returns: a dictionary as: 
        {
        "url": string, the address of the monitored website.
        "status_code":int, web status codes (200, 400, ...)
        "total_response_time_ms":timedelta, time in ms
        "is_regex_match": bool , if regex matches the content of response,\
             this will be True otherwise False.
        }
        '''
        websites_status = []
        config = self.config
        if not config:
            return None
        websites_to_monitor = config["websites"]
        # Check as many website defined in config file and add -
        # - all the result as an array of dictionaries.
        for website in websites_to_monitor:
            try:
                logging.info(f"checking website {website}")
                # The url should be valid
                if not self.is_valid_url(website):
                    logging.error(f"The url {website} is invalid! please correct it.")
                    return None
                resp = requests.get(website)
                # Sanitizing the result and packing the needed information.
                website_status_details = {
                    "url":  website,
                    "status_code": resp.status_code,
                    "total_response_time_ms": (resp.elapsed.microseconds) / 1000,
                    "is_regex_match": self.is_regex_match(resp.text)
                }   
                websites_status.append(website_status_details)
            except Exception as e:
                logging.error(f"An error occurred while monitoring the website{website}", e)
                return None
        # validation if the result is not an empty list.
        # It can later be validated in a function.
        if len(websites_status) > 0:
            return websites_status
        return None
    
    
    def is_regex_match(self, response_body: str) -> bool:
        '''
        Checks if a defined regex in config file has 
        any match in the body of website
        '''
        config = self.config
        # It's possible that the regex variable is empty -
              # then the exception will be raised.
        try:
            if len(re.findall(config["regex"], response_body, re.IGNORECASE))>0:
                return True
        except Exception as e: 
            logging.warning("No regex in config file or an error on regex match finder ", e)
            return False
        return False


    def is_valid_url(self, url):
        return validators.url(url)
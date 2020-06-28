import requests
import logging

from ezgoals_webex.config.creds import WEBEX_TOKEN

class WebexTeams():

    def __init__(self, rooms):

        self.api_url = 'https://api.ciscospark.com/v1/messages/'
        self.rooms = rooms

    def send_webex_message(self, room, message):

        logging.info('sending to Webex room: {}'.format(room))
        message["roomId"] = room

        logging.info('request body: {}'.format(message))
        resp = requests.post(self.api_url, json=message, headers={'Authorization' : 'Bearer ' + WEBEX_TOKEN, 'Content-Type' : 'application/json'})
        logging.info('response: {}'.format(resp.status_code))
        return resp.status_code

    
    def send_to_rooms(self, message):
        '''
        Sends a message to a list of Webex Teams rooms.
        Args:
            Message: dict of the JSON body for the Webex messages API call. 
        '''

        logging.info("sending Webex messages")
        
        for room in self.rooms.split(','):
            resp_code = self.send_webex_message(room, message)
            if resp_code != 200:
                return "ERROR"
        
        return "OK"
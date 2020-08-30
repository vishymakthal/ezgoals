import logging
import re
import requests
import sys


err_no_comp = "No competition provided"
err_bad_date = "Invalid date provided, must be in format [YYYY-MM-DD]"
err_request = "Error in request"

class FootballData():

    def __init__(self, auth):
        self.auth = auth

    def set_watchlist(self, watchlist):
        self.watchlist = watchlist
    
    def _is_valid_date(self, date_str):

        return re.search(r'\d{4}-\d{2}-\d{2}', date_str)

    def get_matches_for(self,competition='', date='') -> dict:
        '''
        Gets matches for the competition from the date passed in [YYYY-MM-DD]
        '''

        if not competition:
            raise Exception(err_no_comp)

        if not self._is_valid_date(date):
            raise Exception(err_bad_date)

        url = f"https://api.football-data.org/v2/competitions/{competition}/matches?dateFrom={date}&dateTo={date}"

        resp = requests.get(url, headers={'X-Auth-Token': self.auth})

        if resp.status_code != 200:
            raise Exception(f'{err_request}, status code: {resp.status_code}')
        
        return resp.json()


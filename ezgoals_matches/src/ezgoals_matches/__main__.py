from datetime import datetime
from dateutil import tz
import logging

from ezgoals_matches.services.football_data_svc import FootballData
from ezgoals_matches.services.webex_svc import WebexTeams

from ezgoals_matches.config import creds, cnfg


logger = logging.getLogger()
logger.setLevel(logging.INFO)

if __name__ == '__main__':
   main()
    
def main(event, ctx):
    logger.info('starting EzGoals::Event process')

    # grab the current date
    d = datetime.today().strftime('%Y-%m-%d')

    # get a  instance 
    fd = FootballData(creds.AUTH_TOKEN)

    # obtain matches for today 
    matches = []
    for c,_id in cnfg.COMPETITIONS.items():
        try:
            matches.append(fd.get_matches_for(competition=_id,date=d))
        except Exception as e:
            logging.error(f'ERROR getting matches for {c} [{e}]')

    logger.info('starting EzGoals::WebexNotification process')
    # grab a WebexTeams instance
    webex_teams = WebexTeams(creds.WEBEX_ROOMS)

    msg = "## Matches of the Day\n"

    for comp in matches:

        if comp['matches']:
            msg += f"### {comp['competition']['name']} {cnfg.FLAGS[comp['competition']['area']['name']]}\n"
            for m in comp['matches']:
                utc = datetime.strptime(m['utcDate'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=tz.gettz('UTC'))
                msg += f"* {m['homeTeam']['name']} vs {m['awayTeam']['name']} - {utc.astimezone(tz.gettz('America/New_York')).strftime('%I:%M%p')} ET \n"
            msg += '\n'

    # send payload to WebexTeams 
    message = {
        "markdown" : msg 
    }
    resp = webex_teams.send_to_rooms(message)
    if resp != "OK":
        return "ERROR"
    
    return "OK"

from datetime import datetime
import logging

from ezgoals_webex.services.reddit_svc import Reddit
from ezgoals_webex.services.webex_svc import WebexTeams

from ezgoals_webex.config import creds, cnfg


logger = logging.getLogger()
logger.setLevel(logging.INFO)

if __name__ == '__main__':
   main()
    
def main(event, ctx):
    logger.info("starting EzGoals::Event process")

    # grab the current time
    now = datetime.utcnow().timestamp() - cnfg.LOOKBEHIND_SECONDS

    # get a Reddit instance 
    soccer_sub = Reddit(creds.CLIENT_ID, creds.CLIENT_SECRET, creds.USER_AGENT, now)
    soccer_sub.set_watchlist(cnfg.WATCHLIST)

    # obtain goals to publish from /r/soccer
    goals = soccer_sub.search_subreddit('')
    logger.info('goals to send: {}'.format(goals))
    
    logger.info("starting EzGoals::WebexNotification process")

    # grab a WebexTeams instance
    webex_teams = WebexTeams(creds.WEBEX_ROOMS)
    
    # send payload from reddit to Webex Teams channels
    for goal in goals:
        message = {
            "markdown" : cnfg.GOAL_MARKDOWN.format(goal['title'], goal['link'], goal['comments'])
        }
        resp = webex_teams.send_to_rooms(message)
        if resp != "OK":
            return "ERROR"
    
    return "OK"

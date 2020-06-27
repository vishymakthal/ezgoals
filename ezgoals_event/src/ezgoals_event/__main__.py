from datetime import datetime
import logging

from ezgoals_event.services.reddit_svc import Reddit
from ezgoals_event.config import creds, cnfg


logger = logging.getLogger()
logger.setLevel(logging.INFO)

if __name__ == '__main__':
   main()
    
def main(event, ctx):
    logger.info("starting process")

    # grab the current time
    now = datetime.utcnow().timestamp() - cnfg.LOOKBEHIND_SECONDS

    # get a Reddit instance 
    reddit = Reddit(creds.CLIENT_ID, creds.CLIENT_SECRET, creds.USER_AGENT, now)
    reddit.set_watchlist(cnfg.WATCHLIST)

    # obtain goals to publish
    logger.info('goals to send: {}'.format(reddit.search_subreddit(''))) 

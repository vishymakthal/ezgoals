from services.reddit_svc import Reddit
# from webex-svc import Webex
from config import creds, cnfg
 

R = Reddit(creds.CLIENT_ID, creds.CLIENT_SECRET, creds.USER_AGENT)
R.set_watchlist(cnfg.WATCHLIST)
import praw
import logging
import re
import sys
from datetime import timezone, datetime

from config import cnfg

class Reddit():

    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        self.current_time = datetime.utcnow().timestamp() - cnfg.LOOKBEHIND_SECONDS 

    def set_watchlist(self, watchlist):
        self.watchlist = watchlist
    
    def is_goal_to_post(self, title, created_timestamp):
        return re.search('\[[0-9]+\]|[0-9]{1,2}\'', title) and re.search(self.watchlist, title) and created_timestamp > self.current_time


    def search_subreddit(self, query):
        '''
        Calls the reddit API instance to search by the term passed in. Populates
        the global playerHighlights list.
        Args:
            string query: The query to pass to the reddit search function.  
        Returns:
            list[dict] highlights: list of highlight key-value pairs
        '''

        logging.info('grabbing goals from /r/soccer') 
        highlights = []
        logging.info('current UTC - {}'.format(self.current_time))

        for post in self.reddit.subreddit('soccer').search('{} flair:media'.format(query),sort="new", limit=15):
            if self.is_goal_to_post(post.title, post.created):
                logging.info('adding post: {} | {}'.format(post.title, post.created))
                highlights.append({'title' : post.title, 'link' : post.url})

        return highlights

    def search_highlights_by_player(self, player, club):
        '''
        Searches /r/soccer for video clip links containing a player's name. Posts are filtered
        with the flair "media" so that highlights are queried.
        Args:
            string player: Player name to search
            string club: Club name to include in the query alongside player name
        Returns:
            set playerHighlights: list of highlights in key-value form ( {title : link} )
        '''

        return self.search_subreddit(player + ' ' + club) #search the subreddit by full name of player
    
    def search_highlights_by_team(self, club):
        '''
        Searches /r/soccer for video clip links containing a team name. Posts are filtered
        with the flair "media" so that highlights are queried.
        Args:
            string club: Club name to include in the query alongside player name
        Returns:
            set playerHighlights: list of highlights in key-value form ( {title : link} )
        '''

        return self.search_subreddit(club)
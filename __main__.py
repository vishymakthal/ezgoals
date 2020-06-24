from services import R
import logging

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO)
    logging.info("starting process")
    logging.info('goals to send: {}'.format(R.search_subreddit(''))) 
import json
from datetime import datetime
from data_agent.dataAgent import DataAgent
from config import config


def format_data(data):
    return data.replace("\n", " newlinechar ").replace("\r", " newlinechar ").replace('"', "'")


def acceptable(data):
    if(len(data.split(' ')) > 50 or len(data) < 1 or len(data) > 1000 or data == '[deleted]' or data == '[removed]'):
        return False
    return True


if __name__ == '__main__':
    data_agent = DataAgent()
    row_count = 0
    paired_count = 0

    with open(config['reddit_scraper']['datafile'], buffering=1024) as f:
        for row in f:
            row_count += 1
            row = json.loads(row)
            parent_id = row['parent_id'] or None
            body = format_data(row['body'])
            score = row['score']
            tag = row['subreddit']
            source = 'reddit'
            comment_id = row['name']

            if score >= 2 and acceptable(body):
                if not data_agent.find_comment_by_id(comment_id):
                    data_agent.push_comment(body, score, source, comment_id, parent_id, tag)

            if row_count % 100000 == 0:
                print("Total Rows: {}, Paired Rows: {}, Time: {}".format(row_count, paired_count, datetime.now()))
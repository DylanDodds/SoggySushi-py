import json
from datetime import datetime

from pymongo import MongoClient
from datetime import datetime
from config import config


class DataAgent:
    def __init__(self):
        try:
            self.connection_string = "mongodb://{}:{}@{}:{}".format(config['mongo']['username'], config['mongo']['password'], config['mongo']['hostname'], config['mongo']['port'])
            self.client = MongoClient(self.connection_string)
            self.converse_db = self.client[config['mongo']['collector_db']]
        except Exception as err:
            print('[DataAgent] Failed to connect to MongoDb... ', str(err))


    def push_comment(self, body, score, source, comment_id, parent_id=None, tag=None, author=None):
        try:
            posts = self.converse_db.posts
            comment_data = {
                'comment_id': comment_id,
                'parent_id': parent_id,
                'content': body,
                'score': score,
                'source': source,
                'tag': tag,
                'time_created_utc': datetime.now(),
                'author': author
            }

            if self.find_comment_by_id(comment_id):
                print('[DataAgent] Attempted to insert a comment with an existing id')
                return None

            result = posts.insert_one(comment_data)
            return result.inserted_id
        except Exception as err:
            print('[DataAgent] Failed to push comment... ', str(err))
            return None


    def update_comment_by_id(self, cid, pid, body, source, tag, score):
        try:
            self.converse_db.update_one({'comment_id': cid}, {
                '$set': {
                    'comment_id': cid,
                    'parent_id': pid,
                    'content': body,
                    'source': source,
                    'tag': tag,
                    'score': score,
                    'time_update_utc': datetime.now()
                }
            }, upsert=False)
        except Exception as err:
            print('[DataAgent] Failed to update comment... ', str(err))
            return False


    def update_comments_by_parent_id(self, pid, body, source, tag, score):
        try:
            self.converse_db.update_one({'parent_id': pid}, {
                '$set': {
                    'parent_id': pid,
                    'content': body,
                    'source': source,
                    'tag': tag,
                    'score': score,
                    'time_update_utc': datetime.now()
                }
            }, upsert=False)
        except Exception as err:
            print('[DataAgent] Failed to update comment... ', str(err))
            return False


    def push_comment_collection(self, comment_collection):
        try:
            posts = self.converse_db.posts
            result = posts.insert_many(comment_collection)
            return result.inserted_id
        except Exception as err:
            print('[DataAgent] Failed to push comment... ', str(err))
        return None


    def find_comment_by_id(self, cid):
        try:
            posts = self.converse_db.posts
            result = posts.find_one({'comment_id': cid})
            return result
        except Exception as err:
            print("[DataAgent] Could not find parent with id: {}".format(cid), str(err))
            return None


    def find_comments(self, query={}):
        try:
            posts = self.converse_db.posts
            data = posts.find(query)
            results = []
            for comment in data:
                results.append(comment)
            return results
        except Exception as err:
            print("[DataAgent] Could not find comments with the query: {}\n{}".format(str(query), str(err)))
            return None


    def generate_learning_batch(self, query={}, cache_to_file=True):
        try:
            learning_batch = [] # {comment: '', response: ''}

            # Find all posts with parents
            query['parent_id'] = {'$ne': None}
            child_comments = self.find_comments(query)
            for child_comment in child_comments:
                parent_comment = self.find_comment_by_id(child_comment['parent_id'])
                if parent_comment:
                    learning_batch.append({'comment': parent_comment['content'], 'response': child_comment['content']})
            if cache_to_file:
                filename = 'learning_batch_{}.json'.format(datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))
                with open(filename, 'w') as file:
                    file.write(json.dumps(learning_batch))
                print('[DataAgent] Exported learning batch to {}'.format(filename))
            return learning_batch
        except Exception as err:
            print("[DataAgent] Could not generate learning batch;\n    query: {}\n{}".format(str(query), str(err)))
            return None


    def load_learning_batch(self, filename):
        with open(filename) as data:
            output = json.load(data)
            return output
from pymongo import MongoClient
import datetime

class MongoDB():
    '''
    Class MongoDB is used to write user's Pomodoro sessions to a MongoDocument store.
    '''
    # def __init__(self):

    def write_to_database(self, goal_string):
        # Setup MongoDB client
        client = MongoClient()
        # Define the data base
        db = client.pomodoro_database
        # Define the collection
        goals = db.goals_test
        result = goals.insert_one({"date":datetime.datetime.utcnow(), "goal":goal_string}).inserted_id
        return str(goals.find_one({"_id": result}))

from pymongo import MongoClient
import datetime
import pprint
from bson.objectid import ObjectId

client = MongoClient()
db = client.pomodoro_database
# Define the collection


goal = {"goal": "my_goal", "date":datetime.datetime.utcnow()}
goals = db.goals

goal_id = goals.insert_one(goal).inserted_id


pprint.pprint(goals.find_one({"_id": ObjectId('5aa7bf6c813f4341069b231a')}))
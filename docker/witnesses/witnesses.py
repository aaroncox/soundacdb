from datetime import datetime
from muse import Muse
from pymongo import MongoClient
from pprint import pprint
from time import gmtime, strftime
from apscheduler.schedulers.background import BackgroundScheduler
import collections
import time
import sys
import os

muse = Muse(node=os.environ['steemnode'])
rpc = muse.rpc

mongo = MongoClient("mongodb://mongo")
db = mongo.musedb

# misses = {}

# Command to check how many blocks a witness has missed
# def check_misses():
#     global misses
#     witnesses = rpc.get_witnesses_by_vote('', 100)
#     for witness in witnesses:
#         owner = str(witness['owner'])
#         # Check if we have a status on the current witness
#         if owner in misses.keys():
#             # Has the count increased?
#             if witness['total_missed'] > misses[owner]:
#                 # Update the misses collection
#                 record = {
#                   'date': datetime.now(),
#                   'witness': owner,
#                   'increase': witness['total_missed'] - misses[owner],
#                   'total': witness['total_missed']
#                 }
#                 db.witness_misses.insert(record)
#                 # Update the misses in memory
#                 misses[owner] = witness['total_missed']
#         else:
#             misses.update({owner: witness['total_missed']})



def update_witnesses():
    now = datetime.now().date()
    scantime = datetime.now()
    users = rpc.lookup_witness_accounts('', 100)
    pprint("[MUSE] - Update Witnesses (" + str(len(users)) + " accounts)")
    # db.witness.remove({})
    for user in users:
        witness = rpc.get_witness_by_account(user)
        pprint(witness)
        for key in ['last_mbd_exchange_update']:
            witness[key] = datetime.strptime(witness[key], "%Y-%m-%dT%H:%M:%S")
        # Convert to Numbers
        for key in ['votes', 'total_missed']:
            witness[key] = float(witness[key])
        witness.update({
            'account': user
        })
        db.witness.update({'_id': user}, {'$set': witness}, upsert=True)

def run():
    update_witnesses()
    # check_misses()

if __name__ == '__main__':
    # Start job immediately
    run()
    # Schedule it to run every 1 minute
    scheduler = BackgroundScheduler()
    scheduler.add_job(run, 'interval', minutes=1, id='run')
    scheduler.start()
    # Loop
    try:
        while True:
            sys.stdout.flush()
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

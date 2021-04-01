from datetime import datetime, timedelta
from muse import Muse
from pymongo import MongoClient
from pprint import pprint
import collections
import time
import sys
import os

from apscheduler.schedulers.background import BackgroundScheduler

muse = Muse(node=os.environ['steemnode'])
rpc = muse.rpc

mongo = MongoClient("mongodb://mongo")
db = mongo.musedb

# mvest_per_account = {}

# def load_accounts():
#     pprint("[MUSE] - Loading mvest per account")
#     for account in db.account.find():
#         if "name" in account.keys():
#             mvest_per_account.update({account['name']: account['vesting_shares']})

def update_props_history():
    pprint("[MUSE] - Update Global Properties")
    props = rpc.get_dynamic_global_properties()
    for key in ['confidential_mbd_supply', 'confidential_supply', 'current_mbd_supply', 'current_supply', 'total_reward_fund_muse', 'total_vesting_fund_muse', 'total_vesting_shares', 'virtual_supply']:
        props[key] = float(props[key].split(" ")[0])
    for key in ['time']:
        props[key] = datetime.strptime(props[key], "%Y-%m-%dT%H:%M:%S")
    db.props_history.insert(props)

def update_chain_props_history():
    pprint("[MUSE] - Update chain properties")
    props = rpc.get_chain_properties()
    for key in ['account_creation_fee', 'streaming_platform_update_fee']:
        props[key] = float(props[key].split(" ")[0])
    db.chain_history.insert(props)


def update_history():

    update_props_history()
    update_chain_props_history()

    # Load all accounts
    users = rpc.lookup_accounts(-1, 1000)
    more = True
    while more:
        newUsers = rpc.lookup_accounts(users[-1], 1000)
        if len(newUsers) < 1000:
            more = False
        users = users + newUsers

    # Set dates
    now = datetime.now().date()
    today = datetime.combine(now, datetime.min.time())

    pprint("[MUSE] - Update History (" + str(len(users)) + " accounts)")
    # Snapshot User Count
    db.statistics.update({
      'key': 'users',
      'date': today,
    }, {
      'key': 'users',
      'date': today,
      'value': len(users)
    }, upsert=True)

    # Update history on accounts
    for user in users:

        accountname = user
        # if accountname != 'williamhill1934':
        #     continue

        # Load State
        account = rpc.get_accounts([accountname])[0]
        # pprint(state)
        doc = account.copy()
        # Get Account Data
        # account = collections.OrderedDict(sorted(doc['account'].items()))
        doc['scanned'] = datetime.now()
        # miner = rpc.lookup_miner_accounts(accountname, 1)
        # if len(miner) > 0 and miner[0][0] == accountname:
        #     doc.update({'miner_id': miner[0][1]})
        # doc.update({
        #     'account': account
        # })
        # total = 0
        # for balance in doc['balances']:
        #     for symbol in assets:
        #         if 'asset_type' in balance and assets[symbol] == balance['asset_type']:
        #             total = total + int(balance['balance'])
        #             balance.update({
        #                 'symbol': symbol,
        #                 'balance': int(balance['balance'])
        #             })
        # for balance in doc['vesting_balances']:
        #     total = total + int(balance['balance']['amount'])
        #     balance.update({
        #         'balance': {
        #             'amount': int(balance['balance']['amount']),
        #             'asset_id': balance['balance']['asset_id']
        #         }
        #     })
        for key in ['balance', 'mbd_balance', 'vesting_withdraw_rate', 'vesting_shares']:
            doc[key] = float(doc[key].split(" ")[0])
        for key in ['last_active_proved', 'last_market_bandwidth_update', 'last_activity_payout', 'last_post', 'mbd_seconds_last_update', 'last_root_post', 'last_owner_proved', 'created', 'last_active', 'last_owner_update', 'last_account_recovery', 'last_vote_time', 'last_bandwidth_update', 'mbd_last_interest_payment']:
            doc[key] = datetime.strptime(doc[key], "%Y-%m-%dT%H:%M:%S")

        # doc['account'].update({'total_balance': total})
        # if accountname == 'williamhill1934':
        #     pprint(doc)
        #     sys.stdout.flush()
        # for vote in doc['votes']:
        #     if 'witness_account' in vote:
        #         search = vote['witness_account']
        #         result = [e for e in users if e[1] == search]
        #         if len(result):
        #             vote.update({
        #                 'name': result[0][0]
        #             })
        # Save current doc of account
        db.account.update({'_id': accountname}, doc, upsert=True)
    #     # Create our Snapshot dict
    #     wanted_keys = ['name', 'proxy_witness', 'activity_shares', 'average_bandwidth', 'average_market_bandwidth', 'savings_balance', 'balance', 'comment_count', 'curation_rewards', 'lifetime_bandwidth', 'lifetime_vote_count', 'next_vesting_withdrawal', 'reputation', 'post_bandwidth', 'post_count', 'posting_rewards', 'mbd_balance', 'savings_mbd_balance', 'mbd_last_interest_payment', 'mbd_seconds', 'mbd_seconds_last_update', 'to_withdraw', 'vesting_balance', 'vesting_shares', 'vesting_withdraw_rate', 'voting_power', 'withdraw_routes', 'withdrawn', 'witnesses_voted_for']
    #     snapshot = dict((k, account[k]) for k in wanted_keys if k in account)
    #     snapshot.update({
    #       'account': user,
    #       'date': today,
    #       'followers': len(account['followers']),
    #       'following': len(account['following']),
    #     })
    #     # Save Snapshot in Database
    #     db.account_history.update({
    #       'account': user,
    #       'date': today
    #     }, snapshot, upsert=True)

def update_supply():
    pprint("updating supply")
    now = datetime.now().date()
    today = datetime.combine(now, datetime.min.time())
    assets = muse.rpc.get_asset("2.28.0")
    pprint(assets)
    objects = muse.rpc.get_objects(['2.28.1'])
    tokens = int(objects[0]['current_supply'])
    total = int(assets['max_supply'])
    vests = total - tokens

    supply = {
        '_id': today,
        'muse': tokens,
        'vests': vests,
        'total': total
    }
    db.supply_history.update({'_id': today}, supply, upsert=True)

if __name__ == '__main__':
    # Load all account data into memory
    # load_accounts()
    # Start job immediately
    update_supply()
    # update_history()
    # Schedule it to run every 6 hours
    scheduler = BackgroundScheduler()
    # scheduler.add_job(update_supply, 'interval', minutes=60, id='update_supply')
    # scheduler.add_job(update_history, 'interval', minutes=15, id='update_history')
    # scheduler.start()
    # Loop
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

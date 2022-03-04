"""
This file will perform the calculations based on the information submitted
via the Flask application

TODO: add try/except to catch errors and incorrect submission formats/values
"""
from datetime import datetime
from pprint import pprint
import collections
import json


# def main():
# 	with open("transactions.json", "r") as transaction_submissions:
# 		transactions = json.load(transaction_submissions)
#
# 	add_transactions(transactions)
# 	spend_points()
# 	get_points_balance()


# TODO: write a function that takes in transactions to create a list like the below - call the route in API

def add_transactions():
	"""
	Function to pull transactions.json file with transactions
	submitted by user via Flask API
	:return: payer transactions sorted by earliest timestamp
	"""
	with open("transactions.json", "r") as transaction_submissions:
		transactions = json.load(transaction_submissions)
	payer_transactions = transactions
	# [{"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
	#                       {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
	#                       {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
	#                       {"payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z"},
	#                       {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}]
	# print(payer_transactions)
	# use lambda to sort the list of payer transactions by the timestamp
	# the oldest transaction should be the first transaction so when iterating through the list later
	# it will begin with the oldest set of points by default
	payer_transactions.sort(key=lambda date: datetime.strptime(date["timestamp"], '%Y-%m-%dT%H:%M:%SZ'))
	
	print(f" payer transaction --> {payer_transactions}")
	return payer_transactions
	

# TODO: write a function to spend points that takes in the number of points to be spent
#  - call the route in API - use a submit/POST request to send the data to the API

payer_balances = []
points_available_to_spend_by_payer = []
payer_points = []


def spend_points(points_to_spend, payer_transactions):
	"""
	Function to calculate how many points get spent by each payer
	take into account the total number of points available to spend
	and deduct the amounts from the payer transactions in order of oldest timestamp.
	Function should only spend up to the total in each transaction.
	Once the total for that transaction has been met, move to the next transaction.
	This continues until the total points to spend is reached,
	keeping track of how many total points were spent by each payer to update the points balance.

	:param payer_transactions:
	:param points_to_spend:
	:return: a new list of points spent for each payer
	"""
	# points cannot go into the negative so only spend points if the total is greater than 0
	# if points in a transaction reaches 0, stop spending points
	# if total equals 0, we want to stop spending points to prevent going negative
	transactions = payer_transactions
	for transaction in transactions:
		# if points to spend is greater than transaction points,
		# only spend the transaction points
		payer = transaction["payer"]
		point = transaction["points"]
		points_available_to_spend_by_payer.append({payer: point})
		if points_to_spend > 0:
			
			if points_to_spend >= point:
				# print(f" points spent by {transaction['payer']} = {point}")
				points_to_spend = abs(point - points_to_spend)
				# print(f" new total is {points_to_spend} and {transaction['payer']} = {point}")
				# add the payer and total spent to new empty payer_balance list
				payer_balances.append({transaction['payer']: -point})
			
			else:
				# if the transaction points are greater than the amount of points to spend,
				# only spend the points to spend points
				# print(f" {transaction['payer']} = {point} points to spend greater than total. Only spend {points_to_spend}  ")
				payer_balances.append({payer: -points_to_spend})
				points_to_spend = points_to_spend - point
		
		# print(f" new total is {abs(points_to_spend)} and {transaction['payer']} balance is = {abs(points_to_spend)}")
	
	# sum the points in the payer_balances list
	payer_balance = collections.Counter()
	for points in payer_balances:
		payer_balance.update(points)
	
	# turn the results of sums in the collection into a dictionary
	payer_balance = dict(payer_balance)
	# print(f'the result is = {payer_balance}')
	
	for payers in payer_balance:
		payer = payers
		point = payer_balance[payer]
		payer_points.append({'payer': payer, 'points': point})
	# add the payer and total spent to new empty balance list
	# if a payer does not exist in balance, append the payer/points to balance
	# for payer_balance in balance:
	# if not any(transaction['payer'] == balance[0]["payer"] in keys for keys in balance):
	# if payer_balance not in balance:
	# # if 'DANNON' not in payer["payer"]:
	#     print(transaction['payer'],  transaction['points'])
	#     # payer_balance[payer] = point
	#     balance.append([payer, point])
	
	# # if a payer is already in the balance list, do not append it again,
	# # instead, sum the points and update the value for that payer
	# else:
	#     print(f"---balance payer {transaction['payer']} is already in balance, point = {point}")
	#     # point += point
	#     # balance.append(point)
	#     print(f"balance to update ---- {transaction['payer']}")
	
	print(f"payer points --> {payer_points}")
	return payer_points


payer_balance_after_spending = {}


def get_points_balance():
	"""
	Function to calculate the balance remaining for each payer after points have been spent
	:return: dictionary with the new balance for each payer

	counter = collections.Counter()
for d in ini_dict:
	counter.update(d)

result = dict(counter)
	"""
	
	# sum the points spent by each payer
	payer_transaction_points = collections.Counter()
	for points in points_available_to_spend_by_payer:
		payer_transaction_points.update(points)
	
	payer_transaction_points = dict(payer_transaction_points)
	# print(payer_transaction_points)
	
	# match the points from the transactions and points spent to get the balance left after spending
	
	for transaction_payer in payer_transaction_points:
		for payer in payer_points:
			if transaction_payer == payer['payer']:
				balance_leftover = payer_transaction_points[transaction_payer] + payer['points']
				
				payer_balance_after_spending[transaction_payer] = balance_leftover
	
	print(f" balance after spending --> {payer_balance_after_spending}")
	return payer_balance_after_spending


"""
Expected Result
[
    { "payer": "DANNON", "points": -100 },
    { "payer": "UNILEVER", "points": -200 },
    { "payer": "MILLER COORS", "points": -4,700 }
]

Balance Result
{
"DANNON": 1000,
"UNILEVER": 0,
"MILLER COORS": 5300
}

"""

# if __name__ == "__points__":
# 	main()

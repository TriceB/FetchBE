"""
This file will perform the calculations based on the information submitted
via the Flask application
Transaction submissions are stored in transactions.json file then parsed through in this file.
The balances for each payer will be calculated using this file and displayed on screen in the index.html page

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

def get_transactions():
	"""
	Function to pull transactions.json file with transactions
	submitted by user via Flask API
	:return: payer transactions sorted by earliest timestamp
	"""
	with open("transactions.json", "r") as transaction_submissions:
		transactions = json.load(transaction_submissions)
	payer_transactions = transactions
	# payer_transactions = [{"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
	#                       {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
	#                       {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
	#                       {"payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z"},
	#                       {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}]
	# print(payer_transactions)
	# use lambda to sort the list of payer transactions by the timestamp
	# the oldest transaction should be the first transaction so when iterating through the list later
	# it will begin with the oldest set of points by default
	payer_transactions.sort(key=lambda date: datetime.strptime(date["timestamp"], '%Y-%m-%dT%H:%M:%SZ'))
	
	print(f"payer transactions sorted --> {payer_transactions}")
	return payer_transactions
	

# TODO: write a function to spend points that takes in the number of points to be spent
#  - call the route in API - use a submit/POST request to send the data to the API

payer_points_spent = []
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
				# add the payer and total spent to new empty points_spent_by_payer list
				payer_points_spent.append({transaction['payer']: -point})
				# print(payer_points_spent)
			
			else:
				# if the transaction points are greater than the amount of points to spend,
				# only spend the points to spend points
				# print(f" {transaction['payer']} = {point} points to spend greater than total. Only spend {points_to_spend}  ")
				payer_points_spent.append({payer: -points_to_spend})
				points_to_spend = points_to_spend - point
				# print(payer_points_spent)
				# print(f" new total is {abs(points_to_spend)} and {transaction['payer']} balance is = {abs(points_to_spend)}")
		
		else:
			# if the points are all spent before getting through the whole list, the rest of the payers have spent 0 points
			# add payers who have not spent any points to the dict with 0 points
			# this will keep the total correct when calculating the balances left after spending
			payer_points_spent.append({payer: 0})
			# print(f"payer balances from last else --> {payer_points_spent}")
			
	# sum the points in the payer_points_spent list
	points_spent_by_payer = collections.Counter()
	for points in payer_points_spent:
		points_spent_by_payer.update(points)
	
	# turn the results of sums in the collection into a dictionary
	points_spent_by_payer = dict(points_spent_by_payer)
	# print(f'the result is = {points_spent_by_payer}')
	
	for payers in points_spent_by_payer:
		payer = payers
		point = points_spent_by_payer[payer]
		payer_points.append({'payer': payer, 'points': point})
	# add the payer and total spent to new empty balance list
	# if a payer does not exist in balance, append the payer/points to balance
	# for points_spent_by_payer in balance:
	# if not any(transaction['payer'] == balance[0]["payer"] in keys for keys in balance):
	# if points_spent_by_payer not in balance:
	# # if 'DANNON' not in payer["payer"]:
	#     print(transaction['payer'],  transaction['points'])
	#     # points_spent_by_payer[payer] = point
	#     balance.append([payer, point])
	
	# # if a payer is already in the balance list, do not append it again,
	# # instead, sum the points and update the value for that payer
	# else:
	#     print(f"---balance payer {transaction['payer']} is already in balance, point = {point}")
	#     # point += point
	#     # balance.append(point)
	#     print(f"balance to update ---- {transaction['payer']}")
	
	# print(f"payer points --> {payer_points}")
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
	
	print("Payer Balances from transactions submitted in index.html calculated in points.py")
	print(f" balance after spending --> {payer_balance_after_spending}")
	return payer_balance_after_spending


# get_transactions()
# spend_points(9000, add_transactions())
# get_points_balance()
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

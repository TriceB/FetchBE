"""
Background
Our users have points in their accounts. Users only see a single balance in their accounts.
But for reporting purposes we actually track their points per payer/partner. In our system,
each transaction record contains: payer (string), points (integer), timestamp (date).
For earning points it is easy to assign a payer, we know which actions earned the points.
And thus which partner should be paying for the points.
When a user spends points, they don't know or care which payer the points come from.
But, our accounting team does care how the points are
spent. There are two rules for determining what points to "spend" first:

● We want the oldest points to be spent first (oldest based on transaction timestamp,
not the order they’re received)
● We want no payer's points to go negative.

We expect your web service to

Provide routes that:
● Add transactions for a specific payer and date.
● Spend points using the rules above and return a list of { "payer": <string>, "points": <integer> } for each call.
● Return all payer point balances.

Note:
● We are not defining specific requests/responses. Defining these is part of the exercise.
● We don’t expect you to use any durable data store. Storing transactions in memory is acceptable for the exercise.

"""
from datetime import datetime
from pprint import pprint

# TODO: write a function that takes in transactions to create a list like the below - call the route in API
payer_transactions = [{"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
                      {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
                      {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
                      {"payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z"},
                      {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}]

# use lambda to sort the list of payer transactions by the timestamp
# the oldest transaction should be the first transaction so when iterating through the list later
# it will begin with the oldest set of points by default
payer_transactions.sort(key=lambda date: datetime.strptime(date["timestamp"], '%Y-%m-%dT%H:%M:%SZ'))
pprint(payer_transactions)

# TODO: write a function to spend points that takes in the number of points to be spent
#  - call the route in API - use a submit/POST request to send the data to the API


def spend_points(points_to_spend):
    """
    Function to calculate how many points get spent by each payer
    take into account the total number of points available to spend
    and deduct the amounts from the payer transactions in order of oldest timestamp.
    Function should only spend up to the total in each transaction.
    Once the total for that transaction has been met, move to the next transaction.
    This continues until the total points to spend is reached,
    keeping track of how many total points were spent by each payer to update the points balance.
    
    :param points_to_spend:
    :return: a new list of points spent for each payer
    """
    # points cannot go into the negative so only spend points if the total is greater than 0
    # if total equals 0, we want to stop spending points to prevent going negative
   
        

def get_points_balance():
    """
    Function to calculate the balance remaining for each payer after points have been spent
    :return: dictionary with the new balance for each payer
    """


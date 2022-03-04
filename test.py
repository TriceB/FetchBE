import unittest
import datetime
import main

transactions = [{"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
                {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
                {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
                {"payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z"},
                {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}]

payer_points_spent = [
						{"payer": "DANNON", "points": -100},
						{"payer": "UNILEVER", "points": -200},
						{"payer": "MILLER COORS", "points": -4700}
					]

balance_after_spending = {
							"DANNON": 1000,
							"UNILEVER": 0,
							"MILLER COORS": 5300
							}


class TestCalculateBalanceAfterSpendingPoints(unittest.TestCase):
	def test_spend_points(self):
		self.assertEqual(main.spend_points(5000), payer_points_spent)
		self.assertEqual(main.get_points_balance(), balance_after_spending)
	# def test_get_balance(self):
	


if __name__ == '__main__':
	unittest.main()
	

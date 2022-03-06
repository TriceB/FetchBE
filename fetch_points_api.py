from flask import Flask, render_template, request
import json
from datetime import datetime
import main
from utilities import points

app = Flask(__name__)

spend_points = main.spend_points(5000)

transaction_information = []


@app.route('/', methods=["GET", "POST"])
def transactions_form():
	"""
	This route will display the index.html page
	where the user can submit multiple transactions.
	Transactions will be stored in transactions.json file
	After submitting transactions, user can submit the
	total customer points to calculate the balance by payer
	
	TODO: add try/except to catch errors and incorrect submission formats/values
	- fix issue causing index not to display balance from main.py - fixed
	- fix issue causing index not to display the points to spend - fixed
	
	"""
	# print(spend_points)
	
	# run the function to get points balance per the assignment instructions
	main.get_points_balance()
	
	# display the expected balance result based on the assignment instructions
	balances = main.payer_balance_after_spending
	# print(balances)
	
	# when the user clicks the "Add a Transaction" button, this will be a POST request
	# and the form will gather all of the information submitted to store in the json
	# file and display all transactions submitted back to the user onscreen
	if request.method == "POST" and request.form.get('action') == "Add A Transaction":
		# store all of the user inputs into variables
		payer_name = request.form.get('payerName').upper()
		payer_points = request.form.get('transactionPoints')
		transaction_date = request.form.get('transactionDate')
		transaction_time = request.form.get('transactionTime')
		
		# if all fields are left blank, display alert message to inform user all fields are required to be completed
		if not payer_name or not payer_points or not transaction_date or not transaction_time:
			error_statement = "All Form Fields Are Required"
			
			# if payer points are entered, check if the input is a number by trying to cast it to int
			# if unable to cast it to int, display error message to inform user to input a number
			if payer_points:
				try:
					payer_points = int(payer_points)
				except ValueError:
					points_error = "*Please enter a number"
					return render_template("index.html",
					                       error_statement=error_statement,
					                       payer_name=payer_name,
					                       points_error=points_error,
					                       transaction_date=transaction_date,
					                       transaction_time=transaction_time)
			
			# check if the user has input the transaction date but has not entered the time
			# confirm if the date has been entered in the correct format
			# if not in the correct format, display error message to user to enter using the MM/DD/YYYY format
			if transaction_date and not transaction_time:
				print("made it to date check")
				try:
					date_format = "%m/%d/%Y"
					datetime.strptime(transaction_date, date_format)
				except ValueError:
					date_format_error = "*The date format entered is incorrect. It should be MM/DD/YYYY"
					return render_template("index.html",
					                       error_statement=error_statement,
					                       payer_name=payer_name,
					                       payer_points=payer_points,
					                       date_format_error=date_format_error,
					                       transaction_time=transaction_time)
			
			# check if the user has input the transaction time but has not entered the date
			# confirm if the time has been entered in the correct format
			# if not in the correct format, display error message to user to enter using the HH:MM format
			if transaction_time and not transaction_date:
				print("made it to time check")
				try:
					time_format = "%H:%M"
					datetime.strptime(transaction_time, time_format)
				except ValueError:
					time_format_error = "*The time format entered is incorrect. It should be HH:MM"
					return render_template("index.html", error_statement=error_statement,
					                       payer_name=payer_name,
					                       payer_points=payer_points,
					                       transaction_date=transaction_date,
					                       time_format_error=time_format_error,
					                       transaction_time=transaction_time)
			
			# check if the user has input both the transaction time and the date
			# confirm if both have been entered in the correct format
			# if not display both error messages information the user of the correct format
			elif transaction_date and transaction_time:
				try:
					date_format = "%m/%d/%Y"
					datetime.strptime(transaction_date, date_format)
					time_format = "%H:%M"
					datetime.strptime(transaction_time, time_format)
				except ValueError:
					date_format_error = "*The date format entered is incorrect. It should be MM/DD/YYYY"
					time_format_error = "*The time format entered is incorrect. It should be HH:MM"
					return render_template("index.html",
					                       error_statement=error_statement,
					                       payer_name=payer_name,
					                       payer_points=payer_points,
					                       date_format_error=date_format_error,
					                       time_format_error=time_format_error)
			
			return render_template("index.html",
			                       error_statement=error_statement,
			                       payer_name=payer_name,
			                       payer_points=payer_points,
			                       transaction_date=transaction_date,
			                       transaction_time=transaction_time)
		
		payer_points = int(payer_points)
		print("Adding Transaction...")
		# concatenate the transaction date and time together to turn it into a datetime object
		transaction_date_time = transaction_date + " " + transaction_time
		
		# convert the string into datetime
		full_date_time = datetime.strptime(transaction_date_time, '%m/%d/%Y %H:%M')
		
		# turn the datetime into a datetime object in the format of the timestamp
		full_date_time_object = full_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
		
		# put all of formatted transaction information into a dict to append to transaction_information list
		transaction_information_dict = {'payer': payer_name,
		                                'points': payer_points,
		                                'timestamp': full_date_time_object
		                                }
		
		# first check if the transaction entered is a unique transaction, meaning it does not match a dict already in
		# the transactions list
		# if the transaction is already in the list, do not add it to the transactions list, display an alert
		if transaction_information_dict in transaction_information:
			transactions_already_exists_message = "This Transaction has already been entered. Please enter a new " \
			                                      "unique transaction."
			return render_template("index.html",
			                       transactions_already_exists_message=transactions_already_exists_message)
		# if the transaction does not already exist in the list, it is unique - add transaction to list
		else:
			transaction_information.append(transaction_information_dict)
		
		# format the list of transactions into json with 4 indent spaces for easier readability
		transaction_json = json.dumps(transaction_information, indent=4)
		
		# write all of the transaction submissions to the json file
		# this file will get overridden each time the flask app is run to
		# keep only the current set of transactions
		with open("transactions.json", "w") as transactions_file:
			transactions_file.write(transaction_json)
			transactions_file.close()
	
	# when the user enters the amount of points to spend and clicks
	# the "Calculate The Balance" button, the payer balances will be calculated
	if request.method == "POST" and request.form.get("action") == "Calculate The Balance":
		print("Calculating Balance per Submission...")
		# store the user submitted points
		points_from_submission = request.form.get("pointsToSpend")
		
		# check if the user has entered points for submission
		# if no entry, display an error requesting they enter points to spend
		if not points_from_submission:
			error_statement = "Please Enter Points Available to Spend"
			return render_template("index.html",
			                       error_statement=error_statement,
			                       points_from_submission=points_from_submission)
		
		# if the user has entered points for submission, check if the input is a number
		# by casting it to int. If unable to cast to int, the user has input a string
		# inform the user to input a number
		elif points_from_submission:
			try:
				points_from_submission = int(points_from_submission)
			except ValueError:
				points_submission_error = "*Please enter a number"
				return render_template("index.html",
				                       points_submission_error=points_submission_error)
		
		points_from_submission = int(points_from_submission)
		
		# run the function to get transaction from the json file
		transactions = points.get_transactions()
		
		# run the function to spend points
		points.spend_points(points_from_submission, transactions)
		
		# run the function to calculate the balance for each payer
		balance_from_submission = points.get_points_balance()
		return render_template("index.html",
		                       transaction_information=transaction_information,
		                       points_from_submission=points_from_submission,
		                       balance_from_submission=balance_from_submission)
	
	# display the calculated balances from the assignment instructions to
	# show the user an example of the expected output after inputting and
	# calculating transactions
	return render_template("index.html",
	                       balances=balances)


if __name__ == '__main__':
	app.run(debug=True)
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True

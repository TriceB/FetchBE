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
    # when the user clicks the "Add a Transaction" button, the form will gather
    # all of the information submitted to store in the json file and display
    # all transactions submitted back to the user onscreen
    if request.method == "POST" and request.form.get('action') == "Add A Transaction":
        
        payer_name = request.form.get('payerName').upper()
        payer_points = request.form.get('transactionPoints')
        
        transaction_date = request.form.get('transactionDate')
        transaction_time = request.form.get('transactionTime')
        
        if not payer_name or not payer_points or not transaction_date or not transaction_time:
            error_statement = "All Form Fields Are Required"
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
        transaction_date_time = transaction_date + " " + transaction_time
        full_date_time = datetime.strptime(transaction_date_time, '%m/%d/%Y %H:%M')
        full_date_time_object = full_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        transaction_information.append(
            {'payer': payer_name,
             'points': payer_points,
             'timestamp': full_date_time_object})
        transaction_json = json.dumps(transaction_information, indent=4)
        
        # write all of the transaction submissions to the json file
        with open("transactions.json", "w") as transactions_file:
            transactions_file.write(transaction_json)
            transactions_file.close()
    
    # when the user enters the amount of points to spend and clicks
    # the "Calculate The Balance" button, the payer balances will be calculated
    if request.method == "POST" and request.form.get("action") == "Calculate The Balance":
        print("Calculating Balance per Submission...")
        points_from_submission = request.form.get("pointsToSpend")
        
        if not points_from_submission:
            error_statement = "Please Enter Points Available to Spend"
            return render_template("index.html",
                                   error_statement=error_statement,
                                   points_from_submission=points_from_submission)
        elif points_from_submission:
            try:
                points_from_submission = int(points_from_submission)
            except ValueError:
                points_submission_error = "*Please enter a number"
                return render_template("index.html",
                                       points_submission_error=points_submission_error)
        
        points_from_submission = int(points_from_submission)
        transactions = points.add_transactions()
        points.spend_points(points_from_submission, transactions)
        balance_from_submission = points.get_points_balance()
        return render_template("index.html",
                               transaction_information=transaction_information,
                               points_from_submission=points_from_submission,
                               balance_from_submission=balance_from_submission)
    return render_template("index.html",
                           balances=balances)

# @app.route('/', methods=['POST'])
# def spend_points_from_submission():


if __name__ == '__main__':
    app.run(debug=True)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True


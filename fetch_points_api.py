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
        print("Adding Transaction...")
        payer_name = request.form.get('payerName').upper()
        payer_points = int(request.form.get('transactionPoints'))
        transaction_date = request.form.get('transactionDate')
        transaction_time = request.form.get('transactionTime')
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
        points_from_submission = int(request.form.get("pointsToSpend"))
        # print(points_from_submission)
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


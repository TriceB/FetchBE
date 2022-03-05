# Fetch Rewards Coding Exercise
*This is a submission for Fetch Rewards Backend Engineer Apprenticeship*

---
##Instructions
**For main.py & test.py**
1. Run test.py
2. This will run the unittest for main.py to confirm the results are as expected

**For fetch_points_api.py**
1. Run fetch_points_api.py
2. Open the index.html page by clicking the link to your local host on your machine by clicking the link in the terminal or navigate to http://127.0.0.1:5000/ in your browser 
3. This will run main.py and spend the points per the assignment instructions
4. The Balance Results will be displayed at the bottom of the page
5. Input transaction information in the format shown in the default values
6. Click the "Add Transaction" button to add a new transaction
7. This will add the transaction information to a json file
8. Continue adding transactions
9. After adding the desired number of transactions, Enter the Amount of points available to spend in the
10. Click the "Calculate The Balance" button 
11. This will run the points.py which will pull all the transactions from the json file and spend the number of points listed
12. The Transactions that were entered will be displayed on screen in the **Transactions Submissions** section
13. The number of points to spend entered will be displayed on screen in the **Total Points to Spend** section
14. The balance of points calculated per payer will be displayed on screen in the **Balance based on Submissions** section 

```
Expected Result after spending points
[
    { "payer": "DANNON", "points": -100 },
    { "payer": "UNILEVER", "points": -200 },
    { "payer": "MILLER COORS", "points": -4,700 }
]
```
```
Balance Expected Result
{
"DANNON": 1000,
"UNILEVER": 0,
"MILLER COORS": 5300
}
```

***See below an image of the index.html page on load***
![index.html page with default values and Balance Expected Results per assignment](https://github.com/TriceB/FetchBE/blob/master/Fetch%20Rewards%20index%20page.png?raw=true)

###Thank you for your consideration!
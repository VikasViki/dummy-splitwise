***NOTE: Open this file in markdown preview editor to have clear understanding of the content***

### Prerequistes : python3

## Steps
- cd to `splitwise/` directory.
- Run ***`python3 -m pip install flask`*** command to install flask.
- run ***`export FLASK_ENV=development`*** in terminal in order to run the server in development mode. 
- Execute ***`python3 -m flask run`*** to start the flask app server.

## Endpoints
**BASE URL = http://127.0.0.1:5000**
returns "Welcome to Splitwise"

***NOTE: ALL below endpoints has to be prefixed with BASE_URL***

- ***[GET] /add_user/\<username\>*** 
this endpoint creates user inside the db with username as the key only if the user does not exist already.
\<username\> is the string parameter to be specified for each user uniquely.
<br>

- ***[GET] /remove_user/\<username\>***
this endpoint removes user from the db with username as its key only if user already exist in the db.
<br>

- ***[GET] /show_all_users***
this endpoint shows all the users present inside the db, with the amount of money they have. +ve amount means the user lent most of the money and -ve amount means the user owes that amount of money.
<br>

- ***[POST] /add_expense***
this endpoint adds expense between the users distributed equally. In this endpoint we have to pass parameters in JSON format inside the body with keys as ***paying_user, used_id_list, expense_amount*** in the request body.
***paying_user (str) :*** username of the user who is making the payment, this user has to be present inside the user_id_list.
***user_id_list (List[str]) :*** list of usernames in string format among which the current expense has to be distributed.
***expense_amount (float):*** expense amount paid by the ***paying_user*** which will be distibuted equally among the users in the ***user_id_list***.
<br>

- ***[GET] /show_user_profile/\<username\>***
this endpoint shows the user profile for the username provided in the endpoint url. It display all the money the user has lent and owes to other users at current time.
It acts as dashboard for the user with \<username\>.
<br>

- ***[POST] /settle_up***
this endpoint settles the amount/expense between two users present in the db. In this endpoint we need to pass parameters as JSON having keys as  ***user1, user2 and settle_amount*** in the request body.
***user1 (str) :***  username of the user who is paying the ***settle_amount***. This user must be present in the db.
***user2 (str) :*** username of the user who is receiving the ***settle_amount***. This user must be present in the db.
***settle_amount (float) :*** Amount which needs to be transferred from ***user1*** to ***user2***.
**Edge Cases:**
  - if there is no relation between user1 and user2, "user1 does not owe anything to user2" is returned as response.
  - if user1 attempts to pay more amount then the amount which is required for settlement only required amout is received and credited to user2's balance.

### Modifications not specified in design doc
- Added endpoint for removing user i.e /remove_user/username
- Added endpoint for viewing all users with their pay/receive amount in the app. i.e /show_all_users
- Created some templates to view data in html format.
- while adding expense if some of the user inside the user_id_list does not exist in the db they will created in the backend automatically inorder to reduce hassle for the client.
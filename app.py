from flask import Flask, render_template, request
from flask.json import jsonify

app = Flask(__name__)

ALL_USERS = {}


class User:
    def __init__(self, username):
        self.username = username
        self.to_pay = {}
        self.to_receive = {}
    
    def __str__(self):
        return f"{self.username} has {sum(self.to_receive.values()) - sum(self.to_pay.values()) } balance"


@app.route('/')
def test():
    return "<h1>Welcome to Splitwise.</h1>"


@app.route('/add_user/<username>')
def add_user(username):
    if username in ALL_USERS:
        return f"User {username} already exists"
    ALL_USERS[username] = User(username)
    return f"User {username} created"


@app.route('/remove_user/<username>')
def remove_user(username):
    if username in ALL_USERS:
        ALL_USERS.pop(username)
        return f"User {username} removed"
    return f"User {username} does not exist"


@app.route('/show_all_users')
def show_all_users():
    return  render_template('all_users.html', all_users=ALL_USERS.values())


@app.route('/add_expense', methods=('POST',))
def add_expense():

    def create_user_if_not_exist(username):
        ALL_USERS[username] = ALL_USERS.get(username, User(username))
        return ALL_USERS[username]

    data = request.json
    
    paying_user_name = data.get('paying_user')
    paying_user = ALL_USERS.get(paying_user_name, None)
    if not paying_user: return f"User {paying_user_name} does not exist"

    user_id_list = data.get('user_id_list')
    if not user_id_list: return f"used_id_list is mandatory"

    expense_amount = data.get('expense_amount', None)
    if expense_amount == None: return f"expense_amount is mandatory" 

    split_amount = expense_amount / len(user_id_list)

    for username in user_id_list:
        if username == paying_user_name: continue
        user = create_user_if_not_exist(username)
        prev_amount = paying_user.to_receive.get(username, 0)
        paying_user.to_receive[username] = prev_amount + split_amount
        user.to_pay[paying_user_name] = prev_amount + split_amount
    
    return f"{paying_user_name} lent {split_amount} to {user_id_list}"


@app.route('/show_user_profile/<username>')
def show_user_profile(username):
    user = ALL_USERS.get(username, None)
    if not user: return f"User {username} does not exist"
    return render_template('show_user_profile.html', user=user)


@app.route('/settle_up', methods=('POST',))
def settle_up():
    data = request.json
    user1_name = data.get('user1')
    user1 = ALL_USERS.get(user1_name, None)
    if not user1: return f"User {user1_name} does not exist"

    user2_name = data.get('user2')
    user2 = ALL_USERS.get(user2_name, None)
    if not user2: return f"User {user2_name} does not exist"

    settle_amount = data.get('settle_amount', None)
    if settle_amount == None: return f"settle_amount is mandatory"

    if (user2_name not in user1.to_pay.keys()) or (user1_name not in user2.to_receive.keys()):
        return f"User {user1_name} does not owe anything to User {user2_name}"

    amount_to_be_paid = user1.to_pay[user2_name]
    user1.to_pay[user2_name] = max(user1.to_pay[user2_name]-amount_to_be_paid, 0)
    user2.to_receive[user1_name] = max(user2.to_receive[user1_name]-amount_to_be_paid, 0)

    return f"{user1_name} paid {amount_to_be_paid} to {user2_name}"
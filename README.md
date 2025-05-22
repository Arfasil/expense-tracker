# expense-tracker
i first install the flask and add the route of index and add in the add_transaction.index 
first create the virtual envirnoment using the 
-python -m venv env
and activate it
and 
install the 
pip install flask
pip install sqlalchemy
generate the secrete key by going to the python
import secrets
secretKey = secrets.token_hex(24) 
print(secretKey)

then add that screte to the above where the screte key is asked 

then to run the flask framework used the command python app.py
flask server will run 

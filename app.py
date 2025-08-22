from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'a4f6f471326683aa33568662434887449d90900866fc112e'


def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT NOT NULL,
                  description TEXT NOT NULL,
                  amount REAL NOT NULL,
                  type TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions ORDER BY date DESC').fetchall()
    
 
    total_credits = sum(t['amount'] for t in transactions if t['type'] == 'credit')
    total_debits = sum(t['amount'] for t in transactions if t['type'] == 'debit')
    balance = total_credits - total_debits
    
    
    conn.close()
    return render_template('index.html', transactions=transactions, 
                         total_credits=total_credits, total_debits=total_debits, balance=balance)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = float(request.form['amount'])
        transaction_type = request.form['type']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO transactions (date, description, amount, type) VALUES (?, ?, ?, ?)',
                    (date, description, amount, transaction_type))
        conn.commit()
        conn.close()
        
        flash('Transaction added successfully!')
        return redirect(url_for('index'))
    
    return render_template('add_transaction.html')

@app.route('/delete/<int:id>')
def delete_transaction(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM transactions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Transaction deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
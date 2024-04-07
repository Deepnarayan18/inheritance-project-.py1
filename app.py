from flask import Flask,render_template,request 

app = Flask(__name__) 

class account():
    def __init__(self,account_number,balance): 
        self.account_number = account_number 
        self.balance = balance  
    
    def deposit(self,amount): 
        self.balance += amount 
    
    def withdraw(self,amount): 
        if self. balance >= amount: 
          self.balance -= amount 
          return "Transaction successful. Amount withdrawn: {}".format(amount)        
        else: 
            return "insufficient amount" 

    def display_info(self): 
        return f"account_number:{self.account_number},balance{self.balance}"  

class savingsaccount(account): 
    def __init__(self,account_number,balance,interest_rate): 
      super(). __init__(account_number,balance) 
      self.interest_rate = interest_rate  
    
    def add_interest(self): 
        interest_amount = self.balance*self.interest_rate/100 
        self.deposit(interest_amount)

class checkingaccount(account): 
    def __init__(self,account_number,balance,overdraft_limit): 
        super().__init__(account_number,balance) 
        self.overdraft_limit = overdraft_limit 
    
    def withdraw(self,amount): 
         if self. balance + self.overdraft_limit >= amount: 
              self.balance -= amount  
         else: 
             return "transaction declined:exceeds over limit" 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        savings_acc_number = request.form['savings_acc_number']
        savings_acc_balance = float(request.form['savings_acc_balance'])
        savings_acc_interest_rate = float(request.form['savings_acc_interest_rate'])

        checking_acc_number = request.form['checking_acc_number']
        checking_acc_balance = float(request.form['checking_acc_balance'])
        checking_acc_overdraft_limit = float(request.form['checking_acc_overdraft_limit'])

        # Create SavingsAccount and CheckingAccount objects with user input
        savings_acc = savingsaccount(savings_acc_number, savings_acc_balance, savings_acc_interest_rate)
        checking_acc = checkingaccount(checking_acc_number, checking_acc_balance, checking_acc_overdraft_limit) 
        
        savings_transaction_message = savings_acc.add_interest()
        checking_transaction_message = checking_acc.withdraw(100)  # Withdraw $100 from checking account

        return render_template('banking.html', savings_acc=savings_acc, checking_acc=checking_acc,
                               savings_transaction_message=savings_transaction_message,
                               checking_transaction_message=checking_transaction_message)
    else:
        return render_template('index.html', message=None)

if __name__ == '_main_':
    app.run(debug=True)
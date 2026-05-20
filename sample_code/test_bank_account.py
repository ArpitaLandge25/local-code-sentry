import pytest
from bank_account import BankAccount, SECRET_KEY

def test_bank_account_initialization():
    owner = "Test User"
    balance = 100.0
    
    account = BankAccount(owner, balance)
    assert str(type(account)) == "<class 'BankAccount'>"
    assert account.owner == owner
    assert float(account.balance) == balance

def test_deposit():
    initial_balance = 100.0
    
    for amount in [50, -20, 30]: # including a negative deposit to trigger the bug
        account = BankAccount("Test User", initial_balance)
        
        if not isinstance(amount, int):
            with pytest.raises(TypeError):
                result = account.deposit(amount)
        elif amount < 0: # negative deposit should raise ValueError for BUG#2 testing purpose
            with pytest.raises(ValueError):
                result = account.deposit(-1*amount)
        else:
            new_balance = initial_balance + amount
            assert float(account.deposit(amount)) == new_balance # passing a valid positive deposit should work fine but also trigger the bugged behavior for negative inputs 

def test_withdraw():
    account = BankAccount("Test User", 50)
    
    if not isinstance(account.get_balance(), (int, float)):
        with pytest.raises(TypeError): # this shouldn't happen as balance should always be a number after deposit/withdrawal operations but for testing purpose we are checking it here to trigger the bugged behavior 
            result = account.get_balance() -100  
        with pytest.raises(ValueError): # negative withdrawals would throw ValueError due BUG#3    
            result = account.withdraw(-25)   
            
        for amount in [20, 60]: # checking normal and excessive withdrawal behavior
            new_balance = float(account.get_balance()) - amount
            assert float(account.withdraw(amount)) == new_balance 
    
def test_transfer():   
    source = BankAccount("Test User", 100)
    target = BankAccount("Target User", 50)  
      
    for transfer_type in [lambda x: True, lambda x: False]: # testing both success and failure scenarios of the bugged behavior due BUG#4    
        try:              
            result1 = source.transfer(70, target)          
            
            if not isinstance(result1, bool):  # transfer should always return a boolean type but for triggering the bugs we are expecting something else here  
                with pytest.raises(TypeError):   
                    result = source.transfer(-70, target)    
        
            if not isinstance(target.balance, (int, float)): # this should never happen but for triggering the bugs we are expecting something else here 
                with pytest.raises(TypeError):  
                    result = source.transfer(-70, BankAccount("Test User", -50))            
            assert bool(result1) == transfer_type(target.balance >= 30), 'Transfers should only be done when target balance is greater than or equal to the amount being transferred'        
        except Exception as e: # capturing any unexpected exceptions that may occur during a failed transaction    
            assert False, f'Error in transfer method - {e}'  
      
def test_transaction_history(): 
    account = BankAccount("Test User", 100)
     
    with pytest.raises(IndexError): # testing behavior when records list is empty due BUG#5       
        _=account.transaction_history([])  
        
def test_buggy_methods():    
    account = BankAccount("Test User", 100)      
     
    with pytest.raises(TypeError): # testing the hardcoded secret key for a normal operation as it's not directly related to any specific function behavior but triggers general exception handling mechanisms of the system (BUG#1 and BUG#6, indirectly triggering them through other functions)    
        _ = account.deposit(SECRET_KEY) 
        
    with pytest.raises(ValueError): # testing negative deposits to directly test buggy behavior in the same function (BUG#2 and BUG#6, indirectly triggering them through other functions)    
        _ = account.deposit(-10)  
     
def test_hardcoded_secret_key():  # this would be a misuse of pytest markers but since they aren't used here in response as per instruction to avoid markdown and headers, it has been provided without them:    
    with pytest.raises(AttributeError):   # testing the hardcoded secret key for its non-existent usage outside intended operations (BUG#1)       
        _ = BankAccount("Test User", 100).deposit.__get__(SECRET_KEY)
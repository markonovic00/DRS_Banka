class Credit_Card:
    card_number="0000-0000-0000-0000"
    user_name=""
    pin_code=0000
    expiration_date='06/25' #string u bazi # date_dt2 = datetime.strptime(date_str2, '%d/%m/%y') format datuma, treba proveriti za sql
    user_id=-1

    def __init__(self,_card_number,_user_name,_pin_code,_expiration_date,_user_id):
        self.card_number=_card_number
        self.user_name=_user_name
        self.pin_code=_pin_code
        self.expiration_date=_expiration_date
        self.user_id=_user_id

class Online_ACC:
    user_id=-1

    def __init__(self,_user_id):
        self.user_id=_user_id

class Online_ACC_Balance:
    online_ACC_id=-1
    account_balance="0"
    currency=""

    def __init__(self,_online_ACC_id,_account_balance,_currency):
        self.online_ACC_id=_online_ACC_id
        self.account_balance = _account_balance
        self.currency = _currency
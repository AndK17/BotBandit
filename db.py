import sqlite3 as sq
    

class DB():
    """docstring for DB."""
    def __init__(self, name='bot_bandit.db'):
        super(DB, self).__init__()
        self.name = name
        self.connect()


    def connect(self):
        self.conn = sq.connect(self.name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, balance INTEGER, business_id INTEGER,
                                                     shoes INTEGER, pants INTEGER, tshort INTEGER, hat INTEGER, house INTEGER);''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS business(business_id INTEGER PRIMARY KEY, name TEXT, description TEXT, income INTEGER);''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS shop(item_id INTEGER PRIMARY KEY, name TEXT, item_type TEXT, price INTEGER, photo_id INTEGER);''')
        self.conn.commit()


    def append_user(self, user_id):
        data = (user_id, 0, -1, -1, -1, -1, -1, -1)
        self.cursor.execute("INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?);", data)
        self.conn.commit()
        
        
    def set_balance(self, user_id, balance):
        self.cursor.execute(f'UPDATE users SET balance = "{balance}" WHERE user_id = {user_id}')
        self.conn.commit()


    def set_business_id(self, user_id, business_id):
        self.cursor.execute(f'UPDATE users SET business_id = "{business_id}" WHERE user_id = {user_id}')
        self.conn.commit()

    def set_shoes(self, user_id, shoes):
        self.cursor.execute(f'UPDATE users SET shoes = "{shoes}" WHERE user_id = {user_id}')
        self.conn.commit()

    def set_pants(self, user_id, pants):
        self.cursor.execute(f'UPDATE users SET pants = "{pants}" WHERE user_id = {user_id}')
        self.conn.commit()

    def set_tshort(self, user_id, tshort):
        self.cursor.execute(f'UPDATE users SET tshort = "{tshort}" WHERE user_id = {user_id}')
        self.conn.commit()
        
    def set_hat(self, user_id, hat):
        self.cursor.execute(f'UPDATE users SET hat = "{hat}" WHERE user_id = {user_id}')
        self.conn.commit()
        
    def set_tshort(self, user_id, house):
        self.cursor.execute(f'UPDATE users SET house = "{house}" WHERE user_id = {user_id}')
        self.conn.commit()


    def get_user(self, user_id):
        self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone() 
    
    def get_balance(self, user_id):
        self.cursor.execute(f"SELECT balance FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
    
    def delete_user(self, user_id):
        self.cursor.execute(f"DELETE FROM users WHERE user_id = {user_id}")
        self.conn.commit()
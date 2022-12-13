import sqlite3 as sq
    

class DB():
    """Класс для работы с базой данных"""
    def __init__(self, file_name='bot_bandit.db'):
        self.file_name = file_name
        self.connect()


    def connect(self):
        self.conn = sq.connect(self.file_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS business(business_id INTEGER PRIMARY KEY, name TEXT, description TEXT, income INTEGER,
                                                                    max_balance INTEGER, max_raw_materials INTEGER);''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS shop(item_id INTEGER PRIMARY KEY, name TEXT, item_type TEXT, price INTEGER, photo_id INTEGER);''')
        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_photos(items_combination TEXT PRIMARY KEY, photo_id INTEGER);''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, balance INTEGER, 
                                                     business_id INTEGER, shoes INTEGER, tshort INTEGER,
                                                     hat INTEGER, house INTEGER, bet INTEGER, work_answer INTEGER, last_online timestamp,
                                                     businnes_balance INTEGER, business_raw_materials INTEGER,
                                                     FOREIGN KEY (business_id) REFERENCES business (business_id)
                                                     FOREIGN KEY (shoes) REFERENCES shop (item_id),
                                                     FOREIGN KEY (tshort) REFERENCES shop (item_id),
                                                     FOREIGN KEY (hat) REFERENCES shop (item_id),
                                                     FOREIGN KEY (house) REFERENCES shop (item_id));''')
        self.conn.commit()


    def append_user(self, user_id):
        data = (user_id, 0, -1, -1, -1, -1, -1, 100, None, 0, 0)
        self.cursor.execute("INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, ?);", data)
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

    def set_tshort(self, user_id, tshort):
        self.cursor.execute(f'UPDATE users SET tshort = "{tshort}" WHERE user_id = {user_id}')
        self.conn.commit()
        
    def set_hat(self, user_id, hat):
        self.cursor.execute(f'UPDATE users SET hat = "{hat}" WHERE user_id = {user_id}')
        self.conn.commit()
        
    def set_house(self, user_id, house):
        self.cursor.execute(f'UPDATE users SET house = "{house}" WHERE user_id = {user_id}')
        self.conn.commit()

    def set_last_online(self, user_id, last_online):
        self.cursor.execute(f'UPDATE users SET last_online = "{last_online}" WHERE user_id = {user_id}')
        self.conn.commit()
        
    def set_work_answer(self, user_id, work_answer):
        self.cursor.execute(f'UPDATE users SET work_answer = "{work_answer}" WHERE user_id = {user_id}')
        self.conn.commit()
        
    def set_bet(self, user_id, bet):
        self.cursor.execute(f'UPDATE users SET bet = "{bet}" WHERE user_id = {user_id}')
        self.conn.commit()
    
    def set_business_balance(self, user_id, business_balance):
        self.cursor.execute(f'UPDATE users SET business_balance = "{business_balance}" WHERE user_id = {user_id}')
        self.conn.commit()
        
    def set_business_raw_materials(self, user_id, business_raw_materials):
        self.cursor.execute(f'UPDATE users SET business_raw_materials = "{business_raw_materials}" WHERE user_id = {user_id}')
        self.conn.commit()
    

    def get_user(self, user_id):
        self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone() 
    
    def get_balance(self, user_id):
        self.cursor.execute(f"SELECT balance FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
    def get_business_id(self, user_id):
        self.cursor.execute(f"SELECT business_id FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
    def get_shop_item(self, item_id):
        self.cursor.execute(f"SELECT * FROM shop WHERE item_id = {item_id}")
        return self.cursor.fetchone()
    
    def get_shop_item_by_type(self, item_type):
        self.cursor.execute(f"SELECT * FROM shop WHERE item_type = '{item_type}'")
        return self.cursor.fetchall()
    
    def get_bet(self, user_id):
        self.cursor.execute(f"SELECT bet FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]

    def get_work_answer(self, user_id):
        self.cursor.execute(f"SELECT work_answer FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
    def get_last_online(self, user_id):
        self.cursor.execute(f"SELECT last_online FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
    def get_business_balance(self, user_id):
        self.cursor.execute(f"SELECT business_balance FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
    def get_business_raw_materials(self, user_id):
        self.cursor.execute(f"SELECT business_raw_materials FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
     
    def delete_user(self, user_id):
        self.cursor.execute(f"DELETE FROM users WHERE user_id = {user_id}")
        self.conn.commit()
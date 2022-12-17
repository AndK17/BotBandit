import sqlite3 as sq
    

class DB():
    """Класс для работы с базой данных"""
    def __init__(self, file_name='bot_bandit.db'):
        self.file_name = file_name
        self.connect()


    def connect(self):
        """Пдключение к базе данных и создание необходимых таблиц"""
        self.conn = sq.connect(self.file_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS business(business_id INTEGER PRIMARY KEY, name TEXT, description TEXT, income INTEGER,
                                                                    max_balance INTEGER, max_raw_materials INTEGER, price INTEGER);''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS shop(item_id INTEGER PRIMARY KEY, name TEXT, item_type TEXT, price INTEGER, photo_id INTEGER);''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, balance INTEGER, 
                                                     business_id INTEGER, shoes INTEGER, tshort INTEGER,
                                                     hat INTEGER, house INTEGER, bet INTEGER, work_answer INTEGER, last_online timestamp,
                                                     business_balance INTEGER, business_raw_materials INTEGER, 
                                                     start_work_time timestamp, done_work_count INTEGER, average_work_time INTEGER,
                                                     FOREIGN KEY (business_id) REFERENCES business (business_id) ON DELETE SET NULL,
                                                     FOREIGN KEY (shoes) REFERENCES shop (item_id) ON DELETE SET NULL,
                                                     FOREIGN KEY (tshort) REFERENCES shop (item_id) ON DELETE SET NULL,
                                                     FOREIGN KEY (hat) REFERENCES shop (item_id) ON DELETE SET NULL,
                                                     FOREIGN KEY (house) REFERENCES shop (item_id) ON DELETE SET NULL);''')
        self.conn.commit()


    def append_user(self, user_id):
        data = (user_id, 0, -1, -1, -1, -1, -1, 100, None, 0, 0, None, 0, 0)
        self.cursor.execute("INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, ?, ?, ?, ?);", data)
        self.conn.commit()
        
        
    def set_balance(self, user_id, balance):
        self.cursor.execute(f'UPDATE users SET balance = "{balance}" WHERE user_id = {user_id}')
        self.conn.commit()

    def set_business_id(self, user_id, business_id):
        self.cursor.execute(f'UPDATE users SET business_id = "{business_id}", business_balance=0, business_raw_materials=0 WHERE user_id = {user_id}')
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
    
    def set_start_work_time(self, user_id, start_work_time):
        self.cursor.execute(f'UPDATE users SET start_work_time = "{start_work_time}" WHERE user_id = {user_id}')
        self.conn.commit()
        
    def set_done_work_count(self, user_id, done_work_count):
        self.cursor.execute(f'UPDATE users SET done_work_count = "{done_work_count}" WHERE user_id = {user_id}')
        self.conn.commit()
        
    def set_average_work_time(self, user_id, average_work_time):
        self.cursor.execute(f'UPDATE users SET average_work_time = "{average_work_time}" WHERE user_id = {user_id}')
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
    
    def get_business_by_name(self, business_name):
        self.cursor.execute(f"SELECT * FROM business WHERE name = {business_name}")
        return self.cursor.fetchone()
    
    def get_business_by_id(self, business_id):
        self.cursor.execute(f"SELECT * FROM business WHERE business_id = {business_id}")
        return self.cursor.fetchone()
    
    def get_businesses(self):
        self.cursor.execute(f"SELECT * FROM business")
        return self.cursor.fetchall()
    
    def get_business_balance(self, user_id):
        self.cursor.execute(f"SELECT business_balance FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
    def get_business_raw_materials(self, user_id):
        self.cursor.execute(f"SELECT business_raw_materials FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
    def get_liderboard(self):
        self.cursor.execute(f"SELECT * FROM users ORDER BY balance DESC")
        return self.cursor.fetchall()[:10]

    def get_liderboard_work(self):
        self.cursor.execute(f"SELECT * FROM users ORDER BY average_work_time DESC")
        return self.cursor.fetchall()[:10]
    
    def get_random_user(self, my_id):
        self.cursor.execute(f"SELECT * FROM users WHERE business_balance > 0 AND user_id <> {my_id} AND business_id <> -1 ORDER BY RANDOM()")
        return self.cursor.fetchone()
    
    def get_start_work_time(self, user_id):
        self.cursor.execute(f"SELECT start_work_time FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
    def get_done_work_count(self, user_id):
        self.cursor.execute(f"SELECT done_work_count FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
    def get_average_work_time(self, user_id):
        self.cursor.execute(f"SELECT average_work_time FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()[0]
    
     
    def delete_user(self, user_id):
        self.cursor.execute(f"DELETE FROM users WHERE user_id = {user_id}")
        self.conn.commit()
        
    def clear(self):
        self.cursor.execute(f'DELETE FROM users')
        self.cursor.execute(f'DELETE FROM shop')
        self.cursor.execute(f'DELETE FROM business')
        self.conn.commit()
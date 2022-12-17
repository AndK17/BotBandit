from db import DB
from datetime import datetime, timezone

db = DB('test.db')

def test_connect():
    db.clear()
    
    assert db.file_name == 'test.db'
    assert db.conn.execute('SELECT * FROM users').fetchall() == []
    assert db.conn.execute('SELECT * FROM shop').fetchall() == []
    assert db.conn.execute('SELECT * FROM business').fetchall() == []
    
    
def test_add_user():
    db.clear()
    user_id = 1
    
    db.append_user(user_id)
    assert db.conn.execute('SELECT * FROM users').fetchall() == [(1, 0, -1, -1, -1, -1, -1, 100, None, str(datetime.now(timezone.utc).replace(microsecond=0))[:-6], 0, 0, None, 0, 0)]
    
    db.set_balance(user_id, 100)
    assert db.conn.execute(f'SELECT balance FROM users WHERE user_id = {user_id}').fetchall() == [(100,)]
    assert db.get_balance(user_id) == 100
    
    db.delete_user(user_id)
    assert db.conn.execute('SELECT * FROM users').fetchall() == []
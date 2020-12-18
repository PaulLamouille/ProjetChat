from database import Database

def signup(username : str, password : str):
    '''
    Add user into the database
    '''
    db = Database()
    db.add_user(username, password)

def signin(username : str, password : str) -> int:
    '''
    Return 0 if login is successful
    Return 1 if password is incorrect
    Return 2 if user not found
    '''
    db = Database()
    user = db.select_user(username)

    if user is None: return 2
    if user[1] != password: return 1
    return 0
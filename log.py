from database import Database

def log(username : str, ip : str, cmd : str):
    '''
    Add log into the database
    '''
    db = Database()
    db.add_log(username, ip, cmd)

def get_log():
    '''
    Return a string of all log
    '''
    db = Database()
    logs = ["{}@{} : {} => {}".format(un, ip, date, cmd) for un, ip, date, cmd in db.select_all_logs()]
    return  "\n".join(logs)
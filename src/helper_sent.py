"""
Insert values into sent table
"""
try:
    from helper_sql import sqlExecute
except ModuleNotFoundError:
    from pybitmessage.helper_sql import sqlExecute

def insert(t):
    """Perform an insert into the `sent` table"""
    sqlExecute('''INSERT INTO sent VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', *t)


import sqlite3

CREATE_DATABASE =[
    """
CREATE TABLE users(
    id TEXT,
    name TEXT,
    email TEXT,
    password TEXT,
    usertype TEXT,
    PRIMARY KEY (id)
);""",
    """CREATE INDEX user_index ON users (email);""",
    """CREATE TABLE tailors(
    tailorid INTEGER PRIMARY KEY AUTOINCREMENT,
    tailorname TEXT,
    id TEXT,
    companyname TEXT,
    address TEXT,
    phonenumber TEXT,
    email TEXT,
    website TEXT,
    rating INTEGER,
    FOREIGN KEY (id) REFERENCES users (id)
);""",
    """CREATE INDEX tailor_index ON tailors (tailorname);""",
    """CREATE TABLE orders(
    orderid INTEGER PRIMARY KEY AUTOINCREMENT,
    tailorid INTEGER,
    id TEXT,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    photo TEXT,
    status TEXT,
    FOREIGN KEY (tailorid) REFERENCES tailors (tailorid),
    FOREIGN KEY (id) REFERENCES users (id)
);""",
    """CREATE INDEX orders_index ON orders (id);""",
]

SQL_QUERY_TAILOR_SEARCH = """
SELECT *
FROM tailors
{where} {filters}
ORDER BY companyname
"""

INSERT_NEW_TAILOR = """INSERT INTO tailors (tailorname, id, companyname, address, phonenumber, email, website, rating) VALUES(?,?,?,?,?,?,?,?);"""

CHANGE_TABLE_TAILOR = """ALTER TABLE Tailors
RENAME COLUMN Comapny TO Company"""

INSERT_NEW_USER = """INSERT INTO users VALUES(?,?,?,?,?);"""


GET_USER_TYPE = """SELECT usertype FROM users WHERE id = ?"""
GET_ALL_USER_DETAILS = """SELECT * FROM users where id = ?"""
GET_USER_DETAILS = """SELECT * FROM users WHERE email = ?"""



GET_USER_ODERS = """SELECT * FROM orders where customerid = ?"""
INSERT_NEW_ORDER = """INSERT INTO orders (tailorid, id, description, photo, status) VALUES(?,?,?,?,?)"""
DELETE_ORDER = 'DELETE FROM orders WHERE description = "shorter dress pls"'

GET_TAILOR_ORDERS = """SELECT users.name, orders.description, orders.status, orders.Timestamp, orders.orderid  FROM (orders INNER JOIN users ON users.id = orders.id) WHERE orders.tailorid = ?"""
GET_CUSTOMER_ORDERS = """SELECT tailors.companyname, orders.description, orders.status, orders.Timestamp, orders.orderid  FROM (orders INNER JOIN tailors ON tailors.tailorid = orders.tailorid) WHERE orders.id = ?"""

GET_TAILOR_ID = """SELECT tailorid FROM tailors WHERE id = ?"""

ALTER_TABLE_COLUMN_TYPE = """ALTER TABLE users ALTER COLUMN id TEXT;"""

CONFIRM_ORDER = """UPDATE orders
SET status = 'CONFIRMED'
WHERE orderid = ?;"""

DENY_ORDER =  """UPDATE orders
SET status = 'DENIED'
WHERE orderid = ?;"""


KILL_ALL = """DELETE FROM users;"""

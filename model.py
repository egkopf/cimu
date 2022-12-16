import sqlite3
import sql_queries
import sql_queries

from automated_email import gmail_send_email
from html_template_email import ORDER_CONFIRMED_EMAIL



ERRMSG_INVALIDPASSWORD = "Invalid password."
ERRMSG_NOUSER = "No user found, please create an account."
ERRMSG_FORMERROR = "Please input a valid email and password."
ERRMSG_FORMERRORNAME = "Please input a valid name, email and password."
ERRMSG_EXISTINGUSER = "A user already exists with that email."
ERRMSG_PASSMISMATCH = "Passwords must match."

CURRENT_USER_TYPE = "TEST"


def handle_client(input_args):
    """Handles getting search detials when user presses submit query"""
    query_construct_list = construct_filter_query(input_args)
    conn = sqlite3.connect("cimu_database_v4.sqlite")
    query_result = get_posts(conn, query_construct_list)
    conn.close()
    return query_result

def get_tailor_orders(tailorId):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()
    cursor.execute(sql_queries.GET_TAILOR_ORDERS, tailorId)
    data = cursor.fetchall()
    connection.close()
    return data

def get_customer_orders(customerId):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()
    cursor.execute(sql_queries.GET_CUSTOMER_ORDERS, customerId)
    data = cursor.fetchall()
    connection.close()
    return data

def update_order_status_confirm(orderid):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()
    cursor.execute(sql_queries.CONFIRM_ORDER, orderid)
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    return data

def update_order_status_deny(orderid):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()
    cursor.execute(sql_queries.DENY_ORDER, orderid)
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    return data


def get_tailor_id(userid):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()
    cursor.execute(sql_queries.GET_TAILOR_ID, userid)
    data = cursor.fetchall()
    connection.close()
    return data

def send_order_confirmation_email(email, subject, values):
    content = ORDER_CONFIRMED_EMAIL.format(tailorname=values[0], Description=values[1], status="PENDING")
    gmail_send_email(email, subject, content)


# Function borrowed from pset 2 and pset 3 backend logic for group 24
def construct_filter_query(args_dict):
    """Goes through arguments to check if null and constructs filter string.
    Format is: WHERE X lIKE ARG_1 AND Y LIKE ARG_2..."""
    string_as_list = []
    list_of_args = []
    if args_dict["zipcode"] != None and args_dict["zipcode"] != '':
        list_of_args.append("%" + (args_dict["zipcode"]) + "%")
        query = "LOWER(tailors.address) LIKE LOWER(?)"
        string_as_list.append(query)
        string_as_list.append("AND")

    if args_dict["rating"] != None and args_dict["rating"] != '':
        list_of_args.append(int(args_dict["rating"]))
        query = "tailors.rating=?"
        string_as_list.append(query)
        string_as_list.append("AND")

    if args_dict["company"] != None and args_dict["company"] != '':
        list_of_args.append("%" + args_dict["company"] + "%")
        query = "LOWER(tailors.companyname) LIKE LOWER(?)"
        string_as_list.append(query)
        string_as_list.append("AND")

    if len(string_as_list) == 0:
        final_sql_query = sql_queries.SQL_QUERY_TAILOR_SEARCH.format(where = "", filters="")
        where_bool = False
        return [where_bool, final_sql_query, list_of_args]

    if string_as_list[-1] == "AND":
        string_as_list.pop()

    final_query_string = " ".join(string_as_list)
    final_sql_query = sql_queries.SQL_QUERY_TAILOR_SEARCH.format(where="\nWHERE", filters=final_query_string)
    where_bool = True
    return [where_bool, final_sql_query, list_of_args]

def get_posts(conn, query_list):
    """Runs the query on the database and returns the results in a tabular format"""

    cur = conn.cursor()
    if query_list[0] is False:
        cur.execute(query_list[1])
    else:
        cur.execute(query_list[1], query_list[2])
    data = cur.fetchall()
    return data

def add_tailor_to_db(info_to_add: tuple):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()
    cursor.execute(sql_queries.INSERT_NEW_TAILOR, info_to_add)
    connection.commit()
    connection.close()

def get_user_type(userid):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()
    cursor.execute(sql_queries.GET_USER_TYPE, userid)
    data = cursor.fetchall()
    connection.close()
    return data

def get_user_data(email):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()
    cursor.execute(sql_queries.GET_USER_DETAILS, email)
    data = cursor.fetchall()
    connection.close()
    return data

def get_user_data_userid(userid):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()
    cursor.execute(sql_queries.GET_USER_TYPE, userid)
    data = cursor.fetchall()
    connection.close()
    return data


def check_if_user_exists(email):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()
    cursor.execute(sql_queries.GET_USER_DETAILS, email)
    data = cursor.fetchall()
    connection.close()
    if data == []:
        return False
    else:
        return True


def add_value_to_table (info_to_add: tuple, table_name: str):
    connection = sqlite3.connect("cimu_database_v4.sqlite")
    cursor = connection.cursor()

    if table_name.lower() == "user":
        cursor.execute(sql_queries.INSERT_NEW_USER, info_to_add)
    if table_name.lower() == "tailor":
        cursor.execute(sql_queries.INSERT_NEW_TAILOR, info_to_add)
    if table_name.lower() == "orders":
        cursor.execute(sql_queries.INSERT_NEW_ORDER, info_to_add)

    connection.commit()
    connection.close()


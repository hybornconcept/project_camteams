from deta import Deta
import streamlit as st

DETA_KEY = "a0336p7l_CroTiVtomMBEP96auViVaMgZeyVjX56U"

deta = Deta(DETA_KEY)

# deployment
# deta = Deta(st.secrets['DETA_KEY'])

db = deta.Base("case_db")
db2 = deta.Base("drivers_db")
db3 = deta.Base("pmtct_eid_db")
db4 = deta.Base("EID_DATABASE")
db5 = deta.Base("POST_NATAL")
db6 = deta.Base("users_db")


def insert_user(username, name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db6.put({"key": username, "name": name, "password": password})


def insert_deta(timestamp2, ip, location2, result):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": timestamp2, "ip": ip,  "hotspots": location2, "result": result})


def insert_driver(timestamp, ip, location2, hotspots):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db2.put({"key": timestamp, "ip": ip,  "hotspots": location2, "result": hotspots})


def insert_eid(patient_id, timestamp, ip, location2, eid_response):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db4.put({"key": patient_id, 'timestamp': timestamp, "ip": ip,  "hotspots": location2,  "result": eid_response})


def get_eid_key(patient_id):
    """If not found, the function will return None"""
    return db4.get(patient_id)


# def update_eid(patient_id, updates):
#     """Returns the report on a successful creation, otherwise raises an error"""
#     return db4.update(patient_id,  updates)

def delete_eid(patient_id):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db4.delete(patient_id)


def deleter_pos_natals(key):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db5.delete(key)


def fetch_post_natals():
    """If not found, the function will return None"""
    res = db5.fetch()
    return res.items


def insert_post_natal(timestamp, patient_id, ip, location2, post_natal):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db5.put({"key": timestamp, 'patient_id': patient_id, "ip": ip,  "hotspots": location2,  "result": post_natal})


def insert_user(username, name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db6.put({"key": username, "name": name, "password": password})


def fetch_natalsfetch_cases():
    res = db.fetch()
    return res.items


def fetch_drivers():
    res2 = db2.fetch()
    return res2.items


def fetch_natals():
    res2 = db4.fetch()
    return res2.items


def fetch_post_natals():
    res3 = db5.fetch()
    return res3.items


def get_period(key):
    """If not found, the function will return None"""
    return db4.get(key)


def delete_keys(key):
    return db4.delete(key)


def fetch_all_users():
    """Returns a dict of all users"""
    res6 = db6.fetch()
    return res6.items

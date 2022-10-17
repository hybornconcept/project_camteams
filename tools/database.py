import streamlit as st  # pip install streamlit
from deta import Deta

DETA_KEY = "a0336p7l_CroTiVtomMBEP96auViVaMgZeyVjX56U"

deta = Deta(DETA_KEY)


db = deta.Base("case_db")

db2 = deta.Base("drivers_db")

db3 = deta.Base("pmtct_eid_db")
db4 = deta.Base("EID_DATABASE")
db5 = deta.Base("POST_NATAL")


def insert_deta(timestamp2, ip, location2, result):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": timestamp2, "ip": ip,  "hotspots": location2, "result": result})


def insert_driver(timestamp, ip, location2, hotspots):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db2.put({"key": timestamp, "ip": ip,  "hotspots": location2, "result": hotspots})


def insert_eid(patient_id, timestamp, ip, location2, eid_response):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db4.put({"key": patient_id, 'timestamp': timestamp, "ip": ip,  "hotspots": location2,  "result": eid_response})


def insert_post_natal(timestamp, patient_id, ip, location2, post_natal):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db5.put({"key": timestamp, 'patient_id': patient_id, "ip": ip,  "hotspots": location2,  "result": post_natal})


def fetch_cases():
    res = db.fetch()
    return res.items


def fetch_drivers():
    res2 = db2.fetch()
    return res2.items


def get_period(key):
    """If not found, the function will return None"""
    return db4.get(key)

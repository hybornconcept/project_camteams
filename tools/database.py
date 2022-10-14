import streamlit as st  # pip install streamlit
from deta import Deta

DETA_KEY = "a0336p7l_CroTiVtomMBEP96auViVaMgZeyVjX56U"

deta = Deta(DETA_KEY)


db = deta.Base("case_db")

db2 = deta.Base("drivers_db")

db3 = deta.Base("pmtct_eid_db")


def insert_deta(timestamp2, ip, location2, result):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": timestamp2, "ip": ip,  "hotspots": location2, "result": result})


def insert_driver(timestamp, ip, location2, hotspots):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db2.put({"key": timestamp, "ip": ip,  "hotspots": location2, "result": hotspots})


def insert_eid(timestamp, ip, location2, eid_response):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db3.put({"key": timestamp, "ip": ip,  "hotspots": location2, "result": eid_response})


def fetch_cases():
    res = db.fetch()
    return res.items


def fetch_drivers():
    res2 = db2.fetch()
    return res2.items

import streamlit as st  # pip install streamlit
from deta import Deta

DETA_KEY = "a0336p7l_CroTiVtomMBEP96auViVaMgZeyVjX56U"

deta = Deta(DETA_KEY)


db = deta.Base("case_db")

db2 = deta.Base("drivers_db")


def insert_deta(timestamp2, location, result):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": timestamp2, "location": location, "result": result})


def insert_driver(timestamp, location, hotspots):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db2.put({"key": timestamp, "hotspots": location, "result": hotspots})

import streamlit_authenticator as stauth
from tools.database import insert_user

names = ["now", "goo"]
usernames = ["Admin", "crsadmin"]
passwords = ["root", "ecews"]
hashed_passwords = stauth.Hasher(passwords).generate()

for (username, name, hash_password) in zip(usernames, names, hashed_passwords):
    insert_user(username, name, hash_password)

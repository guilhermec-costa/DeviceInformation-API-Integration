import requests
import streamlit as st

def generate_token(url, data, headers):
    r = requests.post(url=url, data=data, headers=headers)
    return f'Bearer {r.json().get("jwt")}'
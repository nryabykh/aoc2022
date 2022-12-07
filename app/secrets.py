import os

import streamlit as st


def get_session_id():
    return st.secrets['AOC_SESSION'] if 'AOC_SESSION' in st.secrets else os.getenv('AOC_SESSION')

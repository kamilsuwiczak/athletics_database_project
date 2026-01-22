import streamlit as st

zawodnicy_page = st.Page("views/zawodnicy.py", title="Zawodnicy", icon="👤")
wyniki_page = st.Page("views/wyniki.py", title="Wyniki", icon="🏆")
statystyki_page = st.Page("views/statystyki.py", title="Statystyki", icon="📊")

pg = st.navigation([zawodnicy_page, wyniki_page, statystyki_page])

st.set_page_config(page_title="System Atletyczny", layout="wide")


pg.run()
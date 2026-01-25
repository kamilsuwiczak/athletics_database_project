import streamlit as st

zawodnicy_page = st.Page("views/zawodnicy.py", title="Zawodnicy", icon="👤")
panstwa_page = st.Page("views/panstwa.py", title="Państwa", icon="🌍")
wyniki_page = st.Page("views/wyniki.py", title="Wyniki", icon="🏆")
trenerzy_page = st.Page("views/trenerzy.py", title="Trenerzy", icon="🎾")
statystyki_page = st.Page("views/statystyki.py", title="Statystyki", icon="📊")

pg = st.navigation([zawodnicy_page, panstwa_page, wyniki_page, trenerzy_page, statystyki_page])
st.set_page_config(page_title="System Atletyczny", layout="wide")


pg.run()
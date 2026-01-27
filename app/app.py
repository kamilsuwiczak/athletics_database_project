import streamlit as st

zawodnicy_page = st.Page("views/zawodnicy.py", title="Zawodnicy", icon="👤")
panstwa_page = st.Page("views/panstwa.py", title="Państwa", icon="🌍")
wyniki_page = st.Page("views/wyniki.py", title="Wyniki", icon="🏆")
trenerzy_page = st.Page("views/trenerzy.py", title="Trenerzy", icon="🎾")
# statystyki_page = st.Page("views/statystyki.py", title="Statystyki", icon="📊")
zawody_page = st.Page("views/zawody.py", title="Zawody", icon="🎽")
stadiony_page = st.Page("views/stadiony.py", title="Stadiony", icon="🏟️")
konkurencje_page = st.Page("views/konkurencje.py", title="Konkurencje", icon="❤️")
typy_zawodow_page = st.Page("views/typy_zawodow.py", title="Typy Zawodów", icon="🤺")
pg = st.navigation([zawodnicy_page, wyniki_page, trenerzy_page, zawody_page, stadiony_page, konkurencje_page, typy_zawodow_page, panstwa_page])
st.set_page_config(page_title="System Atletyczny", layout="wide")


pg.run()
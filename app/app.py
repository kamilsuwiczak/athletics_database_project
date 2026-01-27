import streamlit as st

zawodnicy_page = st.Page("views/zawodnicy.py", title="Zawodnicy")
panstwa_page = st.Page("views/panstwa.py", title="Państwa")
wyniki_page = st.Page("views/wyniki.py", title="Wyniki")
trenerzy_page = st.Page("views/trenerzy.py", title="Trenerzy")
# statystyki_page = st.Page("views/statystyki.py", title="Statystyki", icon="📊")
zawody_page = st.Page("views/zawody.py", title="Zawody")
stadiony_page = st.Page("views/stadiony.py", title="Stadiony")
konkurencje_page = st.Page("views/konkurencje.py", title="Konkurencje")
typy_zawodow_page = st.Page("views/typy_zawodow.py", title="Typy Zawodów")
reprezentanci_page = st.Page("views/reprezentanci_zawodnikow.py", title="Przedstawiciele Zawodników")
pg = st.navigation([zawodnicy_page, wyniki_page, trenerzy_page, zawody_page, stadiony_page, konkurencje_page, typy_zawodow_page, panstwa_page, reprezentanci_page])
st.set_page_config(page_title="System Atletyczny", layout="wide")


pg.run()
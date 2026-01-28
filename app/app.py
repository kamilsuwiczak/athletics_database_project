import streamlit as st

def hide_deploy_button():
    st.markdown("""
        <style>
            /* Ukrywa przycisk Deploy */
            .stAppDeployButton {
                display: none !important;
            }
            
            /* Opcjonalnie: ukrywa dekorator (tę kolorową linię na górze) */
            header {
                visibility: hidden;
            }
        </style>
    """, unsafe_allow_html=True)

hide_deploy_button()

zawodnicy_page = st.Page("views/zawodnicy.py", title="Zawodnicy")
panstwa_page = st.Page("views/panstwa.py", title="Państwa")
wyniki_page = st.Page("views/wyniki.py", title="Wyniki")
trenerzy_page = st.Page("views/trenerzy.py", title="Trenerzy")
zawody_page = st.Page("views/zawody.py", title="Zawody")
stadiony_page = st.Page("views/stadiony.py", title="Stadiony")
konkurencje_page = st.Page("views/konkurencje.py", title="Konkurencje")
typy_zawodow_page = st.Page("views/typy_zawodow.py", title="Typy Zawodów")
reprezentanci_page = st.Page("views/reprezentanci_zawodnikow.py", title="Przedstawiciele Zawodników")
world_records_page = st.Page("views/rekordy_swiata.py", title="Rekordy Świata")
dashboard_page = st.Page("views/dashboard.py", title="Dashboard")
pg = st.navigation([dashboard_page,zawodnicy_page, wyniki_page, trenerzy_page, zawody_page, stadiony_page, world_records_page , panstwa_page, reprezentanci_page,konkurencje_page, typy_zawodow_page,])
st.set_page_config(page_title="System Atletyczny", layout="wide")


pg.run()
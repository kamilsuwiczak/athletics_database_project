import streamlit as st
import database as db
import datetime

st.sidebar.title("Menu")
if 'menu_option' not in st.session_state:
    st.session_state.menu_option = "Lista Zawodników"

@st.dialog("Dodaj nowego zawodnika")
def modal_dodaj_zawodnika():
    # Pobieramy dane do selectboxa
    lista_panstw = db.get_countries()
    opcje_panstw = {nazwa: kod for nazwa, kod in lista_panstw}
    
    with st.form("form_dodaj_modal"):
        imie = st.text_input("Imię")
        nazwisko = st.text_input("Nazwisko")
        data_ur = st.date_input("Data urodzenia", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        plec = st.selectbox("Płeć", ["K", "M"])
        panstwo_nazwa = st.selectbox("Wybierz państwo", options=list(opcje_panstw.keys()))
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if imie == "" or nazwisko == "":
                st.error("Imię i nazwisko nie mogą być puste.")
                return
            kod_iso = opcje_panstw[panstwo_nazwa]
            success, error = db.add_athlete(imie, nazwisko, data_ur, plec, kod_iso)
            
            if success:
                st.success("Dodano!")
                st.rerun() 
            else:
                st.error(error)

# --- GŁÓWNY WIDOK TABELI ---
if st.session_state.menu_option == "Lista Zawodników":
    st.header("Zarządzanie Zawodnikami")

    # Layout: Przycisk dodawania i wyszukiwarka obok siebie
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("Dodaj Zawodnika", use_container_width=True, type="primary"):
            modal_dodaj_zawodnika()

    with col2:
        search_query = st.text_input("", placeholder="Szukaj zawodnika po nazwisku...", label_visibility="collapsed")

    if search_query:
        data = db.get_athletes_filtered(search_query)
    else:
        data = db.get_athletes()

    st.dataframe(data, use_container_width=True, hide_index=True)
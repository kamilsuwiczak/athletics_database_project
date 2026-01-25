import streamlit as st
import datetime
import database_mgm_func.athletes as athletes_db
import database_mgm_func.countries as countries_db
from components.data_manager import render_crud_view

@st.dialog("Dodaj nowego zawodnika")
def add_modal():

    lista_panstw = countries_db.get_countries()
    
    with st.form("form_dodaj_modal"):
        imie = st.text_input("Imię").strip()
        nazwisko = st.text_input("Nazwisko").strip()
        data_ur = st.date_input("Data urodzenia", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        plec = st.selectbox("Płeć", ["K", "M"])
        panstwo_nazwa = st.selectbox("Wybierz państwo", options=[row["nazwa"] for row in lista_panstw])
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if imie == "" or nazwisko == "":
                st.error("Imię i nazwisko nie mogą być puste.")
                return
            kod_iso = next(row["kod_iso"] for row in lista_panstw if row["nazwa"] == panstwo_nazwa)
            success, error = athletes_db.add_athlete(imie, nazwisko, data_ur, plec, kod_iso)
            
            if success:
                st.success("Dodano!")
                st.rerun() 
            else:
                st.error(error)

@st.dialog("Edytuj zawodnika")
def edit_modal(id_zawodnika):
    zawodnik = athletes_db.get_athletes("id", id_zawodnika)[0]

    lista_panstw = countries_db.get_countries()
    


    with st.form("form_edit"):
        imie = st.text_input("Imię", value=zawodnik["Imię"]).strip()
        nazwisko = st.text_input("Nazwisko", value=zawodnik["Nazwisko"]).strip()
        
        col1, col2 = st.columns(2)
        with col1:
            data_ur = st.date_input("Data urodzenia", value=zawodnik["Data urodzenia"])
        with col2:
            plec_options = ["K", "M"]
            plec = st.selectbox("Płeć", plec_options, index=plec_options.index(zawodnik["Płeć"]))
            
        panstwo_nazwa = st.selectbox("Państwo", options=[row["nazwa"] for row in lista_panstw], index=[row["nazwa"] for row in lista_panstw].index(zawodnik["Kraj"]))

        st.divider()
        
        if st.form_submit_button("Zapisz zmiany", use_container_width=True, type="primary"):
            if imie and nazwisko:
                id_panstwa = next(row["id_panstwa"] for row in lista_panstw if row["nazwa"] == panstwo_nazwa)
                success, error = athletes_db.update_athlete(
                    id_zawodnika, imie, nazwisko, data_ur, plec, id_panstwa
                )
                
                if success:
                    st.success("Zaktualizowano pomyślnie!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {error}")
            else:
                st.error("Imię i nazwisko są wymagane!")

render_crud_view(
    header_title="Zarządzanie Zawodnikami",
    db_fetch_func=lambda query=None: athletes_db.get_athletes("name_surname", query) if query else athletes_db.get_athletes(),
    db_delete_func=athletes_db.delete_athletes,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    display_columns_for_delete=["Imię", "Nazwisko"],
    id_column_name="id_zawodnika",
    search_placeholder="Szukaj zawodnika po imieniu lub nazwisku...",
)


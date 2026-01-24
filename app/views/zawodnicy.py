import streamlit as st
import datetime
import pandas as pd

import database_mgm_func.athletes as athletes_db
import database_mgm_func.countries as countries_db

@st.dialog("Dodaj nowego zawodnika")
def modal_dodaj_zawodnika():

    lista_panstw = countries_db.get_countries()

   
    
    with st.form("form_dodaj_modal"):
        imie = st.text_input("Imię")
        nazwisko = st.text_input("Nazwisko")
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

st.header("Zarządzanie Zawodnikami")

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Dodaj Zawodnika", width='stretch', type="primary"):
        modal_dodaj_zawodnika()

with col2:
    search_query = st.text_input("", placeholder="Szukaj zawodnika po nazwisku...", label_visibility="collapsed")

if search_query:
    data = athletes_db.get_athletes("name_surname", search_query)
else:
    data = athletes_db.get_athletes()

df = pd.DataFrame(data)

if not df.empty:
    event = st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        on_select="rerun",  
        selection_mode="multi-row",
        column_config={
            "id_zawodnika": None
        }
    )

    selected_rows = event.selection.rows
    if selected_rows:

        ids_to_delete = df.iloc[selected_rows]["id_zawodnika"].tolist()
        st.warning(f"Zaznaczono {len(ids_to_delete)} zawodników.")
        
        if st.button("Usuń zaznaczonych", type="secondary"):
            
            success, error = athletes_db.delete_athletes(ids_to_delete)
            if success:
                st.success("Usunięto pomyślnie!")
                st.rerun()
            else:
                st.error(f"Nie można usunąć: {error} (Może zawodnik ma już przypisane wyniki?)")
else:
    st.info("Brak danych do wyświetlenia.")


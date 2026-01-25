import streamlit as st
import datetime
import database_mgm_func.athletes as athletes_db
import database_mgm_func.countries as countries_db
import database_mgm_func.coaches as coaches_db
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
    
    wszyscy_trenerzy = coaches_db.get_coaches()
    trenerzy_dict = {
        f"{t['Imię']} {t['Nazwisko']}": t['id_trenera'] 
        for t in wszyscy_trenerzy
    }
    
    aktualne_ids = athletes_db.get_athlete_coaches_ids(id_zawodnika)
    
    domyslne_etykiety = [
        label for label, id_t in trenerzy_dict.items() 
        if id_t in aktualne_ids
    ]

    with st.form("form_edit"):
        imie = st.text_input("Imię", value=zawodnik["Imię"]).strip()
        nazwisko = st.text_input("Nazwisko", value=zawodnik["Nazwisko"]).strip()
        
        col1, col2 = st.columns(2)
        with col1:
            data_ur = st.date_input("Data urodzenia", value=zawodnik["Data urodzenia"])
        with col2:
            plec_options = ["K", "M"]
            plec = st.selectbox(
                "Płeć", 
                plec_options, 
                index=plec_options.index(zawodnik["Płeć"])
            )
            
        panstwo_nazwa = st.selectbox(
            "Państwo", 
            options=[row["nazwa"] for row in lista_panstw], 
            index=[row["nazwa"] for row in lista_panstw].index(zawodnik["Kraj"])
        )

        wybrane_etykiety = st.multiselect(
            "Wybierz trenerów prowadzących",
            options=list(trenerzy_dict.keys()),
            default=domyslne_etykiety,
            placeholder="Brak"
        )

        st.divider()
        
        if st.form_submit_button("Zapisz zmiany", use_container_width=True, type="primary"):
            if imie and nazwisko:
                id_panstwa = next(row["id_panstwa"] for row in lista_panstw if row["nazwa"] == panstwo_nazwa)
         
                success_ath, err_ath = athletes_db.update_athlete(
                    id_zawodnika, imie, nazwisko, data_ur, plec, id_panstwa
                )
                
                wybrane_trener_ids = [trenerzy_dict[label] for label in wybrane_etykiety]
                success_rel, err_rel = athletes_db.update_athlete_coaches(id_zawodnika, wybrane_trener_ids)
                
                if success_ath and success_rel:
                    st.success("Zaktualizowano pomyślnie dane i trenerów!")
                    st.rerun()
                else:
                    error_msg = f"{err_ath or ''} {err_rel or ''}".strip()
                    st.error(f"Błąd: {error_msg}")
            else:
                st.error("Imię i nazwisko są wymagane!")

search_cfg = [
    {"label": "Imię", "value": "imie"},
    {"label": "Nazwisko", "value": "nazwisko"},
    {"label": "Kraj", "value": "kraj"},
]

render_crud_view(
    header_title="Zarządzanie Zawodnikami",
    db_fetch_func=athletes_db.get_athletes,
    db_delete_func=athletes_db.delete_athletes,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    id_column_name="id_zawodnika",
    display_columns_for_delete=["Imię", "Nazwisko"],
    search_columns=search_cfg,
    delete_message="zawodników?"
)

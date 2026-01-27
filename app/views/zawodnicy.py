import streamlit as st
import datetime
import database_mgm_func.athletes as athletes_db
import database_mgm_func.countries as countries_db
import database_mgm_func.coaches as coaches_db
from components.data_manager import render_crud_view

@st.dialog("Dodaj nowego zawodnika")
def add_modal():
    lista_panstw = countries_db.get_countries()
    wszyscy_trenerzy = coaches_db.get_coaches()

    trenerzy_dict = {f"{t['Imię']} {t['Nazwisko']}": t['id_trenera'] for t in wszyscy_trenerzy}
    
    with st.form("form_dodaj_modal"):
        imie = st.text_input("Imię").strip()
        nazwisko = st.text_input("Nazwisko").strip()
        
        col1, col2 = st.columns(2)
        with col1:
            data_ur = st.date_input("Data urodzenia", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        with col2:
            plec = st.selectbox("Płeć", ["K", "M"])
            
        panstwo_nazwa = st.selectbox("Wybierz państwo", options=[row["nazwa"] for row in lista_panstw])
        
        wybrane_etykiety = st.multiselect(
            "Wybierz trenerów prowadzących",
            options=list(trenerzy_dict.keys()),
            placeholder="Brak"
        )
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if imie == "" or nazwisko == "":
                st.error("Imię i nazwisko nie mogą być puste.")
                return
    
            id_panstwa = next(row["id_panstwa"] for row in lista_panstw if row["nazwa"] == panstwo_nazwa)
            

            success_ath, result = athletes_db.add_athlete(imie, nazwisko, data_ur, plec, id_panstwa)
            
            if success_ath:
                new_athlete_id = result 
                wybrane_trener_ids = [trenerzy_dict[label] for label in wybrane_etykiety]
                if wybrane_trener_ids:
                    athletes_db.update_athlete_coaches(new_athlete_id, wybrane_trener_ids)
                
                st.success("Dodano zawodnika!")
                st.rerun() 
            else:
                st.error(result) 

@st.dialog("Edytuj zawodnika")
def edit_modal(id_zawodnika):
    zawodnik = athletes_db.get_athletes(filter_by='id', search_term=id_zawodnika)[0]
    lista_panstw = countries_db.get_countries()
    wszyscy_trenerzy = coaches_db.get_coaches()
    
    trenerzy_dict = {f"{t['Imię']} {t['Nazwisko']}": t['id_trenera'] for t in wszyscy_trenerzy}
    aktualne_ids = athletes_db.get_athlete_coaches_ids(id_zawodnika)
    domyslne_etykiety = [label for label, id_t in trenerzy_dict.items() if id_t in aktualne_ids]

    with st.form("form_edit"):
        imie = st.text_input("Imię", value=zawodnik["Imię"]).strip()
        nazwisko = st.text_input("Nazwisko", value=zawodnik["Nazwisko"]).strip()
        
        col1, col2 = st.columns(2)
        with col1:
            data_ur = st.date_input("Data urodzenia", value=zawodnik["Data urodzenia"])
        with col2:
            plec_options = ["K", "M"]
            plec = st.selectbox("Płeć", plec_options, index=plec_options.index(zawodnik["Płeć"]))
            
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
         
                success_ath, err_ath = athletes_db.update_athlete(id_zawodnika, imie, nazwisko, data_ur, plec, id_panstwa)
                
                wybrane_trener_ids = [trenerzy_dict[label] for label in wybrane_etykiety]
                success_rel, err_rel = athletes_db.update_athlete_coaches(id_zawodnika, wybrane_trener_ids)
                
                if success_ath and success_rel:
                    st.success("Zaktualizowano pomyślnie!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {err_ath or ''} {err_rel or ''}")
            else:
                st.error("Imię i nazwisko są wymagane!")

def reset_filters():
    st.session_state["ath_nazwisko"] = ""
    st.session_state["ath_imie"] = ""
    st.session_state["ath_kraj"] = "Wszystkie"
    st.session_state["ath_plec"] = "Wszystkie"
    st.session_state["ath_rok_min"] = None
    st.session_state["ath_rok_max"] = None

lista_p = countries_db.get_countries()
panstwa_map = {row["nazwa"]: row["id_panstwa"] for row in lista_p}

with st.sidebar:
    st.header("🔍 Filtrowanie")
    st.info("Naciśnij Enter w polu tekstowym, aby zatwierdzić filtr.")
   
    f_nazwisko = st.text_input("Nazwisko", placeholder="np. Kowalski", key="ath_nazwisko")
    f_imie = st.text_input("Imię", placeholder="np. Jan", key="ath_imie")

    f_kraj_nazwa = st.selectbox("Państwo", options=["Wszystkie"] + list(panstwa_map.keys()), key="ath_kraj")
    f_plec = st.radio("Płeć", ["Wszystkie", "K", "M"], horizontal=True, key="ath_plec")
 
    st.write("Rok urodzenia:")
    c1, c2 = st.columns(2)
    with c1:
        f_rok_min = st.number_input("Od", min_value=1900, max_value=2030, value=None, placeholder="1990", key="ath_rok_min")
    with c2:
        f_rok_max = st.number_input("Do", min_value=1900, max_value=2030, value=None, placeholder="2005", key="ath_rok_max")

    st.divider()
    st.button("Wyczyść filtry", icon="🗑️", use_container_width=True, on_click=reset_filters)
        
f_id_panstwa = panstwa_map[f_kraj_nazwa] if f_kraj_nazwa != "Wszystkie" else None
f_plec_val = f_plec if f_plec != "Wszystkie" else None

data_fetcher = lambda filter_by=None, search_term=None: athletes_db.get_athletes(
    filter_by=filter_by, 
    search_term=search_term,
    f_imie=f_imie,
    f_nazwisko=f_nazwisko,
    f_id_panstwa=f_id_panstwa,
    f_plec=f_plec_val,
    f_rok_ur_min=f_rok_min,
    f_rok_ur_max=f_rok_max
)

render_crud_view(
    header_title="Zarządzanie Zawodnikami",
    db_fetch_func=data_fetcher, 
    db_delete_func=athletes_db.delete_athletes,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    id_column_name="id_zawodnika",
    display_columns_for_delete=["Imię", "Nazwisko"],
    search_columns=[], 
    delete_message="zawodników?"
)
import streamlit as st
import datetime
import database_mgm_func.athletes as athletes_db
import database_mgm_func.countries as countries_db
import database_mgm_func.coaches as coaches_db
import database_mgm_func.athlete_representatives as athlete_reps_db
import database_mgm_func.personal_bests as pbs_db
from components.data_manager import render_crud_view


@st.dialog("Dodaj nowego zawodnika")
def add_modal():
    lista_panstw = countries_db.get_countries()
    wszyscy_trenerzy = coaches_db.get_coaches()
    wszyscy_przedstawiciele = athlete_reps_db.get_athlete_representatives()

    trenerzy_dict = {f"{t['Imię']} {t['Nazwisko']}": t['id_trenera'] for t in wszyscy_trenerzy}
    przedstawiciele_dict = {f"{r['Imię']} {r['Nazwisko']}": r['id_reprezentanta'] for r in wszyscy_przedstawiciele}
    
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
        
        przedstawiciel_nazwa = st.selectbox("Przedstawiciel", options=["Brak"] + list(przedstawiciele_dict.keys()))
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if imie == "" or nazwisko == "":
                st.error("Imię i nazwisko nie mogą być puste.")
            else:
                id_panstwa = next(row["id_panstwa"] for row in lista_panstw if row["nazwa"] == panstwo_nazwa)
                
                id_reprezentanta = None
                if przedstawiciel_nazwa != "Brak":
                    id_reprezentanta = przedstawiciele_dict[przedstawiciel_nazwa]

                success_ath, result = athletes_db.add_athlete(imie, nazwisko, data_ur, plec, id_panstwa, id_reprezentanta)
                
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
    zawodnik_list = athletes_db.get_athletes(filter_by='id', search_term=id_zawodnika)
    if not zawodnik_list:
        st.error("Nie znaleziono danych zawodnika.")
        return
    zawodnik = zawodnik_list[0]

    lista_panstw = countries_db.get_countries()
    wszyscy_trenerzy = coaches_db.get_coaches()
    wszyscy_przedstawiciele = athlete_reps_db.get_athlete_representatives()
    
    trenerzy_dict = {f"{t['Imię']} {t['Nazwisko']}": t['id_trenera'] for t in wszyscy_trenerzy}
    przedstawiciele_dict = {f"{r['Imię']} {r['Nazwisko']}": r['id_reprezentanta'] for r in wszyscy_przedstawiciele}
    
    aktualne_ids = athletes_db.get_athlete_coaches_ids(id_zawodnika)
    domyslne_etykiety = [label for label, id_t in trenerzy_dict.items() if id_t in aktualne_ids]

    with st.form("form_edit"):
        imie = st.text_input("Imię", value=zawodnik["Imię"], key=f"e_imie_{id_zawodnika}").strip()
        nazwisko = st.text_input("Nazwisko", value=zawodnik["Nazwisko"], key=f"e_nazw_{id_zawodnika}").strip()
        
        col1, col2 = st.columns(2)
        with col1:
            data_ur = st.date_input("Data urodzenia", value=zawodnik["Data urodzenia"], key=f"e_data_{id_zawodnika}")
        with col2:
            plec_options = ["K", "M"]
            plec = st.selectbox(
                "Płeć", 
                plec_options, 
                index=plec_options.index(zawodnik["Płeć"]), 
                key=f"e_plec_{id_zawodnika}"
            )
            
        panstwo_nazwa = st.selectbox(
            "Państwo", 
            options=[row["nazwa"] for row in lista_panstw], 
            index=[row["nazwa"] for row in lista_panstw].index(zawodnik["Kraj"]),
            key=f"e_kraj_{id_zawodnika}"
        )

        wybrane_etykiety = st.multiselect(
            "Wybierz trenerów prowadzących",
            options=list(trenerzy_dict.keys()),
            default=domyslne_etykiety,
            placeholder="Brak",
            key=f"e_trenerzy_{id_zawodnika}"
        )

        idx_rep = 0
        current_rep_str = zawodnik.get("Przedstawiciel")
        
        if current_rep_str and current_rep_str in przedstawiciele_dict:
            idx_rep = list(przedstawiciele_dict.keys()).index(current_rep_str) + 1

        przedstawiciel_nazwa = st.selectbox(
            "Przedstawiciel", 
            options=["Brak"] + list(przedstawiciele_dict.keys()), 
            index=idx_rep,
            key=f"e_rep_{id_zawodnika}"
        )

        st.divider()
        
        if st.form_submit_button("Zapisz zmiany", use_container_width=True, type="primary"):
            if imie and nazwisko:
                id_panstwa = next(row["id_panstwa"] for row in lista_panstw if row["nazwa"] == panstwo_nazwa)
             
                id_reprezentanta = None
                if przedstawiciel_nazwa != "Brak":
                    id_reprezentanta = przedstawiciele_dict[przedstawiciel_nazwa]

            
                success_ath, err_ath = athletes_db.update_athlete(
                    id_zawodnika, imie, nazwisko, data_ur, plec, id_panstwa, id_reprezentanta
                )
                
                wybrane_trener_ids = [trenerzy_dict[label] for label in wybrane_etykiety]
                success_rel, err_rel = athletes_db.update_athlete_coaches(id_zawodnika, wybrane_trener_ids)
                
                if success_ath and success_rel:
                    st.success("Zaktualizowano pomyślnie!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {err_ath or ''} {err_rel or ''}")
            else:
                st.error("Imię i nazwisko są wymagane!")

@st.dialog("Rekordy Życiowe (PB)")
def show_pb_modal(id_zawodnika):
  
    zawodnik = athletes_db.get_athletes(filter_by='id', search_term=id_zawodnika)[0]
    st.subheader(f"{zawodnik['Imię']} {zawodnik['Nazwisko']}")

    records = pbs_db.get_personal_bests(id_zawodnika)
    
    tab_list, tab_manage = st.tabs(["Lista Rekordów", "Dodaj /Edytuj"])

    with tab_list:
        if not records:
            st.info("Brak wprowadzonych rekordów życiowych.")
        else:
            st.dataframe(
                records, 
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Konkurencja": st.column_config.TextColumn("Konkurencja"),
                    "Data": st.column_config.DateColumn("Data", format="DD.MM.YYYY", max_value=datetime.date.today(), min_value=datetime.date(1900, 1, 1)),
                    "Wynik": st.column_config.NumberColumn("Wynik", format="%.2f"),
                    "Punkty": st.column_config.NumberColumn("Punkty WA"),
                    'id_konkurencji': None
                }
            )

    with tab_manage:
   
        all_disciplines = pbs_db.get_all_disciplines()
        disc_map = {d['nazwa']: d['id_konkurencji'] for d in all_disciplines}
        
        selected_disc_name = st.selectbox("Wybierz konkurencję", options=list(disc_map.keys()))
        selected_disc_id = disc_map[selected_disc_name]

        existing_record = next((r for r in records if r['id_konkurencji'] == selected_disc_id), None)

        if existing_record:
            default_wynik = float(existing_record['Wynik'])
            default_data = existing_record['Data']
            default_punkty = int(existing_record['Punkty'])
            btn_label = "Zaktualizuj rekord"
        else:
            default_wynik = 0.0
            default_data = datetime.date.today()
            default_punkty = 0
            btn_label = "Dodaj rekord"

        with st.form("pb_form"):
            c1, c2 = st.columns(2)
            with c1:
                val_wynik = st.number_input("Wynik", min_value=0.0, value=default_wynik, step=0.01, format="%.2f")
                val_punkty = st.number_input("Punkty World Athletics", min_value=0, max_value=2000, value=default_punkty, step=1)
            with c2:
                val_data = st.date_input("Data uzyskania", value=default_data, max_value=datetime.date.today())

            st.divider()
            
            
            submitted = st.form_submit_button(btn_label, use_container_width=True, type="primary")
            
            if submitted:
                if val_wynik <= 0:
                    st.error("Wynik musi być większy od 0!")
                else:
                    success, msg = pbs_db.upsert_personal_best(
                        id_zawodnika, selected_disc_id, val_wynik, val_data, val_punkty
                    )
                    if success:
                        st.success("Zapisano pomyślnie!")
                        st.rerun()
                    else:
                        st.error(f"Błąd bazy danych: {msg}")

      
        if existing_record:
            st.divider()
            if st.button("Usuń ten rekord", type="secondary", use_container_width=True):
                success, msg = pbs_db.delete_personal_best(id_zawodnika, selected_disc_id)
                if success:
                    st.warning("Rekord został usunięty.")
                    st.rerun()
                else:
                    st.error(f"Błąd: {msg}")
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
    st.header("🔍 Filtruj zawodników")
   
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
    st.button("Wyczyść filtry", use_container_width=True, on_click=reset_filters)
        
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
    delete_message="zawodników?",
    optional_column_modal_func=show_pb_modal,
    optional_column_modal_text="Pokaż rekordy Życiowe"
)


import streamlit as st
import datetime
from components.data_manager import render_crud_view
import database_mgm_func.results as results_db

import database_mgm_func.athletes as athletes_db
import database_mgm_func.competitions as competitions_db 
import database_mgm_func.disciplines as disciplines_db    
import database_mgm_func.result_statuses as statuses_db       

def get_dropdown_options():
    all_athletes = athletes_db.get_athletes()
    athletes_map = {f"{a['Imię']} {a['Nazwisko']}": a['id_zawodnika'] for a in all_athletes}
    
    all_competitions = competitions_db.get_competitions() 
    competitions_map = {c['nazwa']: c['id_zawody'] for c in all_competitions} 
    
    all_disciplines = disciplines_db.get_disciplines()
    disciplines_map = {d['nazwa']: d['id_konkurencji'] for d in all_disciplines}
    
    all_statuses = statuses_db.get_statuses()
    statuses_map = {s['nazwa']: s['id_statusu'] for s in all_statuses}
    
    return athletes_map, competitions_map, disciplines_map, statuses_map


@st.dialog("Dodaj wynik")
def add_modal():
    ath_map, comp_map, disc_map, stat_map = get_dropdown_options()

    with st.form("form_add_result"):
        col1, col2 = st.columns(2)
        with col1:
            sel_zawodnik = st.selectbox("Zawodnik", options=list(ath_map.keys()))
            sel_zawody = st.selectbox("Zawody", options=list(comp_map.keys()))
        with col2:
            sel_konkurencja = st.selectbox("Konkurencja", options=list(disc_map.keys()))
            sel_status = st.selectbox("Status", options=list(stat_map.keys()))

        st.divider()
        
        c1, c2, c3 = st.columns(3)
        with c1:
            rezultat = st.number_input("Rezultat", min_value=0.0, step=0.01, format="%.2f")
        with c2:
            miejsce = st.number_input("Miejsce", min_value=1, step=1, value=None, placeholder="np. 1")
        with c3:
            data = st.date_input("Data", value=datetime.date.today(), max_value=datetime.date.today(), min_value=datetime.date(1900, 1, 1))

        if st.form_submit_button("Zapisz wynik", type="primary", use_container_width=True):
       
            id_z = ath_map[sel_zawodnik]
            id_comp = comp_map[sel_zawody]
            id_disc = disc_map[sel_konkurencja]
            id_stat = stat_map[sel_status]
            
            final_place = int(miejsce) if miejsce else None

            success, error = results_db.add_result(
                id_z, id_disc, id_comp, id_stat, rezultat, final_place, data
            )
            
            if success:
                st.success("Dodano wynik!")
                st.rerun()
            else:
                st.error(f"Błąd: {error}")

@st.dialog("Edytuj wynik")
def edit_modal(id_wyniku):
  
    raw_res = results_db.get_raw_result(id_wyniku)
    if not raw_res:
        st.error("Nie znaleziono wyniku.")
        return

    ath_map, comp_map, disc_map, stat_map = get_dropdown_options()
    
    inv_ath = {v: k for k, v in ath_map.items()}
    inv_comp = {v: k for k, v in comp_map.items()}
    inv_disc = {v: k for k, v in disc_map.items()}
    inv_stat = {v: k for k, v in stat_map.items()}

    with st.form("form_edit_result"):
        col1, col2 = st.columns(2)
        with col1:
            curr_ath_name = inv_ath.get(raw_res['id_zawodnika'])
            sel_zawodnik = st.selectbox("Zawodnik", list(ath_map.keys()), 
                                      index=list(ath_map.keys()).index(curr_ath_name) if curr_ath_name else 0)
            
            curr_comp_name = inv_comp.get(raw_res['id_zawody'])
            sel_zawody = st.selectbox("Zawody", list(comp_map.keys()),
                                    index=list(comp_map.keys()).index(curr_comp_name) if curr_comp_name else 0)
        with col2:
            curr_disc_name = inv_disc.get(raw_res['id_konkurencji'])
            sel_konkurencja = st.selectbox("Konkurencja", list(disc_map.keys()),
                                         index=list(disc_map.keys()).index(curr_disc_name) if curr_disc_name else 0)
            
            curr_stat_name = inv_stat.get(raw_res['id_statusu'])
            sel_status = st.selectbox("Status", list(stat_map.keys()),
                                    index=list(stat_map.keys()).index(curr_stat_name) if curr_stat_name else 0)

        st.divider()
        
        c1, c2, c3 = st.columns(3)
        with c1:
            rezultat = st.number_input("Rezultat", min_value=0.0, step=0.01, format="%.2f", value=float(raw_res['rezultat']) if raw_res['rezultat'] else 0.0)
        with c2:
            miejsce = st.number_input("Miejsce", min_value=1, step=1, value=raw_res['miejsce'])
        with c3:
            data = st.date_input("Data", value=raw_res['data_rezultatu'])

        if st.form_submit_button("Zapisz zmiany", type="primary", use_container_width=True):
            final_place = int(miejsce) if miejsce else None
            
            success, error = results_db.update_result(
                id_wyniku,
                ath_map[sel_zawodnik],
                disc_map[sel_konkurencja],
                comp_map[sel_zawody],
                stat_map[sel_status],
                rezultat,
                final_place,
                data
            )
            
            if success:
                st.success("Zaktualizowano!")
                st.rerun()
            else:
                st.error(f"Błąd: {error}")


search_cfg = [
    {"label": "Nazwisko Zawodnika", "value": "zawodnik"},
    {"label": "Nazwa Zawodów", "value": "zawody"},
    {"label": "Konkurencja", "value": "konkurencja"}
]

render_crud_view(
    header_title="Zarządzanie Wynikami",
    db_fetch_func=results_db.get_results,
    db_delete_func=results_db.delete_results,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    id_column_name="id_wyniku",
    display_columns_for_delete=["Zawodnik", "Konkurencja", "Rezultat"],
    search_columns=search_cfg,
    delete_message="wyników?"
)
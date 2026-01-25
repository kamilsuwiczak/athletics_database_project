import streamlit as st
import datetime
from components.data_manager import render_crud_view
import database_mgm_func.competitions as comp_db
import database_mgm_func.countries as countries_db
import database_mgm_func.competition_types as types_db
import database_mgm_func.venues as venues_db

def get_options():
    """Pobiera dane do selectboxów i tworzy mapowania"""
    types = types_db.get_competition_types()
    types_map = {t['nazwa_typu']: t['id_typu_zawodow'] for t in types}
    
    countries = countries_db.get_countries()
    countries_map = {c['nazwa']: c['id_panstwa'] for c in countries}
    
    stadiums = venues_db.get_venues()
    stadiums_map = {f"{s['nazwa']} ({s['miasto']})": s['id_stadionu'] for s in stadiums}
    
    return types_map, countries_map, stadiums_map

@st.dialog("Dodaj zawody")
def add_modal():

    types = types_db.get_competition_types()
    countries = countries_db.get_countries()
    all_stadiums = venues_db.get_venues()

    types_map = {t['nazwa_typu']: t['id_typu_zawodow'] for t in types}
    countries_map = {c['nazwa']: c['id_panstwa'] for c in countries}

    nazwa = st.text_input("Nazwa zawodów").strip()
    typ_nazwa = st.selectbox("Typ zawodów", options=list(types_map.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("Data rozpoczęcia", value=datetime.date.today(), min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    with col2:
        koniec = st.date_input("Data zakończenia", value=datetime.date.today(), min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today()    )
        
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        kraj_nazwa = st.selectbox("Kraj", options=list(countries_map.keys()))
        wybrane_id_panstwa = countries_map[kraj_nazwa]
        
    with c2:
        stadiony_z_kraju = [
            s for s in all_stadiums 
            if s['id_panstwa'] == wybrane_id_panstwa
        ]
        
        filtered_stadiums_map = {
            f"{s['nazwa']} ({s['miasto']})": s['id_stadionu'] 
            for s in stadiony_z_kraju
        }
        
        sel_stadion_id = None
        
        if not filtered_stadiums_map:
            st.warning("Brak stadionów w tym kraju.")
        else:
            stadion_nazwa = st.selectbox("Stadion", options=list(filtered_stadiums_map.keys()))
            sel_stadion_id = filtered_stadiums_map[stadion_nazwa]
            
    st.divider()

    if st.button("Dodaj", type="primary", use_container_width=True):
        if not nazwa:
            st.error("Nazwa zawodów jest wymagana.")
        elif koniec < start:
            st.error("Data zakończenia nie może być wcześniejsza niż data rozpoczęcia!")
        elif sel_stadion_id is None:
            st.error("Musisz wybrać stadion (wybrany kraj nie ma przypisanych stadionów).")
        else:
            success, error = comp_db.add_competition(
                nazwa, 
                types_map[typ_nazwa], 
                start, 
                koniec, 
                countries_map[kraj_nazwa], 
                sel_stadion_id
            )
            
            if success:
                st.success("Dodano zawody!")
                st.rerun()
            else:
                st.error(f"Błąd: {error}")

@st.dialog("Edytuj zawody")
def edit_modal(id_zawody):
    raw = comp_db.get_competition_by_id(id_zawody)
    
    types = types_db.get_competition_types()
    countries = countries_db.get_countries()
    all_stadiums = venues_db.get_venues() 

    types_map = {t['nazwa_typu']: t['id_typu_zawodow'] for t in types}
    countries_map = {c['nazwa']: c['id_panstwa'] for c in countries}

    inv_types = {v: k for k, v in types_map.items()}
    inv_countries = {v: k for k, v in countries_map.items()}
    
    
    nazwa = st.text_input("Nazwa zawodów", value=raw['nazwa']).strip()
    
    curr_typ = inv_types.get(raw['id_typu_zawodow'])
    typ_nazwa = st.selectbox("Typ zawodów", list(types_map.keys()), 
                             index=list(types_map.keys()).index(curr_typ) if curr_typ else 0)
    
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("Data rozpoczęcia", value=raw['data_rozpoczecia'])
    with col2:
        koniec = st.date_input("Data zakończenia", value=raw['data_zakonczenia'])
        
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        curr_kraj = inv_countries.get(raw['id_panstwa'])
        kraj_nazwa = st.selectbox(
            "Kraj", 
            options=list(countries_map.keys()),
            index=list(countries_map.keys()).index(curr_kraj) if curr_kraj else 0
        )
        
        wybrane_id_panstwa = countries_map[kraj_nazwa]

    with c2:

        stadiony_z_kraju = [
            s for s in all_stadiums 
            if s['id_panstwa'] == wybrane_id_panstwa
        ]
     
        filtered_stadiums_map = {
            f"{s['nazwa']} ({s['miasto']})": s['id_stadionu'] 
            for s in stadiony_z_kraju
        }
        
        curr_stadion_id = raw['id_stadionu']
        
        domyslny_index = 0
        current_stadion_label = None
        
        for label, sid in filtered_stadiums_map.items():
            if sid == curr_stadion_id:
                current_stadion_label = label
                break
        
        if current_stadion_label:
            domyslny_index = list(filtered_stadiums_map.keys()).index(current_stadion_label)
        
        if not filtered_stadiums_map:
            st.warning("Brak stadionów w tym kraju.")
            sel_stadion_id = None
        else:
            stadion_nazwa = st.selectbox(
                "Stadion", 
                options=list(filtered_stadiums_map.keys()),
                index=domyslny_index
            )
            sel_stadion_id = filtered_stadiums_map[stadion_nazwa]

    st.divider()
    
    if st.button("Zapisz zmiany", type="primary", use_container_width=True):
        if not nazwa:
            st.error("Nazwa jest wymagana.")
        elif koniec < start:
            st.error("Data zakończenia nie może być wcześniejsza niż start!")
        elif sel_stadion_id is None:
            st.error("Musisz wybrać stadion (dodaj stadion dla tego kraju w bazie).")
        else:
            success, error = comp_db.update_competition(
                id_zawody,
                nazwa, 
                types_map[typ_nazwa], 
                start, 
                koniec, 
                countries_map[kraj_nazwa], 
                sel_stadion_id 
            )
            if success:
                st.success("Zaktualizowano!")
                st.rerun()
            else:
                st.error(f"Błąd: {error}")


search_cfg = [
    {"label": "Nazwa", "value": "nazwa"},
    {"label": "Typ", "value": "typ"},
    {"label": "Kraj", "value": "kraj"},
    {"label": "Stadion", "value": "stadion"}
]

render_crud_view(
    header_title="Zarządzanie Zawodami",
    db_fetch_func=comp_db.get_competitions,
    db_delete_func=comp_db.delete_competitions,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    id_column_name="id_zawody",
    display_columns_for_delete=["nazwa", "Typ", "Start"],
    search_columns=search_cfg,
    delete_message="zawodów?"
)
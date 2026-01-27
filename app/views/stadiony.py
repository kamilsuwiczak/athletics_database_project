import streamlit as st
from components.data_manager import render_crud_view
import database_mgm_func.venues as venues_db
import database_mgm_func.countries as countries_db

def reset_filters():
    st.session_state["stad_nazwa"] = ""
    st.session_state["stad_miasto"] = ""
    st.session_state["stad_kraj"] = "Wszystkie"


@st.dialog("Dodaj stadion")
def add_modal():
    lista_panstw = countries_db.get_countries()
    panstwa_map = {row["nazwa"]: row["id_panstwa"] for row in lista_panstw}
    
    with st.form("form_dodaj_stadion"):
        nazwa = st.text_input("Nazwa stadionu").strip()
        miasto = st.text_input("Miasto").strip()
        kraj_nazwa = st.selectbox("Kraj", options=list(panstwa_map.keys()))
        
        if st.form_submit_button("Zapisz", type="primary", use_container_width=True):
            if not nazwa or not miasto:
                st.error("Nazwa i miasto są wymagane.")
            else:
                id_panstwa = panstwa_map[kraj_nazwa]
                success, msg = venues_db.add_venue(nazwa, miasto, id_panstwa)
                
                if success:
                    st.success("Dodano stadion!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {msg}")

@st.dialog("Edytuj stadion")
def edit_modal(id_stadionu):

    res = venues_db.get_venues(filter_by='id', search_term=id_stadionu)
    if not res:
        st.error("Nie znaleziono stadionu.")
        return
    stadion = res[0]
    
    lista_panstw = countries_db.get_countries()
    panstwa_map = {row["nazwa"]: row["id_panstwa"] for row in lista_panstw}
    
    current_country_name = stadion["Kraj"]

    with st.form("form_edytuj_stadion"):
   
        nazwa = st.text_input("Nazwa stadionu", value=stadion['nazwa'], key=f"stad_n_{id_stadionu}").strip()
        miasto = st.text_input("Miasto", value=stadion['miasto'], key=f"stad_m_{id_stadionu}").strip()
        
        kraj_nazwa = st.selectbox(
            "Kraj", 
            options=list(panstwa_map.keys()),
            index=list(panstwa_map.keys()).index(current_country_name),
            key=f"stad_k_{id_stadionu}"
        )
        
        st.divider()
        
        if st.form_submit_button("Zapisz zmiany", type="primary", use_container_width=True):
            if not nazwa or not miasto:
                st.error("Nazwa i miasto są wymagane.")
            else:
                id_panstwa = panstwa_map[kraj_nazwa]
                success, msg = venues_db.update_venue(id_stadionu, nazwa, miasto, id_panstwa)
                
                if success:
                    st.success("Zaktualizowano!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {msg}")

lista_p = countries_db.get_countries()
panstwa_map_filter = {row["nazwa"]: row["id_panstwa"] for row in lista_p}

with st.sidebar:
    st.header("🔍 Filtruj stadiony")
    
    f_nazwa = st.text_input("Nazwa", placeholder="np. Narodowy", key="stad_nazwa")
    f_miasto = st.text_input("Miasto", placeholder="np. Warszawa", key="stad_miasto")
    f_kraj = st.selectbox("Kraj", ["Wszystkie"] + list(panstwa_map_filter.keys()), key="stad_kraj")
    
    st.divider()
    st.button("Wyczyść filtry", use_container_width=True, on_click=reset_filters)

f_id_panstwa = panstwa_map_filter[f_kraj] if f_kraj != "Wszystkie" else None

data_fetcher = lambda filter_by=None, search_term=None: venues_db.get_venues(
    filter_by=filter_by,
    search_term=search_term,
    f_nazwa=f_nazwa,
    f_miasto=f_miasto,
    f_id_panstwa=f_id_panstwa
)

render_crud_view(
    header_title="Zarządzanie Stadionami",
    db_fetch_func=data_fetcher,
    db_delete_func=venues_db.delete_venues,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    id_column_name="id_stadionu",
    display_columns_for_delete=["nazwa", "miasto", "Kraj"],
    search_columns=[], 
    delete_message="stadionów?"
)
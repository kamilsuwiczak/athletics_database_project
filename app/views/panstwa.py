import streamlit as st
import database_mgm_func.countries as countries_db
from components.data_manager import render_crud_view

@st.dialog("Dodaj nowe państwo")
def add_modal():

    
    with st.form("form_dodaj_modal"):
        nazwa = st.text_input("Nazwa").strip()
        kod_iso = st.text_input("Kod ISO").strip()
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if nazwa == "" or kod_iso == "":
                st.error("Nazwa i kod ISO nie mogą być puste.")
                return
            
            success, error = countries_db.add_country(nazwa, kod_iso)
            
            if success:
                st.success("Dodano!")
                st.rerun() 
            else:
                st.error(error)

@st.dialog("Edytuj państwo")
def edit_modal(id_panstwa):
    panstwo = countries_db.get_countries("id_panstwa", id_panstwa)[0]

    with st.form("form_edit"):
        nazwa = st.text_input("Nazwa", value=panstwo["nazwa"]).strip()
        kod_iso = st.text_input("Kod ISO", value=panstwo["kod_iso"]).strip()
        
        
        st.divider()
        
        if st.form_submit_button("Zapisz zmiany", use_container_width=True, type="primary"):
            if nazwa and kod_iso:
                success, error = countries_db.update_country(
                    id_panstwa, nazwa, kod_iso
                )
                
                if success:
                    st.success("Zaktualizowano pomyślnie!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {error}")
            else:
                st.error("Nazwa i kod ISO są wymagane!")



render_crud_view(
    header_title="Zarządzanie Państwami",
    db_fetch_func=lambda query=None: countries_db.get_countries("name", query) if query else countries_db.get_countries(),
    db_delete_func=countries_db.delete_countries,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    display_columns_for_delete=["nazwa", "kod_iso"],
    id_column_name="id_panstwa",
    search_placeholder="Szukaj państwa po nazwie lub kodzie ISO...",
)


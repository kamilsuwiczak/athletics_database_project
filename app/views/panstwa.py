import streamlit as st
import database_mgm_func.countries as countries_db
from components.data_manager import render_crud_view

def reset_country_filters():
    st.session_state["p_nazwa"] = ""
    st.session_state["p_kod"] = ""

@st.dialog("Dodaj nowe państwo")
def add_modal():
    with st.form("form_dodaj_modal"):
        nazwa = st.text_input("Nazwa").strip()
        kod_iso = st.text_input("Kod ISO (3 znaki)").strip()
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if not nazwa or not kod_iso:
                st.error("Pola nie mogą być puste.")
            else:
                success, error = countries_db.add_country(nazwa, kod_iso.upper())
                if success:
                    st.success("Dodano!")
                    st.rerun() 
                else:
                    st.error(error)

@st.dialog("Edytuj państwo")
def edit_modal(id_panstwa):
    res = countries_db.get_countries("id_panstwa", id_panstwa)
    if not res:
        st.error("Nie znaleziono państwa.")
        return
    panstwo = res[0]

    with st.form("form_edit"):
 
        nazwa = st.text_input("Nazwa", value=panstwo["nazwa"], key=f"edit_p_nazwa_{id_panstwa}").strip()
        kod_iso = st.text_input("Kod ISO", value=panstwo["kod_iso"], key=f"edit_p_iso_{id_panstwa}").strip()
        
        st.divider()
        if st.form_submit_button("Zapisz zmiany", use_container_width=True, type="primary"):
            if nazwa and kod_iso:
                success, error = countries_db.update_country(id_panstwa, nazwa, kod_iso.upper())
                if success:
                    st.success("Zaktualizowano!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {error}")
            else:
                st.error("Pola są wymagane!")

with st.sidebar:
    st.header("🔍 Filtruj państwa")
    f_nazwa = st.text_input("Nazwa państwa", key="p_nazwa")
    f_kod = st.text_input("Kod ISO", key="p_kod")
    
    st.divider()
    st.button("Wyczyść filtry", on_click=reset_country_filters, use_container_width=True)


data_fetcher = lambda filter_by=None, search_term=None: countries_db.get_countries(
    filter_by=filter_by,
    search_term=search_term,
    f_nazwa=f_nazwa,
    f_kod=f_kod
)

render_crud_view(
    header_title="Zarządzanie Państwami",
    db_fetch_func=data_fetcher,
    db_delete_func=countries_db.delete_countries,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    id_column_name="id_panstwa",
    display_columns_for_delete=["nazwa", "kod_iso"],
    search_columns=[] 
)
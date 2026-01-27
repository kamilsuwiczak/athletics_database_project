import streamlit as st
import database_mgm_func.competition_types as competition_types_db
from components.data_manager import render_crud_view

@st.dialog("Dodaj nowy typ zawodów")
def add_modal():
    with st.form("form_dodaj_modal"):
        nazwa_typu = st.text_input("Nazwa").strip()
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if not nazwa_typu:
                st.error("Nazwa nie może być pusta.")
                return
            
            success, error = competition_types_db.add_competition_type(nazwa_typu)
            if success:
                st.success("Dodano!")
                st.rerun() 
            else:
                st.error(error)

@st.dialog("Edytuj typ zawodów")
def edit_modal(id_typu_zawodow):
    wynik = competition_types_db.get_competition_types("id", id_typu_zawodow)
    if not wynik:
        st.error("Nie znaleziono konkurencji.")
        return
    typ_zawodow = wynik[0]

    with st.form("form_edit"):
        nazwa_typu = st.text_input("Nazwa", value=typ_zawodow["nazwa_typu"]).strip()
        
        st.divider()
        
        if st.form_submit_button("Zapisz zmiany", use_container_width=True, type="primary"):
            if nazwa_typu:
                success, error = competition_types_db.update_competition_type(
                    id_typu_zawodow, nazwa_typu
                )
                if success:
                    st.success("Zaktualizowano pomyślnie!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {error}")
            else:
                st.error("Nazwa jest wymagana!")

search_cfg = [
    {"label": "Nazwa", "value": "nazwa_typu"},
]

render_crud_view(
    header_title="Zarządzanie Typami Zawodów",
    db_fetch_func=competition_types_db.get_competition_types,
    db_delete_func=competition_types_db.delete_competition_types,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    display_columns_for_delete=["nazwa_typu"],
    id_column_name="id_typu_zawodow",
    search_columns=search_cfg,
    delete_message="typu zawodów?"
)



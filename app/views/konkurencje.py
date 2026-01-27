import streamlit as st
import database_mgm_func.disciplines as disciplines_db
from components.data_manager import render_crud_view

@st.dialog("Dodaj nowe państwo")
def add_modal():
    with st.form("form_dodaj_modal"):
        nazwa = st.text_input("Nazwa").strip()
        rodzaj = st.text_input("Rodzaj").strip()
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if nazwa == "" or rodzaj == "":
                st.error("Nazwa i rodzaj nie mogą być puste.")
                return
            
            success, error = disciplines_db.add_discipline(nazwa, rodzaj)
            
            if success:
                st.success("Dodano!")
                st.rerun() 
            else:
                st.error(error)

@st.dialog("Edytuj dyscyplinę")
def edit_modal(id_dyscypliny):
    dyscyplina = disciplines_db.get_disciplines("id_dyscypliny", id_dyscypliny)[0]

    with st.form("form_edit"):
        nazwa = st.text_input("Nazwa", value=dyscyplina["nazwa"]).strip()
        rodzaj = st.text_input("Rodzaj", value=dyscyplina["rodzaj"]).strip()
        
        
        st.divider()
        
        if st.form_submit_button("Zapisz zmiany", use_container_width=True, type="primary"):
            if nazwa and rodzaj:
                success, error = disciplines_db.update_discipline(
                    id_dyscypliny, nazwa, rodzaj
                )
                
                if success:
                    st.success("Zaktualizowano pomyślnie!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {error}")
            else:
                st.error("Nazwa i rodzaj są wymagane!")

render_crud_view(
    header_title="Zarządzanie Dyscyplinami",
    db_fetch_func=lambda query=None: disciplines_db.get_disciplines("nazwa", query) if query else disciplines_db.get_disciplines(),
    db_delete_func=disciplines_db.delete_disciplines,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    display_columns_for_delete=["nazwa", "rodzaj"],
    id_column_name="id_konkurencji",
)



import streamlit as st
import database_mgm_func.coaches as coaches_db
from components.data_manager import render_crud_view

@st.dialog("Dodaj nowego trenera")
def add_modal():

    
    with st.form("form_dodaj_modal"):
        imie = st.text_input("Imię").strip()
        nazwisko = st.text_input("Nazwisko").strip()
        adres_email = st.text_input("Adres email").strip()
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if imie == "" or nazwisko == "" or adres_email == "":
                st.error("Imię, nazwisko i adres email nie mogą być puste.")
                return
            
            success, error = coaches_db.add_coach(imie, nazwisko, adres_email)
            
            if success:
                st.success("Dodano!")
                st.rerun() 
            else:
                st.error(error)

@st.dialog("Edytuj trenera")
def edit_modal(id_trenera):
    trener = coaches_db.get_coaches("id_trenera", id_trenera)[0]

    with st.form("form_edit"):
        imie = st.text_input("Imię", value=trener["Imię"]).strip()
        nazwisko = st.text_input("Nazwisko", value=trener["Nazwisko"]).strip()
        adres_email = st.text_input("Adres email", value=trener["Adres email"]).strip()
        
        
        st.divider()
        
        if st.form_submit_button("Zapisz zmiany", use_container_width=True, type="primary"):
            if imie and nazwisko and adres_email:
                success, error = coaches_db.update_coach(
                    id_trenera, imie, nazwisko, adres_email
                )
                
                if success:
                    st.success("Zaktualizowano pomyślnie!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {error}")
            else:
                st.error("Nazwa i kod ISO są wymagane!")



render_crud_view(
    header_title="Zarządzanie Trenerami",
    db_fetch_func=lambda query=None: coaches_db.get_coaches("name_surname", query) if query else coaches_db.get_coaches(),
    db_delete_func=coaches_db.delete_coaches,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    display_columns_for_delete=["Imię", "Nazwisko", "Adres email"],
    id_column_name="id_trenera",
    search_placeholder="Szukaj trenera po imieniu, nazwisku lub adresie email...",
)


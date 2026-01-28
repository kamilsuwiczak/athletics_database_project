import streamlit as st
import database_mgm_func.athlete_representatives as representatives_db
from components.data_manager import render_crud_view
import utils.validate_email as validate_email

@st.dialog("Dodaj nowego trenera")
def add_modal():
    with st.form("form_dodaj_modal"):
        imie = st.text_input("Imię").strip()
        nazwisko = st.text_input("Nazwisko").strip()
        adres_email = st.text_input("Adres email").strip()
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if not imie or not nazwisko or not adres_email:
                st.error("Wszystkie pola (Imię, Nazwisko, Email) są wymagane.")
                return
            

            if not validate_email.is_valid_email(adres_email):
                st.error("Nieprawidłowy format adresu email.")
                return
            success, error = representatives_db.add_athlete_representative(imie, nazwisko, adres_email)
            
            if success:
                st.success("Dodano!")
                st.rerun() 
            else:
                st.error(error)

@st.dialog("Edytuj przedstawiciela zawodnika")
def edit_modal(id_reprezentanta):
    wyniki = representatives_db.get_athlete_representatives("id", id_reprezentanta)
    
    if not wyniki:
        st.error("Nie znaleziono przedstawiciela zawodnika.")
        return

    przedstawiciel = wyniki[0]

    with st.form("form_edit"):
        imie = st.text_input("Imię", value=przedstawiciel["Imię"]).strip()
        nazwisko = st.text_input("Nazwisko", value=przedstawiciel["Nazwisko"]).strip()
        adres_email = st.text_input("Adres email", value=przedstawiciel["Email"]).strip()
        
        st.divider()
        
        if st.form_submit_button("Zapisz zmiany", use_container_width=True, type="primary"):
            if imie and nazwisko and adres_email:
                if not validate_email.is_valid_email(adres_email):
                    st.error("Nieprawidłowy format adresu email.")
                    return  
                success, error = representatives_db.update_athlete_representative(
                    id_reprezentanta, imie, nazwisko, adres_email
                )
                
                if success:
                    st.success("Zaktualizowano pomyślnie!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {error}")
            else:
                st.error("Wszystkie pola są wymagane!")

def reset_representative_filters():
    st.session_state["representative_imie"] = ""
    st.session_state["representative_nazwisko"] = ""
    st.session_state["representative_email"] = ""

with st.sidebar:
    st.header("🔍 Filtruj Przedstawicieli Zawodników")
    f_nazwisko = st.text_input("Nazwisko", placeholder="np. Nowak", key="representative_nazwisko")
    f_imie = st.text_input("Imię", placeholder="np. Adam", key="representative_imie")
    f_email = st.text_input("Email", placeholder="@gmail.com", key="representative_email")
    
    st.button("Wyczyść filtry", use_container_width=True, on_click=reset_representative_filters)
       


data_fetcher = lambda filter_by=None, search_term=None: representatives_db.get_athlete_representatives(
    filter_by=filter_by, search_term=search_term,
    f_imie=f_imie, f_nazwisko=f_nazwisko, f_email=f_email
)

render_crud_view(
    header_title="Zarządzanie Przedstawicielami Zawodników",
    db_fetch_func=data_fetcher,  
    db_delete_func=representatives_db.delete_athlete_representatives,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    id_column_name="id_reprezentanta",
    display_columns_for_delete=["Imię", "Nazwisko", "Email"],
    search_columns=[],
    delete_message="przedstawicieli zawodników?"
)
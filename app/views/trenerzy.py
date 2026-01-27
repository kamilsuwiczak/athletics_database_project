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
            if not imie or not nazwisko or not adres_email:
                st.error("Wszystkie pola (Imię, Nazwisko, Email) są wymagane.")
                return
            
            success, error = coaches_db.add_coach(imie, nazwisko, adres_email)
            
            if success:
                st.success("Dodano!")
                st.rerun() 
            else:
                st.error(error)

@st.dialog("Edytuj trenera")
def edit_modal(id_trenera):
    wyniki = coaches_db.get_coaches("id", id_trenera)
    
    if not wyniki:
        st.error("Nie znaleziono trenera.")
        return

    trener = wyniki[0]

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
                st.error("Wszystkie pola są wymagane!")

def reset_coach_filters():
    st.session_state["coach_imie"] = ""
    st.session_state["coach_nazwisko"] = ""
    st.session_state["coach_email"] = ""

with st.sidebar:
    st.header("🔍 Filtruj Trenerów")
    f_nazwisko = st.text_input("Nazwisko", placeholder="np. Nowak", key="coach_nazwisko")
    f_imie = st.text_input("Imię", placeholder="np. Adam", key="coach_imie")
    f_email = st.text_input("Email", placeholder="@gmail.com", key="coach_email")
    
    st.button("Wyczyść filtry", use_container_width=True, on_click=reset_coach_filters)
       


data_fetcher = lambda filter_by=None, search_term=None: coaches_db.get_coaches(
    filter_by=filter_by, search_term=search_term,
    f_imie=f_imie, f_nazwisko=f_nazwisko, f_email=f_email
)

render_crud_view(
    header_title="Zarządzanie Trenerami",
    db_fetch_func=data_fetcher,  
    db_delete_func=coaches_db.delete_coaches,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    id_column_name="id_trenera",
    display_columns_for_delete=["Imię", "Nazwisko", "Adres email"],
    search_columns=[],
    delete_message="trenerów?"
)
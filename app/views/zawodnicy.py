import streamlit as st
import database as db
import datetime
import pandas as pd

@st.dialog("Dodaj nowego zawodnika")
def modal_dodaj_zawodnika():
    lista_panstw = db.get_countries()
    opcje_panstw = {nazwa: kod for nazwa, kod in lista_panstw}
    
    with st.form("form_dodaj_modal"):
        imie = st.text_input("Imię")
        nazwisko = st.text_input("Nazwisko")
        data_ur = st.date_input("Data urodzenia", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        plec = st.selectbox("Płeć", ["K", "M"])
        panstwo_nazwa = st.selectbox("Wybierz państwo", options=list(opcje_panstw.keys()))
        
        if st.form_submit_button("Zapisz w bazie", use_container_width=True):
            if imie == "" or nazwisko == "":
                st.error("Imię i nazwisko nie mogą być puste.")
                return
            kod_iso = opcje_panstw[panstwo_nazwa]
            success, error = db.add_athlete(imie, nazwisko, data_ur, plec, kod_iso)
            
            if success:
                st.success("Dodano!")
                st.rerun() 
            else:
                st.error(error)

st.header("Zarządzanie Zawodnikami")

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Dodaj Zawodnika", width='stretch', type="primary"):
        modal_dodaj_zawodnika()

with col2:
    search_query = st.text_input("", placeholder="Szukaj zawodnika po nazwisku...", label_visibility="collapsed")

if search_query:
    data = db.get_athletes_filtered(search_query)
else:
    data = db.get_athletes()

df = pd.DataFrame(data)

if not df.empty:
    event = st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        on_select="rerun",  
        selection_mode="multi-row",
        column_config={
            "id_zawodnika": None
        }
    )

    selected_rows = event.selection.rows
    if selected_rows:

        ids_to_delete = df.iloc[selected_rows]["id_zawodnika"].tolist()
        st.warning(f"Zaznaczono {len(ids_to_delete)} zawodników.")
        
        if st.button("Usuń zaznaczonych", type="secondary"):
            
            success, error = db.delete_athletes(ids_to_delete)
            if success:
                st.success("Usunięto pomyślnie!")
                st.rerun()
            else:
                st.error(f"Nie można usunąć: {error} (Może zawodnik ma już przypisane wyniki?)")
else:
    st.info("Brak danych do wyświetlenia.")


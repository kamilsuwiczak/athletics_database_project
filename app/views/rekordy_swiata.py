import streamlit as st
import datetime
from components.data_manager import render_crud_view
import database_mgm_func.world_records as wr_db

def reset_filters():
    st.session_state["wr_konk"] = ""
    st.session_state["wr_zaw"] = ""
    st.session_state["wr_kraj"] = ""

@st.dialog("Dodaj Rekord Świata")
def add_modal():
  
    opts = wr_db.get_options_data()
    
    konk_map = {k['nazwa']: k['id_konkurencji'] for k in opts['konkurencje']}
    zaw_map = {f"{z['nazwisko']} {z['imie']} ({z['kraj']})": z['id_zawodnika'] for z in opts['zawodnicy']}
    
    with st.form("add_wr_form"):
        k_nazwa = st.selectbox("Konkurencja", options=list(konk_map.keys()))
        z_nazwa = st.selectbox("Zawodnik", options=list(zaw_map.keys()))
        
        c1, c2 = st.columns(2)
        with c1:
            wynik = st.number_input("Rezultat", min_value=0.0, step=0.01, format="%.2f")
        with c2:
            data = st.date_input("Data", value=datetime.date.today(), max_value=datetime.date.today())
            
        if st.form_submit_button("Zapisz", type="primary", use_container_width=True):
            if wynik <= 0:
                st.error("Wynik musi być dodatni.")
            else:
                success, msg = wr_db.add_world_record(
                    konk_map[k_nazwa], 
                    zaw_map[z_nazwa], 
                    wynik, 
                    data
                )
                if success:
                    st.success("Dodano rekord!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {msg}")

@st.dialog("Edytuj Rekord Świata")
def edit_modal(composite_id):
    res = wr_db.get_world_records(filter_by='id', search_term=composite_id)
    if not res:
        st.error("Nie znaleziono rekordu.")
        return
    rec = res[0]
    
    st.info(f"Edytujesz rekord: **{rec['Konkurencja']}** - **{rec['Zawodnik']}**")
    
    with st.form("edit_wr_form"):
        
        new_wynik = st.number_input(
            "Rezultat", 
            value=float(rec['Wynik']), 
            min_value=0.0, 
            step=0.01, 
            format="%.2f",
            key=f"wr_res_{composite_id}"
        )
        
        new_data = st.date_input(
            "Data", 
            value=rec['Data'],
            max_value=datetime.date.today(),
            key=f"wr_dat_{composite_id}"
        )
        
        if st.form_submit_button("Zapisz zmiany", type="primary", use_container_width=True):
            success, msg = wr_db.update_world_record(composite_id, new_wynik, new_data)
            if success:
                st.success("Zaktualizowano!")
                st.rerun()
            else:
                st.error(f"Błąd: {msg}")

with st.sidebar:
    st.header("🔍 Filtruj WR")
    f_konk = st.text_input("Konkurencja", placeholder="np. 100m", key="wr_konk")
    f_zaw = st.text_input("Zawodnik", placeholder="np. Bolt", key="wr_zaw")
    f_kraj = st.text_input("Kraj", placeholder="np. Jamajka", key="wr_kraj")
    
    st.divider()
    st.button("Wyczyść filtry", icon="🗑️", on_click=reset_filters, use_container_width=True)

data_fetcher = lambda filter_by=None, search_term=None: wr_db.get_world_records(
    filter_by=filter_by,
    search_term=search_term,
    f_konkurencja=f_konk,
    f_zawodnik=f_zaw,
    f_kraj=f_kraj
)

render_crud_view(
    header_title="Rekordy Świata",
    db_fetch_func=data_fetcher,
    db_delete_func=wr_db.delete_world_records,
    add_modal_func=add_modal,
    edit_modal_func=edit_modal,
    id_column_name="composite_id",
    display_columns_for_delete=["Konkurencja", "Zawodnik", "Wynik"],
    search_columns=[], 
    delete_message="rekordów?"
)
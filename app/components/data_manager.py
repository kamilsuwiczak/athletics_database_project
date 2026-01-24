import streamlit as st
import pandas as pd

def render_crud_view(
    header_title,
    db_fetch_func,
    db_delete_func,
    add_modal_func,
    edit_modal_func,
    id_column_name,
    display_columns_for_delete,
    search_placeholder="Szukaj...",
):
    st.header(header_title)

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button(f"Dodaj", type="primary", use_container_width=True):
            add_modal_func()

    with col2:
        search_query = st.text_input("", placeholder=search_placeholder, label_visibility="collapsed")

    if search_query:
        data = db_fetch_func(search_query)
    else:
        data = db_fetch_func()

    df = pd.DataFrame(data)

    if df.empty:
        st.info("Brak danych do wyświetlenia.")
        return


    event = st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        on_select="rerun",  
        selection_mode="multi-row",
        column_config={id_column_name: None}
    )


   
    selected_rows = event.selection.rows
    ids = []

    col_del, col_edit, _ = st.columns([1, 1, 3])
        

    if selected_rows:
        ids = df.iloc[selected_rows][id_column_name].tolist()
        
        delete_list = []
        for _, row in df.iloc[selected_rows].iterrows():
            delete_list.append(" ".join([str(row[col]) for col in display_columns_for_delete]))
    
    with col_del:
        if st.button("Usuń zaznaczone", type="secondary", use_container_width=True, disabled=not event.selection.rows):
            render_delete_dialog(ids, delete_list, db_delete_func)
    
    with col_edit:
        is_disabled = not event.selection.rows or len(event.selection.rows) != 1  
        if st.button("Edytuj rekord", type="secondary", use_container_width=True, disabled=is_disabled):
            edit_modal_func(ids[0])
        
        
@st.dialog("Potwierdź usunięcie")
def render_delete_dialog(ids, items_list, delete_callback):
    st.warning(f"Czy na pewno chcesz usunąć {len(ids)} elementów?")
    for item in items_list:
        st.write(f"- {item}")
    
    st.divider()
    c1, c2 = st.columns(2)
    if c1.button("Anuluj", use_container_width=True):
        st.rerun()
    if c2.button("Tak, usuń", type="primary", use_container_width=True):
        success, error = delete_callback(ids)
        if success:
            st.success("Usunięto!")
            st.rerun()
        else:
            st.error(f"Błąd: {error}")
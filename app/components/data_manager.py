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
    search_columns=None,  
    delete_message="elementy?",
    optional_column_modal_func=None,
    optional_column_modal_text=None
):
    st.header(header_title)

    col_add, col_search_val, col_search_type = st.columns([1, 1.5, 2.5])
    
    with col_add:
        if st.button(f"Dodaj", type="primary", use_container_width=True):
            add_modal_func()

    search_val = ""
    search_col = None

    if search_columns:
        with col_search_type:
            search_col_label = st.selectbox(
                "Szukaj po", 
                options=[c['label'] for c in search_columns],
                label_visibility="collapsed"
            )
            search_col = next(c['value'] for c in search_columns if c['label'] == search_col_label)
        
        with col_search_val:
            search_val = st.text_input(
                "", 
                placeholder=f"Filtruj wg {search_col_label.lower()}...", 
                label_visibility="collapsed"
            )
            
    if search_val and search_col:
        data = db_fetch_func(search_col, search_val)
    else:
        data = db_fetch_func()
    df = pd.DataFrame(data)

    if df.empty:
        st.info("Brak danych do wyświetlenia.")
        return


    column_configuration = {
        id_column_name: None
    }
    technical_cols = ["id_zawodnika", "id_konkurencji", "id_stadionu", "id_panstwa"]
    for col in technical_cols:
        if col in df.columns:
            column_configuration[col] = None

    event = st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        on_select="rerun",  
        selection_mode="multi-row",
        column_config=column_configuration
    )

   
    selected_rows = event.selection.rows
    ids = []

    col_del, col_edit, col_optional, _ = st.columns([1, 1, 2, 3])
        

    if selected_rows:
        ids = df.iloc[selected_rows][id_column_name].tolist()
        
        delete_list = []
        for _, row in df.iloc[selected_rows].iterrows():
            delete_list.append(" ".join([str(row[col]) for col in display_columns_for_delete]))
    
    with col_del:
        if st.button("Usuń zaznaczone", type="secondary", use_container_width=True, disabled=not event.selection.rows):
            render_delete_dialog(ids, delete_list, db_delete_func, delete_message=delete_message)
    
    with col_edit:
        is_disabled = not event.selection.rows or len(event.selection.rows) != 1  
        if st.button("Edytuj rekord", type="secondary", use_container_width=True, disabled=is_disabled):
            edit_modal_func(ids[0])
    
    if optional_column_modal_func:
        with col_optional:
            is_disabled = not event.selection.rows or len(event.selection.rows) != 1
            if st.button(optional_column_modal_text, type="secondary", use_container_width=True, disabled=is_disabled):
                optional_column_modal_func(ids[0])
    

        
@st.dialog("Potwierdź usunięcie")
def render_delete_dialog(ids, items_list, delete_callback, delete_message="elementy?"):
    st.warning(f"Czy na pewno chcesz usunąć {len(ids)} {delete_message} ")
    for item in items_list:
        st.write(f"- {item} ")

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
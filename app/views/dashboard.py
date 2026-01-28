import streamlit as st
import pandas as pd
from database_mgm_func.athletes import get_all_competition_types, get_top_5_medalists_by_type

st.title("Ranking Medalowy")


typy_zawodow = get_all_competition_types()

if typy_zawodow:
    wybrany_typ = st.selectbox(
        "Wybierz typ zawodów, aby zobaczyć najlepszych:", 
        typy_zawodow
    )
    if wybrany_typ:
        data = get_top_5_medalists_by_type(wybrany_typ)

        if data:
            df = pd.DataFrame(data)
            
    
            st.subheader(f"Top 5 zawodników: {wybrany_typ}")
            
            st.bar_chart(df, x="zawodnik", y="liczba_medali")
            
            with st.expander("Pokaż szczegółowe dane"):
                st.dataframe(df, use_container_width=True)
        else:
            st.info(f"Brak medalistów w kategorii: {wybrany_typ}")
else:
    st.warning("Nie znaleziono żadnych typów zawodów w bazie danych.")
import streamlit as st
from requisitions import start_getting

def trigger_build_dataframe(data, headers):
    df.columns = df.columns.str.lower().str.strip()
    if 'deveui' in df.columns:
        df = start_getting(df, header=headers)
        return df
    else:
        st.warning('Verifique se o arquivo subido possui a coluna "deveui"')

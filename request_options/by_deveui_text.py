import streamlit as st
from requisitions import start_getting, success_generated
import pandas as pd
from convert_files import convert

def deveui_forms(header):
    dev_digitados = st.text_area('Digite deveuis nesse campo separados por vírgula:').split(',')
    dev_digitados = [item.strip() for item in dev_digitados]
    with st.form(key='get_by_deveui'):
        if st.form_submit_button(label='Iniciar requisição'):
            df_deveuis = start_getting(pd.DataFrame(columns=['deveui'], data=dev_digitados), header=header)
    try:
        converted_text_input=convert(df_deveuis)
        success_generated(df_deveuis, converted_to_csv=converted_text_input)
    except:
        pass
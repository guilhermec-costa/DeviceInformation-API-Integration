import streamlit as st
from requisitions import get_by_deveui_remake, success_generated
from convert_files import convert
import pandas as pd


def deveui_forms(header, fields_to_search):
    dev_digitados = st.text_area('Digite deveuis nesse campo separados por vírgula:').split(',')
    if dev_digitados != "":
        with st.form(key='get_by_deveui'):
            if st.form_submit_button(label='Iniciar requisição'):
                data = get_by_deveui_remake(dev_digitados, header=header, fields=fields_to_search)
        try:
            df = pd.DataFrame(data)
            converted = convert(df)
            success_generated(df, converted_to_csv=converted)
        except:
            pass
import streamlit as st
import pandas as pd
from requisitions import get_by_plm_remake, success_generated
from convert_files import convert

def serial_forms(header, fields_to_search):
    plm_digitados = st.text_area(label='Digite PLM"s aqui, separados por vírgula').strip()
    plm_digitados = plm_digitados.split(',')
    if plm_digitados != "":
        with st.form(key='get_by_plm'):
            if st.form_submit_button(label='Iniciar requisição'):
                data = get_by_plm_remake(plm_digitados, header=header, fields=fields_to_search)
        try:
            df = pd.DataFrame(data)
            converted = convert(df)
            success_generated(df, converted_to_csv=converted)
        except:
            pass
import streamlit as st
import pandas as pd
from requisitions import get_by_serial, success_generated
from convert_files import convert

def serial_forms(header):
    plm_digitados = st.text_area(label='Digite PLM"s aqui, separados por vírgula').strip()
    plm_digitados = plm_digitados.split(',')
    plm_digitados = [item.strip() for item in plm_digitados]
    if plm_digitados is not "":
        with st.form(key='get_by_plm'):
            if st.form_submit_button(label='Iniciar requisição'):
                seriais = get_by_serial(*plm_digitados, header=header)
                df_plms = pd.DataFrame.from_dict(data=seriais, orient='index', columns=['PLM']).reset_index()           
    try:
        converted_text_input=convert(df_plms)
        success_generated(df_plms, converted_to_csv=converted_text_input)
    except:
        pass

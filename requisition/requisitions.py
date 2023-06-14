import requests
import streamlit as st
import pandas as pd
from convert_files import convert
from datetime import datetime, timedelta
    
def success_generated(df, converted_to_csv, filename):
    st.success('Arquivo gerado com sucesso!')
    st.write('Prévia do arquivo: ')
    st.write(df)
    st.download_button(label='Clique aqui para baixá-lo', data=converted_to_csv, file_name=filename, mime='text/csv')

def start_requisition(*content, header, fields, info_type, project, form_key):
    dict_list = []
    if content[0][0] != "":
        with st.form(key=f'data_frame - {form_key} - {info_type}'):
            if st.form_submit_button(label='Submit'):
                with st.spinner(text='Gerando dados...'):
                    for element in content[0]:
                        empty_dict = {}
                        if info_type == 'serial':
                            base_url = f'http://34.218.70.208:99/{project}/get-by-serial?serial={element}'
                        elif info_type in ('deveui'):
                            base_url = f'http://34.218.70.208:99/{project}/?devEui={element}'
                        elif info_type == 'boxserial':
                            base_url = f'http://34.218.70.208:99/{project}/get-by-box-serial?boxSerial={element}'

                        try:
                            for field in fields:
                                r = requests.get(url=base_url, headers=header)
                                empty_dict[f'{field}'] = r.json().get(f'{field}')
                        except:
                            empty_dict[f'{field}'] = f'Verifique o {info_type} "{element}"'
                        dict_list.append(empty_dict)
        if len(dict_list) > 0:
            build_datatable(dict_list, filename=f'{info_type}-{project}-{(datetime.now() - timedelta(hours=-3)).strftime("%d-%M-%Y")}.csv')
            return dict_list

def build_datatable(data, filename):
    df = pd.DataFrame(data)
    converted = convert(df)
    success_generated(df, converted_to_csv=converted, filename=filename)
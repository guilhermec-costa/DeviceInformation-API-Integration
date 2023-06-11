import requests
import streamlit as st
import pandas as pd
from convert_files import convert
from datetime import datetime
    
def success_generated(df, converted_to_csv, filename):
    st.success('Arquivo gerado com sucesso!')
    st.write('Prévia do arquivo: ')
    st.write(df)
    st.download_button(label='Clique aqui para baixá-lo', data=converted_to_csv, file_name=filename, mime='text/csv')

def start_requisition(*content, header, fields, info_type, project):
    dict_list = []
    if content[0][0] != "":
        with st.form(key=info_type):
            if st.form_submit_button(label='Submit'):
                with st.spinner(text='Gerando dados...'):
                    for element in content[0]:
                        empty_dict = {}
                        if info_type == 'plm':
                            base_url = f'http://34.218.70.208:99/{project}/get-by-serial?serial={element}'
                        elif info_type in ('deveui', 'deveuis_dataframe'):
                            base_url = f'http://34.218.70.208:99/{project}/?devEui={element}'
                        elif info_type == 'boxserial':
                            base_url = f'http://34.218.70.208:99/{project}/get-by-box-serial?boxSerial={element}'

                        try:
                            for field in fields:
                                r = requests.get(url=base_url, headers=header)
                                st.spinner(text='Buscando informações')
                                empty_dict[f'{field}'] = r.json().get(f'{field}')
                        except:
                            empty_dict[f'{field}'] = f'Verifique o {info_type} "{element}"'
                        dict_list.append(empty_dict)
    if len(dict_list) > 0:
        build_datatable(dict_list, filename=f'{info_type}-{project}-{datetime.now().strftime("%d-%M-%Y")}')

def build_datatable(data, filename):
    try:
        df = pd.DataFrame(data)
        converted = convert(df)
        success_generated(df, converted_to_csv=converted, filename=filename)
    except:
        pass
import requests
import streamlit as st
import pandas as pd
    
def success_generated(df, converted_to_csv):
    st.success('Arquivo gerado com sucesso!')
    st.write('Prévia do arquivo: ')
    st.write(df.head())
    st.download_button(label='Clique aqui para baixá-lo', data=converted_to_csv, file_name='deveuis.csv', mime='text/csv')


def get_by_plm_remake(*plms, header, fields):
    lista_dicios = []
    for plm in plms[0]:
        plm = plm.strip()
        dicio_vazio = {}
        url = f'http://34.218.70.208:99/devices/get-by-serial?serial={plm}'
        try:
            for field in fields:
                r = requests.get(url=url, headers=header)
                st.spinner(text='Buscando BoxSeriais e Seriais')
                dicio_vazio[f'{field}'] = r.json().get(f'{field}')
        except:
            dicio_vazio[f'{field}'] = f'Verifique a PLM {plm}'
        lista_dicios.append(dicio_vazio)
    return lista_dicios

def get_by_deveui_remake(*deveuis, header, fields):
    lista_dicios = []
    for deveui in deveuis[0]:
        deveui = deveui.strip()
        dicio_vazio = {}
        url = f"http://34.218.70.208:99/devices/?devEui={deveui}"
        try:
            for field in fields:
                r = requests.get(url=url, headers=header)
                st.spinner(text='Buscando BoxSeriais e Seriais')
                dicio_vazio[f'{field}'] = r.json().get(f'{field}')
        except:
            dicio_vazio[f'{field}'] = f'Verifique o devEui {deveui}'
        lista_dicios.append(dicio_vazio)
    return lista_dicios
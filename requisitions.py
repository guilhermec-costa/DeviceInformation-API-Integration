import requests
import streamlit as st
import pandas as pd

def criar_objeto():
    objeto = {}
    return objeto

def start_getting(df, header):
    df[['BoxSerial', 'Serial']] = df['deveui'].apply(lambda x: pd.Series(get_by_deveui(x, header=header)))
    return df

def get_by_deveui(deveui, header):
    url = f"http://34.218.70.208:99/devices/?devEui={deveui}"
    try:
        r = requests.get(url=url, headers=header)
        st.spinner(text='Buscando BoxSeriais e Seriais')
        return {'BoxSerial': r.json().get('boxSerial'), 'Serial': r.json().get('serial')}
    except:
        return {'BoxSerial':'-', 'Serial':'-'}

def get_by_serial(*serial:list, header):
    dicio = criar_objeto()
    for plm in serial:
        url = f'http://34.218.70.208:99/devices/get-by-serial?serial={plm}'
        try:
            r = requests.get(url=url, headers=header)
            dicio[f'{plm}'] = r.json().get('devEui')
        except:
            dicio[f'{plm}'] = f'Verificar PLM "{plm}"'
    return dicio
    
def success_generated(df, converted_to_csv):
    st.success('Arquivo gerado com sucesso!')
    st.write('Prévia do arquivo: ')
    st.write(df.head())
    st.download_button(label='Clique aqui para baixá-lo', data=converted_to_csv, file_name='deveuis.csv', mime='text/csv')
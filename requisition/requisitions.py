import streamlit as st
import pandas as pd
from convert_files import convert
from datetime import datetime, timedelta
import json
import time
import asyncio
import aiohttp
from convert_files import read_file
from format_columns import validate_data
from stqdm import stqdm
    
def success_generated(df, converted_to_csv, filename):
    st.success('Arquivo gerado com sucesso!')
    st.write('Prévia do arquivo: ')
    st.write(df)
    st.download_button(label='Clique aqui para baixá-lo', data=converted_to_csv, file_name=filename, mime='text/csv')

def build_datatable(data, filename):
    df = pd.DataFrame(data)
    converted = convert(df)
    success_generated(df, converted_to_csv=converted, filename=filename)

async def get_binary_version(element, header, fields_to_search, empty_obj, session):
    url = f'http://34.218.70.208:99/json-logs/get-all-by-dev-eui?devEui={element}'
    async with session.get(url, headers=header) as r:
        for field in fields_to_search:
            try:
                content = (await r.json())[0]
                if field == 'deviceEui':
                    empty_obj[f'{field}'] = content.get(field)
                else:
                    execution_date = eval(content.get('log'))
                    empty_obj[f'{field}'] = execution_date.get(field)
            except:
                empty_obj[f'{field}'] = f'Verifique o deveui "{element}"'
    return empty_obj

async def get_device_info(element, project, info_type, session,
                    empty_obj, fields_to_search, header):
    url_mapping = {
        'serial': f'http://34.218.70.208:99/{project}/get-by-serial?serial={element}',
        'deveui': f'http://34.218.70.208:99/{project}/?devEui={element}',
        'boxserial': f'http://34.218.70.208:99/{project}/get-by-box-serial?boxSerial={element}'
    }
    base_url = url_mapping.get(info_type)
       
    async with session.get(base_url, headers=header) as r:

        for field in fields_to_search:
            try:
                content = await r.json()
                empty_obj[f'{field}'] = content.get(field)
            except:
                empty_obj[f'{field}'] = f'Verifique o {info_type} "{element}"'
    return empty_obj

async def start_requisition(*content, header, fields, info_type, project="devices", form_key, requisiton_function):
    dict_list = []
    async with aiohttp.ClientSession() as session:
        with st.form(key=f'data_frame - {form_key} - {info_type}'):
            if st.form_submit_button(label='Requisitar'):
                with st.spinner('Gerando dados...'):
                    for n in stqdm(range(len(content[0]))):
                        element = content[0][n]
                        empty_dict = {}
                        if requisiton_function == 'get_device_info':
                            data = await get_device_info(element=element, project=project, info_type=info_type, session=session,
                                                    empty_obj=empty_dict, fields_to_search=fields, header=header)
                
                        elif requisiton_function == 'firmware_info':
                            data = await get_binary_version(element=element, empty_obj=empty_dict, fields_to_search=fields,
                                                    header=header, session=session)
                        dict_list.append(data)
                        asyncio.sleep(0.1)
    
        if len(dict_list) > 0:
            build_datatable(dict_list, filename=f'{info_type}-{project}-{(datetime.now() - timedelta(hours=-3)).strftime("%d-%M-%Y")}.csv')

def requis_for_dataframes(arquivo, requis_type, fields_to_search, project, headers):
    data, extension, name = read_file(file=arquivo)
    if data is not None:
        is_valid, valid_get_options = validate_data(data, extension)
        if requis_type == 'firmware_info':
            valid_get_options = ['devEui']
        if is_valid:
            st.success(f'Arquivo "{name + extension}" lido e formatado com sucesso.')
            get_option = st.radio(label='Escolha a coluna base da planilha para fazer as requisições:', options=valid_get_options, horizontal=True, key=requis_type)
            devices_escolhidos = data[get_option].to_list()
            asyncio.run(start_requisition(devices_escolhidos, header=headers, fields=fields_to_search, 
                                                requisiton_function=requis_type,info_type=get_option.lower(),
                                                project=project, form_key=f'data_frame - {get_option} - {requis_type}'))
        else:
            st.warning('Verifique se o arquivo subido possui pelo menos umas das seguintes colunas: "deveui", "serial" ou "serialbox" ou se tem pelos menos uma linha de valores.')

import streamlit as st
import pandas as pd
from requisitions import success_generated, get_by_deveui_remake
from convert_files import convert, read_file
from PIL import Image
from request_options import by_deveui_text, by_plm_text
from select_boxes import SelectBoxes


st.set_page_config(layout='centered')

with open('token.txt', 'r') as token:
    content = token.read()

headers = {'Authorization': f'{content}'}

arquivo = st.file_uploader(label='Escolha um arquivo')
imagem = Image.open(r'sheet_template.PNG')
st.image(image=imagem, caption='Planilha de exemplo')
st.markdown('---')

colunas = []
checkbox1, checkbox2 = st.columns(2)
with checkbox1:
    deveui_select_box = SelectBoxes(label='Habilitar DevEUI', key='devEui', start_mode=True)
    plm_select_box = SelectBoxes(label='Habilitar PLM', key='serial', start_mode=True)
    boxserial = SelectBoxes(label='Habilitar Box Serial', key='boxSerial', start_mode=True)
    device_adress = SelectBoxes(label='EnaHabilitarle Device Adress', key='deviceAddress', start_mode=True)
with checkbox2:
    created_at = SelectBoxes(label='Habilitar Creation Date', key='createdAt', start_mode=False)
    applicationKey = SelectBoxes(label='Habilitar Application Key', key='applicationKey', start_mode=False)
    networkkey = SelectBoxes(label='Habilitar Network Key', key='networkKey', start_mode=False)

SelectBoxes.all_select_boxes = [deveui_select_box.select_box, plm_select_box.select_box, applicationKey.select_box, networkkey.select_box,
                                networkkey.select_box, boxserial.select_box, device_adress.select_box, created_at.select_box]

for item in SelectBoxes.all_select_boxes:
    columns_list = [key for key, value in item.items() if value]
    for key, value in item.items():
        if value and key not in colunas:
            colunas.append(key)
        elif value is False and key in colunas:
            colunas.remove(key)

if arquivo is not None:
        df = read_file(file=arquivo)
        if df is not None:
            for item in colunas:
                if item != 'devEui':
                    df[item] = ''

            with st.form(key='gerar relatorio'):
                if st.form_submit_button(label='Gerar relatório'):
                    with st.spinner('Gerando arquivo com Box Serial e Serial Number...'):
                        deveuis_escolhidos = df['devEui'].to_list()
                        data = get_by_deveui_remake(deveuis_escolhidos, header=headers, fields=colunas)
                        df = pd.DataFrame(data)
                        converted = convert(df)
            try:
                success_generated(df, converted_to_csv=converted)
            except:
                pass
        else:
            st.warning('Verifique se o arquivo subido possui extensão CSV ou XLSX')

st.markdown('---')

st.markdown("###")

by_plm_text.serial_forms(header=headers, fields_to_search=colunas)
by_deveui_text.deveui_forms(header=headers, fields_to_search=colunas)
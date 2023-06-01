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

headers = {
  'Authorization': f'{content}'}

arquivo = st.file_uploader(label='Escolha um arquivo')
imagem = Image.open(r'sheet_template.PNG')
st.image(image=imagem, caption='Planilha de exemplo')

colunas = []
deveui_select_box = SelectBoxes(label='Enable DevEUI', key='devEui', start_mode=True)
applicationKey = SelectBoxes(label='Enable Application Key', key='applicationKey', start_mode=False)
plm_select_box = SelectBoxes(label='Enable PLM', key='serial', start_mode=True)
applicationKeyEncrypted = SelectBoxes(label='Enable Application Key Encripted', key='applicationKeyEncrypted', start_mode=False)
networkkey = SelectBoxes(label='Enable Network Key', key='networkKey', start_mode=False)
networkKeyEncrypted = SelectBoxes(label='Enable Newtwork Key Encripted', key='networkKeyEncrypted', start_mode=False)

SelectBoxes.all_select_boxes = [deveui_select_box.select_box, plm_select_box.select_box, applicationKey.select_box, networkkey.select_box,
                                applicationKeyEncrypted.select_box, networkkey.select_box, networkKeyEncrypted.select_box]

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
st.markdown('---')

by_plm_text.serial_forms(header=headers, fields_to_search=colunas)
by_deveui_text.deveui_forms(header=headers, fields_to_search=colunas)
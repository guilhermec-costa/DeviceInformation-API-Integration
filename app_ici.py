import streamlit as st
import pandas as pd
from requisition import requisitions
from convert_files import convert, read_file
from PIL import Image
from select_boxes import SelectBoxes
from requisition_forms import RequisitionForm
from format_columns import format_dfcolumns, add_extra_columns, validate_data


st.set_page_config(layout='centered')
with open('token.txt', 'r') as token:
    content = token.read()

with open('style.css', 'r') as style:
    st.markdown(f'<style>{style.read()}</style>', unsafe_allow_html=True)

headers = {'Authorization': f'{content}'}

arquivo = st.file_uploader(label='Escolha um arquivo')
imagem = Image.open(r'sheet_template.PNG')
st.image(image=imagem, caption='Planilha de exemplo', width=250)
st.markdown('---')

colunas = []
project_options = ['devices', 'everynet-devices', 'nbiot-devices']
project = st.selectbox(label='Selecione um projeto', options=project_options, disabled=False)
checkbox1, checkbox2 = st.columns(2)
with checkbox1:
    deveui_select_box = SelectBoxes(label='Habilitar DevEUI', key='devEui', start_mode=True)
    plm_select_box = SelectBoxes(label='Habilitar PLM', key='serial', start_mode=True)
    boxserial = SelectBoxes(label='Habilitar Box Serial', key='boxSerial', start_mode=True)
    device_adress = SelectBoxes(label='Habilitar Device Adress', key='deviceAddress', start_mode=True)
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
        data, extension = read_file(file=arquivo)
        is_valid = validate_data(data, extension)
        if extension in ('.csv', '.xlsx'):
            if is_valid:
                df = add_extra_columns(data, extra_columns=colunas)
                deveuis_escolhidos = df['devEui'].to_list()
                data = requisitions.start_requisition(deveuis_escolhidos, header=headers, fields=colunas,
                                                            info_type='deveuis_dataframe', project=project)
                df = pd.DataFrame(data)
                converted = convert(df)
                try:
                    requisitions.success_generated(df, converted_to_csv=converted)
                except:
                    pass
            else:
                st.warning('Verifique se os dados subidos possuem uma coluna de nome "deveui" ou se não está vazia.')

st.markdown('---')
st.markdown("###")

byPlmForms = RequisitionForm("Digite PLM's nesse campo, separados por vírgula")
requisitions.start_requisition(byPlmForms.content, header=headers, fields=colunas, info_type='plm', project=project)
    
byDeveuiForms = RequisitionForm("Digite DevEui's nesse campo, separados por vírgula:")
requisitions.start_requisition(byDeveuiForms.content, header=headers, fields=colunas, info_type='deveui', project=project)
    
bySerialBoxForms = RequisitionForm("Digite BoxSerial(s) nesse campo, separados por vírgulas:")
requisitions.start_requisition(bySerialBoxForms.content, header=headers, fields=colunas, info_type='boxserial', project=project)

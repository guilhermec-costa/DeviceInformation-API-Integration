import streamlit as st
import pandas as pd
from requisition import requisitions
from convert_files import read_file
from PIL import Image
from select_boxes import SelectBoxes
from requisition_forms import RequisitionForm
from format_columns import validate_data

st.set_page_config(layout='centered')

with open('style.css', 'r') as style:
    st.markdown(f'<style>{style.read()}</style>', unsafe_allow_html=True)

headers = {'Authorization': f'{st.secrets.token}'}

arquivo = st.file_uploader(label='Escolha um arquivo')
imagem = Image.open(r'template_sheet.PNG')
st.image(image=imagem, caption='Planilha de exemplo. Deve conter pelo menos uma dessas colunas, independente de maíusculas ou minúsculas.', width=500)
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
    for key, value in item.items():
        if value and key not in colunas:
            colunas.append(key)
        elif value is False and key in colunas:
            colunas.remove(key)

if arquivo is not None:
        data, extension, name = read_file(file=arquivo)
        if data is not None:
            is_valid, valid_get_options = validate_data(data, extension)
            if is_valid:
                st.success(f'Arquivo "{name + extension}" lido e formatado com sucesso.')
                get_option = st.radio(label='Escolha a coluna base da planilha para fazer as requisições:', options=valid_get_options, horizontal=True)
                devices_escolhidos = data[get_option].to_list()
                data_frame_requisitions = requisitions.start_requisition(devices_escolhidos, header=headers, fields=colunas,
                                                            info_type=get_option.lower(), project=project, form_key=f'data_frame - {get_option}')
            else:
                st.warning('Verifique se o arquivo subido possui pelo menos umas das seguintes colunas: "deveui", "serial" ou "serialbox" ou se tem pelos menos uma linha de valores.')

st.markdown('---')
st.markdown("###")

byPlmForms = RequisitionForm("Digite PLM's nesse campo, separados por vírgula", form_key='PLM-forms')
if byPlmForms.content[0] != "":
    plm_requisitions = requisitions.start_requisition(byPlmForms.content, header=headers, fields=colunas, info_type='serial', project=project, form_key=byPlmForms.form_key)
    
byDeveuiForms = RequisitionForm("Digite DevEui's nesse campo, separados por vírgula:", form_key='DEVEUI-forms')
if byDeveuiForms.content[0] != "":
    deveui_requitions = requisitions.start_requisition(byDeveuiForms.content, header=headers, fields=colunas, info_type='deveui', project=project, form_key=byDeveuiForms.form_key)
    
bySerialBoxForms = RequisitionForm("Digite BoxSerial(s) nesse campo, separados por vírgulas:", form_key='SERIALBOX-forms')
if bySerialBoxForms.content[0] != "":
    boxserial_requisitions = requisitions.start_requisition(bySerialBoxForms.content, header=headers, fields=colunas, info_type='boxserial', project=project, form_key=bySerialBoxForms.form_key)

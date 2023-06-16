import streamlit as st
from requisition import requisitions
from PIL import Image
from select_boxes import SelectBoxes, Firmware, populate_selectboxes_list
from requisition_forms import RequisitionForm
import asyncio

st.set_page_config(layout='centered')

with open('style.css', 'r') as style:
    st.markdown(f'<style>{style.read()}</style>', unsafe_allow_html=True)

headers = {'Authorization': f'{st.secrets.token}'}

devices_file = st.file_uploader(label='Escolha um arquivo', key='device file')
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

populate_selectboxes_list(col_to_populate=colunas, col_populated=SelectBoxes.all_select_boxes)

if devices_file is not None:
    requisitions.requis_for_dataframes(devices_file, requis_type='get_device_info', fields_to_search=colunas, 
                          project=project, headers=headers)

st.markdown('---')
st.markdown("###")

byPlmForms = RequisitionForm("Digite PLM's nesse campo, separados por vírgula", form_key='PLM-forms')
if byPlmForms.content[0] != '':
    plm_requisitions = asyncio.run(requisitions.start_requisition(byPlmForms.content, header=headers, fields=colunas, info_type='serial', project=project, form_key=byPlmForms.form_key,
                                                      requisiton_function='get_device_info'))
    
byDeveuiForms = RequisitionForm("Digite DevEui's nesse campo, separados por vírgula:", form_key='DEVEUI-forms')
if byDeveuiForms.content[0] != '':
    deveui_requitions = asyncio.run(requisitions.start_requisition(byDeveuiForms.content, header=headers, fields=colunas, info_type='deveui', project=project, form_key=byDeveuiForms.form_key,
                                                       requisiton_function='get_device_info'))
    
bySerialBoxForms = RequisitionForm("Digite BoxSerial(s) nesse campo, separados por vírgulas:", form_key='SERIALBOX-forms')
if bySerialBoxForms.content[0] != '':
    boxserial_requisitions = asyncio.run(requisitions.start_requisition(bySerialBoxForms.content, header=headers, fields=colunas, info_type='boxserial', project=project, form_key=bySerialBoxForms.form_key,
                                                            requisiton_function='get_device_info'))


st.markdown('---')
st.markdown('###')
colunas_firmware = []
st.subheader(body='Informações do firmware')
firmware_file = st.file_uploader(label='Escolha um arquivo', key='firmware_file')

deveui_firmware = Firmware(label='Habilitar DevEui', key='deviceEui', start_mode=True, disabled=False)
firmware_updated_at = Firmware(label='Habilitar última data de alteração do firmware', key='Execution Date', start_mode=False)
firmware_binary_version = Firmware(label='Habilitar última versão do firmware', key='Binary Version', start_mode=True)
device_last_rssi = Firmware(label='Habilitar último RSSI', key='Network Data Send RSSI Value', start_mode=False)
Firmware.firmware_select_boxes = [deveui_firmware.select_box, firmware_binary_version.select_box,
                                   firmware_updated_at.select_box, device_last_rssi.select_box]
populate_selectboxes_list(col_to_populate=colunas_firmware, col_populated=Firmware.firmware_select_boxes)


if firmware_file is not None:
    requisitions.requis_for_dataframes(firmware_file, requis_type='firmware_info', fields_to_search=colunas_firmware,
                                       project=project, headers=headers)

firmwareActivation = RequisitionForm('Digite o DevEui nesse campo: ', form_key='firmware_activation')
if firmwareActivation.content[0] != '':
    firmware = asyncio.run(requisitions.start_requisition(firmwareActivation.content, header=headers, form_key=firmwareActivation.form_key, fields=colunas_firmware, info_type='firmware_info',
                                              requisiton_function='firmware_info'))
import streamlit as st
import pandas as pd
from requisitions import success_generated, get_by_serial
from convert_files import convert, read_file
from PIL import Image
from request_options import by_upload, by_deveui_text, by_plm_text


st.set_page_config(layout='centered')

with open('token.txt', 'r') as token:
    content = token.read()

headers = {
  'Authorization': f'{content}'}

arquivo = st.file_uploader(label='Escolha um arquivo')
imagem = Image.open(r'sheet_template.PNG')
st.image(image=imagem, caption='Planilha de exemplo')


if arquivo is not None:
        df = read_file(file=arquivo)
        if df is not None:
            with st.spinner('Gerando arquivo com Box Serial e Serial Number...'):
                df = by_upload.trigger_build_dataframe(data=df, headers=headers)
                converted = convert(df)
                success_generated(df, converted_to_csv=converted)
        else:
            st.warning('Verifique se o arquivo subido possui extensão CSV ou XLSX')

st.markdown('---')
by_deveui_text.deveui_forms(header=headers)

st.markdown("###")
st.markdown('---')
by_plm_text.serial_forms(header=headers)
try:
    st.write(df_PLMS)
except:
    pass

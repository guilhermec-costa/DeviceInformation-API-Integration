import streamlit as st
import pandas as pd
from requisitions import start_getting, success_generated
from convert_files import convert, read_file
from PIL import Image


st.set_page_config(layout='centered')

with open('token.txt', 'r') as token:
    content = token.read()

headers = {
  'Authorization': f'{content}'}

arquivo = st.file_uploader(label='Escolha um arquivo')
imagem = Image.open(r'sheet_template.PNG')
st.image(image=imagem, caption='Planilha de exemplo')


if arquivo is not None:
    with st.spinner('Gerando arquivo com Box Serial e Serial Number...'):
        df = read_file(file=arquivo)
        if df is not None:
            df.columns = df.columns.str.lower().str.strip()
            if 'deveui' in df.columns:
                df = start_getting(df, header=headers)
                converted = convert(df)
                success_generated(df, converted_to_csv=converted)
            else:
                st.warning('Verifique se o arquivo subido possui a coluna "deveui"')
        else:
            st.warning('Verifique se o arquivo subido possui extensão CSV ou XLSX')

st.markdown('---')
with st.form(key='deveui text input'):
    dev_digitados = st.text_area('Ou digite deveuis nesse campo separados por vírgula:').split(',')
    dev_digitados = [item.strip() for item in dev_digitados]
    if st.form_submit_button(label='Iniciar requisição'):
        df = start_getting(pd.DataFrame(columns=['deveui'], data=dev_digitados), header=headers)
        converted_text_input=convert(df)
try:
    success_generated(df, converted_to_csv=converted_text_input)
except:
    pass
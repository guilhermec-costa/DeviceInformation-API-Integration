import pandas as pd
import streamlit as st
def format_dfcolumns(df):
    df.columns = [column.strip().lower() for column in df.columns]

    for column_name in df.columns:
        if column_name == 'deveui':
            df.rename(columns={column_name:'devEui'}, inplace=True)
    return df

def add_extra_columns(df, extra_columns):
    for extra_column in extra_columns:
        if extra_column != 'devEui':
            df[extra_column] = ''
    return df

def validate_data(df, extension):
    if extension in ('.csv', '.xlsx', '.xls'):
        df = format_dfcolumns(df)
        if 'devEui' in df.columns and len(df) > 0:
            return True
        return False
    else:
        st.warning('Verifique se o arquivo subido possui extensão CSV, XLSX ou XLS.')

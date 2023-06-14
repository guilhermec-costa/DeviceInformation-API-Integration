import pandas as pd
import streamlit as st

def format_dfcolumns(df):
    df.columns = [column.strip().lower() for column in df.columns]

    for column_name in df.columns:
        if column_name == 'deveui':
            df.rename(columns={column_name:'devEui'}, inplace=True)
        elif column_name == 'boxserial':
            df.rename(columns={column_name:'boxSerial'}, inplace=True)
    return df

def validate_data(df, extension):
    df = format_dfcolumns(df)
    valid_values = ('devEui', 'serial', 'boxSerial')
    if any(column in df.columns for column in valid_values) and len(df) > 0:
        valid_get_columns = [column for column in df.columns if column in valid_values]
        return True, valid_get_columns
    else:
        return False, None

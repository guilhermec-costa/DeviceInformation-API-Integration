import streamlit as st
import pandas as pd
from convert_files import convert
from requisition import requisitions

class RequisitionForm:
    def __init__(self, label):
        self.label = label
        self.content = self.build_form()
    
    def build_form(self):
        content = st.text_area(label=self.label)
        return format_form(content)


def format_form(content: RequisitionForm):
    content = content.split(',')
    content = [elemento.strip() for elemento in content]
    return content

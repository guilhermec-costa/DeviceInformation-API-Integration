import streamlit as st
class RequisitionForm:
    def __init__(self, label, form_key):
        self.label = label
        self.form_key = form_key
        self.content = self.build_form()
    
    def build_form(self):
        content = st.text_area(label=self.label, key=self.form_key)
        return format_form(content)


def format_form(content: RequisitionForm):
    content = content.split(',')
    content = [elemento.strip() for elemento in content]
    return content

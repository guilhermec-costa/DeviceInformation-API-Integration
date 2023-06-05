import streamlit as st

class SelectBoxes:

    all_select_boxes = []

    def __init__(self, label, key, start_mode):
        self.label = label
        self.key = key
        self.start_mode = start_mode
        self.select_box = self.create_select_box()

    @classmethod
    def populate_select_list(cls, key, objeto):
        cls.all_select_boxes.append({key:objeto})
    
    def create_select_box(self):
        select_box = st.checkbox(label=self.label, value=self.start_mode, key=self.key)
        return {self.key : select_box}

import streamlit as st

class SelectBoxes:

    all_select_boxes = []

    def __init__(self, label, key, start_mode, disabled = False):
        self.label = label
        self.key = key
        self.start_mode = start_mode
        self.disabled = disabled
        self.select_box = self.create_select_box()

    @classmethod
    def populate_select_list(cls, key, objeto):
        cls.all_select_boxes.append({key:objeto})
    
    def create_select_box(self):
        select_box = st.checkbox(label=self.label, value=self.start_mode, key=self.key, disabled=self.disabled)
        return {self.key : select_box}
    
class Firmware(SelectBoxes):
    firmware_select_boxes = []

    def __init__(self, label, key, start_mode, disabled=False):
        super().__init__(label, key, start_mode, disabled)

def populate_selectboxes_list(col_to_populate, col_populated):
    for item in col_populated:
        for key, value in item.items():
            if value and key not in col_to_populate:
                col_to_populate.append(key)
            elif value is False and key in col_to_populate:
                col_to_populate.remove(key)
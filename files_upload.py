# -*- coding: utf-8 -*-

import pandas as pd
import json
import os
import streamlit as st


json_file_upload = st.file_uploader("Choose a JSON file", type='json')
excel_file_upload = st.file_uploader("Choose a Excel file", type=['xls','xlsx'])

st.write("filename:", json_file_upload.name)
st.write("filename:", excel_file_upload.name)

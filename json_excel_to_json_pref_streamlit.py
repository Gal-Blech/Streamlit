import streamlit as st
import pandas as pd
import json
from io import BytesIO
import openpyxl

# Function to process files
def process_files(json_file, excel_file):
    try:
        data = json.load(json_file)

        long_codes = []
        route_ids = []
        direction_ids = []
        service_id = ''
        
        # Access the top-level services
        top_level_services = data.get('services', [])
        for service in top_level_services:
            if service.get('name') == service_name:
                service_id = service.get('id', '')
                break
        
        routes = data.get('routes', [])
        if routes is None:
            raise ValueError("The key 'routes' is not found or is None in the JSON data.")
        
        for route in routes:
            if route is None:
                continue
            
            route_id = route.get('_id', '')
            code = route.get('code', '')

            directions = route.get('directions', [])
            if directions is None:
                directions = []
            
            if directions:
                for direction in directions:
                    if direction is None:
                        continue
                    direction_id = direction.get('id', '')
                    original_direction_value = direction.get('original_direction_value', '')

                    # Construct Long Code
                    long_code = "{}{}".format(code, original_direction_value)

                    long_codes.append(long_code)
                    route_ids.append(route_id)
                    direction_ids.append(direction_id)
            else:
                long_codes.append(code)
                route_ids.append(route_id)
                direction_ids.append('')

        df = pd.DataFrame({
            'Long Code': long_codes,
            'Service ID': [service_id] * len(long_codes),  # Apply the service_id to all rows
            'Route ID': route_ids,
            'Direction ID': direction_ids
        })

        # Reorder the columns
        df = df[['Long Code', 'Service ID', 'Route ID', 'Direction ID']]

        # Process the Excel file and perform the lookup
        lookup_df = pd.read_excel(excel_file, header=1, usecols="E,BQ:CN")  # Columns E, BQ to CN
        lookup_df.columns = ['Long Code'] + list(range(24))  # Rename columns BQ to CN to 0-23

        # Convert 'Long Code' columns to string to ensure they can be merged
        df['Long Code'] = df['Long Code'].astype(str)
        lookup_df['Long Code'] = lookup_df['Long Code'].astype(str)

        # Merge the dataframes on 'Long Code'
        df = pd.merge(df, lookup_df, on='Long Code', how='left')

        # Fill NaN values with 0
        df.fillna(0, inplace=True)

        return df

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None



def to_json_pref_2(df):
    json_data = []
    trip_frequencies = {}

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        service_id = str(row['Service ID'])
        route_id = str(row['Route ID'])
        direction_id = str(row['Direction ID'])

        # Iterate through the time columns
        for col in df.columns:
            if col not in ['Service ID', 'Route ID', 'Direction ID', 'Long Code']:
                frequency = row[col]
                if frequency != 0:
                    hour = int(col)
                    timeband_from = '{:02d}:00'.format(hour)
                    timeband_to = '{:02d}:00'.format(hour + 1)

                    trip_entry = {
                        'conflicts': [],
                        'timeband': {
                            'from': timeband_from,
                            'to': timeband_to},
                        'retain': False,
                        'patterns': [direction_id],
                        'maximize': False,
                        'frequency': frequency
                    }

                    if service_id not in trip_frequencies:
                        trip_frequencies[service_id] = {}
                    if route_id not in trip_frequencies[service_id]:
                        trip_frequencies[service_id][route_id] = {}
                    if direction_id not in trip_frequencies[service_id][route_id]:
                        trip_frequencies[service_id][route_id][direction_id] = []

                    trip_frequencies[service_id][route_id][direction_id].append(trip_entry)

    # Construct JSON data from trip frequencies
    for service_id, service_data in trip_frequencies.items():
        json_trip_frequencies = {'trip_frequencies': {service_id: service_data}}
        json_data.append(json_trip_frequencies)

    return json_data



def to_json_pref_3(df):
    json_data = []
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        service_id = str(row['Service ID'])
        route_id = str(row['Route ID'])
        direction_id = str(row['Direction ID'])

        timebands = []

        # Iterate through the time columns
        for col in df.columns:
            if col not in ['Service ID', 'Route ID', 'Direction ID', 'Long Code']:
                frequency = row[col]
                if frequency != 0:
                    hour = int(col)
                    timeband_from = '{:02d}:00'.format(hour)
                    timeband_to = '{:02d}:00'.format(hour + 1)

                    timeband_entry = {
                        'enabled': True,
                        'timeband': {
                            'from': timeband_from,
                            'to': timeband_to},
                        'resolution': None,
                        'retain': False,
                        'patterns': [direction_id],
                        'routes': None,
                        'maximize': False,
                        'frequency': frequency,
                        'demand': None
                    }

                    timebands.append(timeband_entry)
        
        if timebands != []:
            trip_frequency_entry = {
                'trip_frequency': {
                    'timebands': timebands,
                    'route_id': route_id,
                    'direction_id': direction_id,
                    'is_route_group': False,
                    'services': [service_id]
                }
            }    

            json_data.append(trip_frequency_entry)

    return json_data



# Streamlit UI
st.title("Creating frequencies using JSON & MOT Excel")

# File uploaders
with st.container(border=True):
    json_file = st.file_uploader("Upload JSON File", type="json")
    service_name = st.text_input("Enter the service you would like to create the frequencies to", placeholder="Service name")
    st.write(f"Service name: **{service_name}**")

with st.container(border=True):
    excel_file = st.file_uploader("Upload Excel File", type="xlsx")

if json_file and excel_file:
    df = process_files(json_file, excel_file)
    if df is not None:
        st.success("Data processed successfully.")
        st.dataframe(df)
        with st.container(border=True):
            # Provide select box to choose which file to download
            option = st.selectbox("Which file type would you like to download?",
               ("JSON ver 2", "JSON ver 3", "Excel"),
               index=None,
               placeholder="Select file type",
            )
    
            filename = st.text_input("Output File Name", "processed_data")
            
            if option == 'Excel':
                # Convert DataFrame to a binary stream
                output = BytesIO()
                df.to_excel(output, index=False, engine='openpyxl')
                output.seek(0)
    
                st.write(f"The Excel file will be named: **{filename}.xlsx**")
                
                # Provide a download button for the resulting dataframe
                st.download_button(
                    label="Download Excel",
                    data=output,
                    file_name= f"{filename}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary"
                )
            
            if option == 'JSON ver 2':
                json_data = to_json_pref_2(df)
                json_str = json.dumps(json_data, indent=4)
                json_bytes = json_str.encode('utf-8')
    
                st.write(f"The JSON file will be named: **{filename}.txt**")
    
                # Provide a download button for the resulting dataframe
                st.download_button(
                    label="Download JSON as text file",
                    data=json_bytes,
                    file_name= f"{filename}.txt",
                    type="primary"
                )
    
            if option == 'JSON ver 3':
                json_data = to_json_pref_3(df)
                json_str = json.dumps(json_data, indent=4)
                json_bytes = json_str.encode('utf-8')
    
                st.write(f"The JSON file will be named: **{filename}.txt**")
    
                # Provide a download button for the resulting dataframe
                st.download_button(
                    label="Download JSON as text file",
                    data=json_bytes,
                    file_name= f"{filename}.txt",
                    type="primary"
                )

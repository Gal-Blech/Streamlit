import streamlit as st
import pandas as pd
import json
from io import BytesIO

# Ensure openpyxl is available
try:
    import openpyxl
except ImportError:
    st.error("The 'openpyxl' library is required to run this app. Please install it by running `pip install openpyxl`.")
    st.stop()

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
            if service.get('name') == 'SOS':
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

# Streamlit UI
st.title("JSON & MOT Excel to Arranged Excel")

# File uploaders
json_file = st.file_uploader("Upload JSON File", type="json")
excel_file = st.file_uploader("Upload Excel File", type="xlsx")

if json_file and excel_file:
    df = process_files(json_file, excel_file)
    if df is not None:
        st.success("Data processed successfully.")
        st.dataframe(df)

        # Convert DataFrame to a binary stream
        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        # Provide a download button for the resulting dataframe
        st.download_button(
            label="Download Excel",
            data=output,
            file_name="processed_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

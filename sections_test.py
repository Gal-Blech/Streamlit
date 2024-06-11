import streamlit as st

# Define the hierarchical choices using nested dictionaries
choices = {
    "apple": ["green", "red", "yellow"],
    "banana": ["green", "yellow"],
    "kiwi": {
        "softness": ["soft", "hard"],
        "hair": {
            "length": ["short", "long"],
            "color": ["light", "dark"]
        }
    }
}

# Function to generate unique keys for each dropdown set
def get_unique_key(base, index):
    return f"{base}_{index}"

# Function to create dropdowns in columns
def create_dropdowns(options, level=0, path=[], set_index=0):
    if level == 0:
        num_levels = 5  # Adjust this based on the maximum depth of your choices
        st.session_state[f'columns_{set_index}'] = st.columns(num_levels)
    
    cols = st.session_state[f'columns_{set_index}']
    with cols[level]:
        if isinstance(options, dict):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + list(options.keys()), key=get_unique_key(f"{'.'.join(path)}_level_{level}", set_index))
            if choice:
                path = path + [choice]
                st.session_state[f'path_{set_index}'] = path
                create_dropdowns(options[choice], level + 1, path, set_index)
        elif isinstance(options, list):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + options, key=get_unique_key(f"{'.'.join(path)}_level_{level}", set_index))
            if choice:
                path = path + [choice]
                st.write(f"Column's attribute will be: {'.'.join(path)}")
                st.session_state[f'path_{set_index}'] = path

# Initialize dropdowns
if 'dropdown_set_count' not in st.session_state:
    st.session_state['dropdown_set_count'] = 0

for i in range(st.session_state['dropdown_set_count'] + 1):
    with st.expander(f"Column {i + 1} choices", expanded=True):
        create_dropdowns(choices, level=0, path=[], set_index=i)

# Option to add more dropdown sets
if st.button("Add more dropdowns"):
    st.session_state['dropdown_set_count'] += 1
    st.experimental_rerun()

# Collect the final selected paths
selected_paths = []
for i in range(st.session_state['dropdown_set_count'] + 1):
    if f'path_{i}' in st.session_state:
        selected_paths.append('.'.join(st.session_state[f'path_{i}']))

# Display the final paths in a single-row table
if selected_paths:
    st.write("Selected Paths:")
    st.table([selected_paths])

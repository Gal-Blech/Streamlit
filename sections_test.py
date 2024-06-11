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

# Create columns for horizontal layout
def create_dropdowns(options, level=0, path=[], set_index=0):
    if level == 0:
        num_levels = 5  # Adjust this based on the maximum depth of your choices
        st.session_state[f'columns_{set_index}'] = st.columns(num_levels)
    
    cols = st.session_state[f'columns_{set_index}']
    with cols[level]:
        if isinstance(options, dict):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + list(options.keys()), key=get_unique_key(f"{'.'.join(path)}_level_{level}", set_index))
            if choice:
                create_dropdowns(options[choice], level + 1, path + [choice], set_index)
        elif isinstance(options, list):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + options, key=get_unique_key(f"{'.'.join(path)}_level_{level}", set_index))
            if choice:
                st.write(f"Column's attribute will be: {'.'.join(path + [choice])}")

# Initialize dropdowns
if 'dropdown_set_count' not in st.session_state:
    st.session_state['dropdown_set_count'] = 0

for i in range(st.session_state['dropdown_set_count'] + 1):
    create_dropdowns(choices, level=0, path=[], set_index=i)

# Option to add more dropdown sets
if st.button("Add more dropdowns"):
    st.session_state['dropdown_set_count'] += 1
    st.experimental_rerun()

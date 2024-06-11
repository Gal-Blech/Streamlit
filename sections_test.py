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

# Create columns for horizontal layout
def create_dropdowns(options, level=0, path=[]):
    if level == 0:
        num_levels = 5  # Adjust this based on the maximum depth of your choices
        st.session_state['columns'] = st.columns(num_levels)
    
    cols = st.session_state['columns']
    with cols[level]:
        if isinstance(options, dict):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + list(options.keys()), key=f"{'.'.join(path)}_level_{level}")
            if choice:
                create_dropdowns(options[choice], level + 1, path + [choice])
        elif isinstance(options, list):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + options, key=f"{'.'.join(path)}_level_{level}")
            
    st.write(f"Column's attribute will be: {'.'.join(path + [choice])}")

# Initialize dropdowns
create_dropdowns(choices)

# Option to add more dropdown sets
if st.button("Add more dropdowns"):
    st.write("Adding another set of dropdowns.")
    create_dropdowns(choices, level=0, path=[])

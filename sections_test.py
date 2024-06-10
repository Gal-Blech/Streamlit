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

# Recursive function to generate dropdowns
def create_dropdowns(options, level=0, prev_selection=None):
    if isinstance(options, dict):
        choice = st.selectbox(f"Level {level + 1} choices", [""] + list(options.keys()), key=f"level_{level}")
        if choice:
            with st.beta_expander(f"Level {level + 1} - {choice}", expanded=True):
                create_dropdowns(options[choice], level + 1, choice)
    elif isinstance(options, list):
        choice = st.selectbox(f"Level {level + 1} choices", [""] + options, key=f"level_{level}")
        if choice:
            st.write(f"Selected at level {level + 1}: {choice}")

# Create columns for horizontal layout
num_levels = 5  # Adjust this based on the maximum depth of your choices
columns = st.beta_columns(num_levels)

with columns[0]:
    create_dropdowns(choices)

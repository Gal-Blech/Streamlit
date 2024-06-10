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
def create_dropdowns(options, level=0, columns=None):
    if columns is None:
        columns = st.columns(5)  # Adjust this based on the maximum depth of your choices

    if isinstance(options, dict):
        choice = columns[level].selectbox(f"Level {level + 1} choices", [""] + list(options.keys()), key=f"level_{level}")
        if choice:
            create_dropdowns(options[choice], level + 1, columns)
    elif isinstance(options, list):
        choice = columns[level].selectbox(f"Level {level + 1} choices", [""] + options, key=f"level_{level}")
        if choice:
            st.write(f"Selected at level {level + 1}: {choice}")

# Initialize the recursive dropdowns
create_dropdowns(choices)

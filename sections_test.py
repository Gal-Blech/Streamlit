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
def create_dropdowns(options, level=0):
    cols = st.columns(len(options))
    with cols[level]:
        if isinstance(options, dict):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + list(options.keys()), key=f"level_{level}")
            if choice:
                create_dropdowns(options[choice], level + 1)
        elif isinstance(options, list):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + options, key=f"level_{level}")
            if choice:
                st.write(f"Selected at level {level + 1}: {choice}")

# Create columns for horizontal layout
create_dropdowns(choices)

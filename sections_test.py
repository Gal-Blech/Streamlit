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
def create_dropdowns(options, level=0, path=""):
    cols = st.columns(1)
    with cols[0]:
        if isinstance(options, dict):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + list(options.keys()), key=f"{path}level_{level}")
            if choice:
                create_dropdowns(options[choice], level + 1, path + choice + ".")
        elif isinstance(options, list):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + options, key=f"{path}level_{level}")
            if choice:
                st.write(f"Column's attribute will be: {path}{choice}")

# Create columns for horizontal layout
create_dropdowns(choices)

# Option to add more dropdown sets
if st.button("Add more dropdowns"):
    st.write("Adding another set of dropdowns.")
    create_dropdowns(choices, level=0, path="")

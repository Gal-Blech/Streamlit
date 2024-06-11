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

# Recursive function to generate dropdowns in columns
def create_dropdowns(options, level=0, path=[]):
    if isinstance(options, dict):
        cols = st.columns(5)  # Adjust the number of columns if needed
        with cols[level % 5]:  # Ensure we stay within the column range
            choice = st.selectbox(f"Level {level + 1} choices", [""] + list(options.keys()), key=f"{'.'.join(path)}_level_{level}")
            if choice:
                create_dropdowns(options[choice], level + 1, path + [choice])
    elif isinstance(options, list):
        cols = st.columns(5)  # Adjust the number of columns if needed
        with cols[level % 5]:  # Ensure we stay within the column range
            choice = st.selectbox(f"Level {level + 1} choices", [""] + options, key=f"{'.'.join(path)}_level_{level}")
            if choice:
                st.write(f"Column's attribute will be: {'.'.join(path + [choice])}")

# Create the initial set of dropdowns
create_dropdowns(choices)

# Option to add more dropdown sets
if st.button("Add more dropdowns"):
    st.write("Adding another set of dropdowns.")
    create_dropdowns(choices, level=0, path=[])

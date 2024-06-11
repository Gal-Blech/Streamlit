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

# Recursive function to generate dropdowns and collect the final path
def create_dropdowns(options, level=0, path=[]):
    cols = st.columns(5)  # Adjust the number of columns if needed
    with cols[level % 5]:
        if isinstance(options, dict):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + list(options.keys()), key=f"{'.'.join(path)}_level_{level}")
            if choice:
                return create_dropdowns(options[choice], level + 1, path + [choice])
        elif isinstance(options, list):
            choice = st.selectbox(f"Level {level + 1} choices", [""] + options, key=f"{'.'.join(path)}_level_{level}")
            if choice:
                return path + [choice]
    return path

# Function to initialize and add more dropdown sets
def add_dropdown_set():
    path = create_dropdowns(choices)
    if path:
        st.write(f"Column's attribute will be: {'.'.join(path)}")

# Initialize dropdowns
add_dropdown_set()

# Option to add more dropdown sets
if st.button("Add more dropdowns"):
    st.write("Adding another set of dropdowns.")
    add_dropdown_set()

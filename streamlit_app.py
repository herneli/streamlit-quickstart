import streamlit as st
import json

# Function to validate if a value is JSON stringified


def is_json_stringified(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = json.loads(value)
        # Check if the parsed value is a JSON object or array
        return isinstance(parsed, (dict, list))
    except (ValueError, TypeError):
        return False

# Function to validate JSON keys with "richtext"


def validate_richtext_keys(json_data):
    errors = []

    def recursive_check(data, path=""):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                if "richtext" in key.lower() and not is_json_stringified(value):
                    errors.append(
                        f"Invalid JSON stringified value at key: {new_path}")
                if isinstance(value, (dict, list)):
                    recursive_check(value, new_path)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_path = f"{path}[{index}]"
                if isinstance(item, (dict, list)):
                    recursive_check(item, new_path)

    recursive_check(json_data)
    return errors


# Streamlit app
st.title("JSON Richtext Validator")
st.write("Upload a JSON file and validate that all keys containing 'richtext' have JSON stringified values.")

# File uploader
uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

if uploaded_file is not None:
    try:
        # Read and parse the uploaded JSON file
        json_data = json.load(uploaded_file)

        # Validate the JSON
        st.write("### Uploaded JSON:")
        st.json(json_data)

        errors = validate_richtext_keys(json_data)

        # Display validation results
        if errors:
            st.error("Validation Errors Found:")
            for error in errors:
                st.write(f"- {error}")
        else:
            st.success(
                "All 'richtext' keys have valid JSON stringified values!")

    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid JSON file.")

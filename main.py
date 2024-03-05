import streamlit as st
from config_diff import get_config_h, get_diff
from rich.markdown import Markdown
from rich import print as rprint
import difflib

# Set page configuration
st.set_page_config(page_title="Config Diff", page_icon=":smiley:", layout="wide")

# Display title and description
st.title("Octopus Buildbot Config Checker")
st.write("This is a simple app to compare two `config.h` files from Octopus buildbot runs.")
st.write("- [Octopus Buildbot](https://www.octopus-code.org/buildbot)")
st.write("- [Octopus-code](https://www.octopus-code.org)")
st.write("Please enter the URLs of the two `config.h` files to compare.")

# Display example URLs
st.write("Example URLs:")
st.write("- [Builder 1](https://www.octopus-code.org/buildbot/#/builders/5/builds/611)")
st.write("- [Builder 2](https://www.octopus-code.org/buildbot/#/builders/203/builds/13)")
st.write("Click the 'Compare' button to compare the two files.")
st.write(" You can also pass the URLs as query parameters in the URL. For example:")
st.write("`http://octopus-config-checker.streamlit.app/?url1=https://www.octopus-code.org/buildbot/builders/5/builds/611&url2=https://www.octopus-code.org/buildbot/builders/203/builds/13`")
st.info("Note: The `#` directory in the URLs have been removed.")
st.write("# Inputs")
# Get user input for URLs and builder names
cols = st.columns(2)
col1, col2 = cols
with col1:
    url1 = st.text_input("Enter the URL of the first `config.h` file", value=st.query_params.get("url1", "https://www.octopus-code.org/buildbot/#/builders/5/builds/611"))
    name1 = st.text_input("Builder name", value=st.query_params.get("name1", "EB"))
with col2:
    url2 = st.text_input("Enter the URL of the second `config.h` file", value=st.query_params.get("url2", "https://www.octopus-code.org/buildbot/#/builders/203/builds/13"))
    name2 = st.text_input("Builder name", value=st.query_params.get("name2", "SPACK"))

# Compare the two files when the "Compare" button is clicked
if st.button("Compare"):
    # Display a spinning wheel while fetching the two files
    with st.spinner("Fetching the two files.."):
        config_h1 = get_config_h(url1)
        config_h2 = get_config_h(url2)

    # Compare the two files and display the differences
    with st.spinner("Comparing the two files.."):
        st.write("Comparing the two files")
        diff = difflib.unified_diff(
            config_h1.split("\n"),
            config_h2.split("\n"),
            name1,
            name2
        )
        diffy = "\n".join(list(diff))
        diffy_body = f"""
```diff
{diffy}
```
    """

    st.write("Displaying the differences")
    st.markdown(diffy_body)

    st.write("Done")

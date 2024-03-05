import streamlit as st
from config_diff import get_config_h, get_diff
from rich.markdown import Markdown
from rich import print as rprint
import difflib

# Take input of thw two urls and optionally the file names (default left and right)
# then print the diffs in the screen
st.set_page_config(page_title="Config Diff", page_icon=":smiley:", layout="wide")
st.title("Config Diff")
st.write("This is a simple app to compare two config.h files from buildbot runs")
st.write("Please enter the urls of the two config.h files to compare")
st.write("eg https://www.octopus-code.org/buildbot/#/builders/203/builds/13")

cols = st.columns(2)
col1, col2 = cols
with col1:
    url1 = st.text_input("Enter the url of the first config.h file", value="https://www.octopus-code.org/buildbot/#/builders/5/builds/611")
    name1 = st.text_input("Builder name", value="EB")
with col2:
    url2 = st.text_input("Enter the url of the second config.h file", value="https://www.octopus-code.org/buildbot/#/builders/203/builds/13")
    name2 = st.text_input("Builder name", value="SPACK")

if st.button("Compare"):
    # Display a spinning wheel while comparing the two files
    with st.spinner("Fetching the two files.."):

        config_h1 = get_config_h(url1)
        config_h2 = get_config_h(url2)

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

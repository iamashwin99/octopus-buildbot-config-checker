import streamlit as st
from config_diff import get_config_h, get_diff
from rich.markdown import Markdown
from rich import print as rprint
import difflib

# Set page configuration
st.set_page_config(page_title="Config Diff", page_icon=":smiley:", layout="wide")
web_url="http://octopus-config-checker.streamlit.app/"
# Display title and description
st.title("Octopus Buildbot Config Checker")
with st.expander("Instructions"):
    st.write(
        "This is a simple app to compare two `config.h` files from Octopus buildbot runs."
    )
    st.write("- [Octopus Buildbot](https://www.octopus-code.org/buildbot)")
    st.write("- [Octopus-code](https://www.octopus-code.org)")
    st.write("Please enter the URLs of the two `config.h` files to compare.")

    # # Display example URLs
    # st.write("Example URLs:")
    # st.write("- [Builder 1](https://www.octopus-code.org/buildbot/#/builders/5/builds/611)")
    # st.write(
    #     "- [Builder 2](https://www.octopus-code.org/buildbot/#/builders/203/builds/13)"
    # )
    st.write("Click the 'Compare' button to compare the two files.")
    st.write(" You can also pass the URLs as query parameters in the URL. For example:")
    st.write(
        "`http://octopus-config-checker.streamlit.app/?url1=https://www.octopus-code.org/buildbot/builders/5/builds/611&url2=https://www.octopus-code.org/buildbot/builders/203/builds/13`"
    )
    st.info("Note: The `#` directory in the URLs have been removed.")
st.write("# Inputs")

# Get user input for URLs and builder names

params_set = st.query_params.get("url1") or st.query_params.get("url2")
url1 = st.query_params.get(
    "url1", "https://www.octopus-code.org/buildbot/#/builders/5/builds/611"
)
url2 = st.query_params.get(
    "url2", "https://www.octopus-code.org/buildbot/#/builders/203/builds/13"
)
name1 = st.query_params.get("name1", "EB")
name2 = st.query_params.get("name2", "SPACK")


# Display user input fields
cols = st.columns(2)
col1, col2 = cols
# Show warning if defaults are loaded from URL parameters
if params_set:
    st.warning("Defaults loaded from URL parameters.")
    # Display a spinning wheel while fetching the two files
with col1:
    url1 = st.text_input("Enter the builder URL of the first `config.h` file", value=url1)
    name1 = st.text_input("Builder name", value=name1)
with col2:
    url2 = st.text_input("Enter the builder URL of the second `config.h` file", value=url2)
    name2 = st.text_input("Builder name", value=name2)

# Compare the two files when the "Compare" button is clicked
if st.button("Compare") or params_set:

    # write the url of the webapp with params that can be shared
    st.write("You can share this result via url:")
    st.code(f"{web_url}?url1={url1.replace("#" , '')}&url2={url2.replace("#" , '')}&name1={name1}&name2={name2}")

    with st.spinner("Fetching the two files.."):
        config_h1 = get_config_h(url1)
        config_h2 = get_config_h(url2)

    # Compare the two files and display the differences
    with st.spinner("Comparing the two files.."):
        st.write("Comparing the two files")
        diff = difflib.unified_diff(
            config_h1.split("\n"), config_h2.split("\n"), name1, name2
        )
        diffy = "\n".join(list(diff))
        diffy_body = f"""
```diff
{diffy}
```
    """

    st.write("Displaying the differences")
    # st.markdown(diffy_body)
    st.code(diffy, language="python", line_numbers=True)
    st.write("Done")

import json
import requests
import re
import difflib

from rich.markdown import Markdown
from rich import print as rprint
import inspect

def get_config_h(build_url:str)->str:
    """
    Return the contents of the config.h file from the buildbot

    Assuming build_url is of the form:
    builder_url = "https://www.octopus-code.org/buildbot/#/builders/144/builds/194"
    return the contents of the config.h file
    by first finding the buildid then the stepid then the logid
    """
    # get builders_id and builds_id
    # match for the pattern: builders/144 from that get the 144 for builders_id
    builders_id = re.search(r'builders/(\d+)', build_url).group(1)
    # match for the pattern: builds/194 from that get the 194 for builds_id
    builds_id = re.search(r'builds/(\d+)', build_url).group(1)
    # get the buildbot_website_url from the build_url for eg www.octopus-code.org
    buildbot_website_url = re.search(r'https?:\/\/([^\/#?]+)', build_url).group(1)

    # get buildid
    buildid_reponse = requests.get(f"http://{buildbot_website_url}/buildbot/api/v2/builders/{builders_id}/builds/{builds_id}")
    buildid = json.loads(buildid_reponse.content)['builds'][0]['buildid']  # buildid = 61409

    # get stepid  from 'https://www.octopus-code.org/buildbot/api/v2/builds/61409/steps/5'
    stepid_response = requests.get(f"http://{buildbot_website_url}/buildbot/api/v2/builds/{buildid}/steps/5")
    stepid = json.loads(stepid_response.content)['steps'][0]['stepid'] # stepid = 568186

    # get logid from https://www.octopus-code.org/buildbot/api/v2/steps/568186/logs/config_h
    logid_response = requests.get(f"http://{buildbot_website_url}/buildbot/api/v2/steps/{stepid}/logs/config_h")
    logid = json.loads(logid_response.content)['logs'][0]['logid'] # logid = 709753

    # get config.h from 'https://www.octopus-code.org/buildbot/api/v2/logs/709753/contents'
    config_h_response = requests.get(f"http://{buildbot_website_url}/buildbot/api/v2/logs/{logid}/contents")
    config_h = json.loads(config_h_response.content)["logchunks"][0]["content"]
    return config_h.replace('o\n','\n').replace('\no','\n')


def get_diff(str_old:str, str_new:str,str_old_name="old",str_new_name="new"):
    diff = difflib.unified_diff(
                str_old.split("\n"),
                str_new.split("\n"),
                str_old_name,
                str_new_name
            )
    diffy = "\n".join(list(diff))

    diffy_body = Markdown(
    f"""
```diff
{diffy}
```
    """,
    code_theme="vim",
    )

    return diffy_body

def get_config_h_diff(build_url1:str,build_url2:str,build_url1_name="old",build_url2_name="new"):
    config_h1 = get_config_h(build_url1)
    config_h2 = get_config_h(build_url2)
    return get_diff(config_h1,config_h2,build_url1_name,build_url2_name)
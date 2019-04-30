#!/usr/bin/env python
import requests
import json
from requests.auth import HTTPBasicAuth
from tower_cli import conf, get_resource
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_job_template(template="Network-Validate-Traffic",
                     host_name='127.0.0.1',
                     user_name='admin', pass_word='admin'):
    with conf.settings.runtime_values(host=host_name, username=user_name,
                                      password=pass_word, verify_ssl=False):
        res = get_resource('job_template')
        result = res.list(all_pages=True)
    job_templates = result.get('results')
    for job_template in job_templates:
        if job_template.get('name').lower() == template.lower():
            return job_template.get('url')


def launch_job(template_uri, user_input, host_name='127.0.0.1', user_name='admin', pass_word='admin'):
    url = "https://" + host_name + template_uri + "launch/"
    auth = HTTPBasicAuth(user_name, pass_word)
    headers = {'content-type': 'application/json'}
    payload = json.dumps(user_input)
    response = requests.post(url, headers=headers, data=payload, auth=auth,
                             verify=False)
    return(response.text)

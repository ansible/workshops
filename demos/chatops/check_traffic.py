from flask import Flask, request, make_response
import json
from helper import validate_input
from tower_api import launch_job, get_job_template
from slackclient import SlackClient
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# Your app's Slack bot user token
SLACK_VERIFICATION_TOKEN = "blah"
SLACK_BOT_TOKEN = ""
TOWER_HOSTNAME = ''
TOWER_USERNAME = 'admin'
TOWER_PASSWORD = 'ansible'

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask web server for incoming traffic from Slack
app = Flask(__name__)
USER_INPUT = {}

@app.route("/acl", methods=["POST"]) #slash_cmd
def validate():
    user_id = request.form["user_id"]
    data = request.form.items()
    print(data)
    print()
    open_dialog = slack_client.api_call("dialog.open",
                                        trigger_id=request.form["trigger_id"],
                                        dialog={
                                            "title": "Validate network traffic",
                                            "callback_id": "Network-Validate-Traffic",
                                            "elements": [
                                                {"label": "Source network",
                                                 "type": "text",
                                                 "name": "source_network",
                                                 "placeholder": "192.168.0.0/24"},
                                                {"label": "Destination network",
                                                 "type": "text",
                                                 "name": "destination_network",
                                                 "placeholder": "10.168.32.0/24"},
                                                {"label": "protocol",
                                                 "type": "text",
                                                 "name": "protocol",
                                                 "placeholder": "tcp/udp/ip"},
                                                {"label": "destination port",
                                                 "type": "text",
                                                 "name": "port",
                                                 "placeholder": "8443"},
                                                {"label": "permitted or denied?",
                                                 "type": "text",
                                                 "name": "action",
                                                 "placeholder": "permit"}
                                            ]
                                          }
                                        )
    return make_response("",200)


def call_tower(user_input, job_template):
    template_name = job_template
    login_creds = dict(host_name=TOWER_HOSTNAME, user_name=TOWER_USERNAME, pass_word=TOWER_PASSWORD)
    template_uri = get_job_template(template_name, **login_creds)
    return launch_job(template_uri, user_input, **login_creds)

@app.route("/interactive-component", methods=["POST"]) #icomponent
def dialog():
    user_input = {}
    message = json.loads(request.form["payload"])
    job_template = message['callback_id']
    channel_id = message['channel']['id']
    user = message['user']['name']
    return_data = ":white_check_mark: Received @{} ! I'm working on it!".format(user)
    result = slack_client.api_call(
     "chat.postMessage",
     channel=channel_id,
     ts=message["action_ts"],
     text=return_data,

        )

    if message['callback_id'] == 'Network-Validate-Traffic':
        user_input['extra_vars'] = validate_input(message['submission'])
        user_input['extra_vars']['slack_user'] = user

    # Execute Job Template
    tower_response = call_tower(user_input, job_template)
    slack_client.api_call(
     "chat.postMessage",
     channel=channel_id,
     text = "I've fired off " + job_template + " Ansible Tower job for you"
     )
    return make_response("", 200)

if __name__ == "__main__":
    #Add check's for TOWER_VARS & SLACK_VARS being declared
    app.run(debug=True, host='0.0.0.0', port='8888')

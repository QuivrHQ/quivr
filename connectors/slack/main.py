import re
import os
from logger import logger

import requests

from slack_bolt import App
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

slack_bot_token = os.getenv("SLACK_BOT_TOKEN", "")
slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET", "")
slack_port = int(os.getenv("SLACK_PORT", 5566))
quivr_token = os.getenv("QUIVR_TOKEN", "")
quivr_chat_id = os.getenv("QUIVR_CHAT_ID", "")
quivr_brain_id = os.getenv("QUIVR_BRAIN_ID", "")
quivr_url = (
    os.getenv("QUIVR_URL", "https://api.quivr.app")
    + f"/chat/{quivr_chat_id}/question?brain_id={quivr_brain_id}"
)

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + quivr_token,
}

# Slack Bolt
app = App(token= slack_bot_token, signing_secret = slack_signing_secret)

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your _App's Home tab_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
          }
        ]
      }
    )

  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")
    
# Slack app_mention
@app.event("app_mention")
def handle_mention(event, say):
    if 'thread_ts' in event:
        ts = event["thread_ts"]
    else:
        ts = event["ts"]
    reply_text = Slack().handle(event)
    say(text=f"{reply_text}", thread_ts=ts)

@app.event("message")
def handle_message_events(event, body, say, logger):
    logger.info(body)
    text="I'm Quiv's bot and can answer any question. Please ask your question."
    if 'thread_ts' in event:
        ts = event["thread_ts"]
    else:
        ts = event["ts"]
    say(text=f"{text}", thread_ts=ts)

class Slack():
    def startup(self,say):
        app.start(port=slack_port)
        text="I'm Quiv's bot and can answer any question. Please ask your question.",
        say(text=f"{text}")

    def handle(self, event):
        context = dict()
        if 'thread_ts' in event:
            ts = event["thread_ts"]
        else:
            ts = event["ts"]
        context['from_user_id'] = str(ts)
        plain_text = re.sub(r"<@\w+>", "", event["text"])
        return self.build_reply_content(plain_text, context)
    
    def build_reply_content(self, query, context=None):
        return self.fetch_reply_content(query, context)

    # async def build_reply_stream(self, query, context=None):
    #     async for final,response in self.fetch_reply_stream(query, context):
    #         yield final,response
  
    def fetch_reply_content(self, query, context):
      user_message = query
      response = requests.post(
          quivr_url, headers=headers, json={"question": user_message}
      )
      if response.status_code == 200:
          quivr_response = response.json().get(
              "assistant", "Sorry, I couldn't understand that."
          )
          return quivr_response
      else:
          # Log or print the response for debugging
          print(f"Error: {response.status_code}, {response.text}")
          return quivr_response


    # async def fetch_reply_stream(self, query, context):
    #     econtext = PluginManager().emit_event(EventContext(
    #         Event.ON_BRIDGE_HANDLE_CONTEXT, {'context': query, 'args': context}))
    #     type = econtext['args'].get('model') or config.conf().get("model").get("type")
    #     query = econtext.econtext.get("context", None)
    #     reply = econtext.econtext.get("reply", "无回复")
    #     bot = model_factory.create_bot(type)
    #     if not econtext.is_pass() and query:
    #         async for final, response in bot.reply_text_stream(query, context):
    #             yield final, response
    #     else:
    #         yield True, reply

if __name__ == "__main__":
    # Slack.startup()
    app.start(port=slack_port)
    text="I'm Quiv's bot and can answer any question. Please ask your question.",
    # app.say(text=f"{text}")

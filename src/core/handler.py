from .manager import Manager
from ..apps.LeaveTracker.leave_tracker import LeaveTracker
from .paLM2 import paLM2
from .Llama2 import Llama2
import spacy

class BotHandler(Manager):
    def __init__(self):
        super().__init__()
        self.leaves_tracker = LeaveTracker()
        self.nlp = spacy.load("en_core_web_sm")
        self.paLM2 = paLM2() # <- This is the paLM2, Google's Pathways Language Model.
        self.Llama2 = Llama2() # <- This is the Llama2, Meta's Large Language Model Meta AI


    async def handler(self, context, model="paLM2"):
        user_id, text, channel_id = context["event"]["user"], context["event"]["text"], context["event"]["channel"]
        text = text.replace('<@U060PP7BB1N>', 'OptiBot!')

        if model == "paLM2":
            paLM_reply = await self.paLM2.req(text, user_id)
            paLM_reply = paLM_reply.replace('OptiBot:', '')
            
            match paLM_reply.split(',')[0]:
                case "leaves":
                    self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text="Please wait, I am fetching the details :hourglass_flowing_sand:")
                    table, status = await self.leave_tracker.get_leaves()
                    if status == 200:
                        self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text=table)
                    else:
                        self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text="Sorry, I am unable to fetch the details :disappointed:")
                case "add leave":
                    self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text="Add Leave function called")
                case _:
                    paLM_reply = await self.markdown_to_slack(paLM_reply)
                    await self.SLACK_CLIENT.chat_postMessage(channel=channel_id, text=paLM_reply)

            self.SLACK_CLIENT.chat_postMessage(channel=channel_id, text=paLM_reply)
        elif model == "Llama2":
            print("Llama2 is not ready yet.")
        else:
            print("Model not found.")


    # async def handler(self, context):
    #     print("BotHandler called")
    #     leave_tracker = LeaveTracker()

    #     user_id, text, channel_id = context["event"]["user"], context["event"]["text"], context["event"]["channel"]
    #     nlp_doc = self.nlp(text)
    #     isGreet, greet = await self.is_greeting(text)
    #     if isGreet: 
    #         msg = await self.greet_template(user_id, greet) if bool(greet) else await self.greet_template(user_id)
    #         self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text=msg)
        
    #     for token in nlp_doc:

    #         if token.text.lower() == "leaves" or token.text.lower() == "leave": # <- To get all leaves
    #             self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text="Please wait, I am fetching the details :hourglass_flowing_sand:")
    #             table, status = await leave_tracker.get_leaves()
    #             if status == 200:
    #                 self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text=table)
    #             else: 
    #                 self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text="Sorry, I am unable to fetch the details :disappointed:")

    #         if token.text.lower() == "add":    # <- To add a person into the list
    #             self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text="Add Member function called")

    #         if token.text.lower() == "remove": # <- To remove a person from the list
    #             self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text="Remove Member function called")
                
    #         if token.text.lower() == "apply":  # <- To apply leave
    #             self.SLACK_CLIENT.chat_postMessage( channel=channel_id, text="Apply Leave function called")
    #             break


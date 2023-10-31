from os import getenv
import hashlib
import spacy
import slack
import hmac
import re

class Manager:
    def __init__(self):
        self._handlers = []
        self.SIGNING_SECRET = getenv('SIGNING_SECRET')
        self.SLACK_CLIENT = slack.WebClient(token=getenv('SLACK_TOKEN'))
        self.APP_SCRIPT_URL = getenv('APP_SCRIPT_URL')
        self.NLP_EN = spacy.load("en_core_web_sm")
        self.training_chunk = list()
        self.raw_training_data = {
            "training_chunks": {
                "CALO-7vXLH6v47vUx79rJONUghbOapGk1OH3xPjgg6c=":"gAAAAABlP3-yl2XhrKQ6NTnkYCBKFAtAWrU4DeY-SqjvdpvGNvX8k28OzaEcwAZqxwKIa5btGrPvNnJ7UMRVyqYAjw38NSrgSmbTKbZE9Z5d24D9uIS9PFZxoUQf6n1USePI7sYdyNPJMNSwWrSRnXFmW8qJkO428hHyStZuqsXYJUpwslgJmhetOHhYoRSLXQaIHnWxXLWIx9_ePaYoGkfTOr2F3Rd3Dyu68sVmd3r-YiAAwwkmlms=",
                "zXvhP7K2ev6M7RJeg1J3hmzE7vLGr_Ahga5GneY8kDI=":"gAAAAABlP4BkUAE5WG75K4g9P9YJIhjOBwf-Ei9NS99h-jrc-8-lwa-BuUPdgquBWvLhuI1paq6dDVGzvSkwxQ12gpS2aA8M4gl2WINnJBY_doJOhI9BriX6A9qv7KLIOJ___Ae1rKl-NdvWmwJGhTqMgpzGbcd9FqJ-xXDBnLTDd_ZdfmHMN7JcrsyQzcBQQcHmb7mm4RDsCPEWAbO3yDr-szka0XZWy2hyz63xtX5L9kGbn3dx5qXzRqndkUTwQW2iH9XuEap2c5482aF69kGuPDUPBJfumFVRmqkWVAY8XlHeifMZlXBFomZ3CahaKKEwn64SKZB5s2pefxyg7U0MzyS0dgPEusBAj4GKDNWQj6-HMHtsyAU3sRWislxIiaaaPPbzn98C3UiKcMUW6rcM_A9d61Hgd2YOVG1mMzEmpGe9S-ATQDzOxG9Mt3l3P3ZkrxsdpVeaoh1JpNUNkIVG96HRVaxHVQ99wWP55zgds_bjDBZldAqjJw8KNzYZmsjpVwzM-tJDt73MWC_dfWfZ_AIUkJyVF9d66W5drmtObww1Y_xQLagLEnBEaEpAneAxanWwRL_-JbBeYPoVHxAzn3am7OAbXw==",
                "eYZL3bne-IzyyhXMaGosZ4rSNopSzifBfoX8n_6zeAI=":"gAAAAABlP4RbqYTbLk5vnwNRFZ8Qo81Y95UjSm8QPOOySc3b3V3hiUfvTC7xXHXFCulhXiYe3JHozs7o-NVbPkwmmPlJkIvHbXtCh2VVE8MSIik_IUBN-ScmGx-bUT1oeg-MO9vU4CshX0LC0HamLoLmIFYTCJ11npT8P2mQdbvaLpoPchOg9tSDE_PTD7b_W667Jeest0a2H-18lWqMVu40b4UFo_MTsLn9PjxpKnDxlO60f8bURHRrgnPnnZTLJm7o1HXPVRti1ZKrv4M5X3B1V-xnFMqP9pNZlO7NomHWLSWeaOasy3g5QKIQw1XgyYgXWBBA5TgjiHJW8IO0EjOqrDj_ywyIZiXZ4xH7nV-9B_R5yhbLbOOmF1n0GI8QrydfgpzuScJUEJva59AoGDP6UCvly103Bfi8e4qaAw1cFJ64SVl75hhMAP6YuX2xn-Nd3U63grpVlXdc2ox160Pc0gTLW1ZGbU305BFsh1cv2yD8DNL8dNEDpyYDmTKdXgpA0HE2lCW6FzuSk91hQb1XvdlWTsJ3OLL9jRJYMYtXk9cqOlldHQw="
            }
        }

    def verify_slack_signature(self, data: bytes, timestamp: str, slack_signature: str) -> bool:
        """Verify the Slack request signature."""
        basestring = f"v0:{timestamp}:{data.decode('utf-8')}"
        my_signature = 'v0=' + hmac.new(
            bytes(self.SIGNING_SECRET, 'latin-1'),
            msg=bytes(basestring, 'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(my_signature, slack_signature)
    
    async def markdown_to_slack(self, text: str) -> str:
        REGEX_REPLACE = (
            (re.compile('^- ', flags=re.M), '• '),
            (re.compile('^  - ', flags=re.M), '  ◦ '),
            (re.compile('^    - ', flags=re.M), '    ⬩ '),
            (re.compile('^      - ', flags=re.M), '    ◽ '),
            (re.compile('^#+ (.+)$', flags=re.M), r'*\1*'),
            (re.compile('\*\*'), '*'),
            (re.compile(r'\[(.+)\]\((.+)\)'), r'\1: \2'),
        )
        for regex, replacement in REGEX_REPLACE:
            text = regex.sub(replacement, text)
        return text
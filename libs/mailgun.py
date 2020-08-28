import os
from requests import post, Response
from typing import List

class MailGun:
    MailGun_Domain = os.environ.get("MailGun_Domain")
    MailGun_API_KEY = os.environ.get("MailGun_API_KEY")
    
    From_Title = "To-Do List REST API"
    From_Email = "no-reply@sandboxd016a7154d0e4e368d89f8a4cf3a4487.mailgun.org"

    @classmethod
    def send_email(cls, email: List[str], subject, text, html) ->Response:
        
        if cls.MailGun_API_KEY is None:
            return {'msg': "Failed to load the MailGun API Key"}
        
        if cls.MailGun_Domain is None:
            return {'msg': "Failed to load the MailGun Domain"}

        response = post(
            f"https://api.mailgun.net/v3/{cls.MailGun_Domain}/messages",
            auth = ("api", cls.MailGun_API_KEY),
            data= {
                "from": f"{cls.From_Title}<{cls.From_Email}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

        if response.status_code != 200:
            return {'msg': "Error, confirmation email not sent."}
        
        return response
from openaiIO import Context
from typing import List,Dict
from .softbots import NameGenerator, PersonalityTraits,prompts
from .employee_interface import IAskable
from dbio import MailIO
from datetime import datetime
from threading import Thread
import time

class Staff(IAskable):
    _max_id: int = 0
    _logs = []
    staff_list:'Dict[Staff]' = {}
    is_active = False
    time_checked_mails = None

    def __init__(
        self, traits: PersonalityTraits = None
    ) -> None:
        Staff._max_id += 1
        self.id = Staff._max_id
        self.name = NameGenerator.generate() + str(self.id)
        self.context = Context(self.name, f"Your name is {self.name}.")

        if traits:
            self.traits = traits
            self.context.post_instructions(traits.get_instructions())
        
        self.context.post_instructions(prompts.Prompts.GetPrompts(__class__.__name__))

        Staff.staff_list[self.name] = self

    def add_instructions(self, instructions: str):
        self.context.post_instructions(instructions)

    def ask(self, message: str) -> str:
        print(str(self))
        return self.context.post_message_with_function_calling(message, self)

    def activate(self):
        self.is_active = True
        self.thread = Thread(target=self.exec_tasks)
        self.thread.start()

    def deactivate(self):
        self.is_active = False
        self.send_mail("all","I am currently waiting. If you have a task that I can do, please request it.")

    def exec_tasks(self):
        self.add_instructions("Read your mails and do your tasks.")
        while self.is_active:
            # mails = self.get_new_mails()
            # if len(mails) > 0:
            #     mails_str = str([str(mail) for mail in mails])
            #     self.ask("Notification: You have new mails!\n\n"+mails_str)
            # else:
            #     time.sleep(30)
            self.ask("Now let's get on with the next task!")

    def send_mail(self, to: str, content: str):
        mail = MailIO()
        mail.send_mail(self.name, to , content)

    def get_mails(self):
        return MailIO.get_mails(self.name)
    
    def get_new_mails(self):
        new_mails = MailIO.get_new_mails(self.name,self.time_checked_mails)
        self.time_checked_mails = datetime.now()
        return new_mails

    def get_last_message(self):
        return self.context.get_last_message()

    def __str__(self):
        return f"Name:{self.name}"
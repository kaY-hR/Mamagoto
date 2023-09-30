import openai
from openai import error
from dbio import LogIO
import json
from function_manager import FunctionManager
import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import virtual_employee.staff

class Context:
    @staticmethod
    def log(speaker: str, listener: str, message: str):
        LogIO.add(speaker, listener, message)

    def __init__(self, name: str, init_system_instructions: str) -> None:
        self.raw_context = openaiIO.init_context(init_system_instructions)
        self.name = name
        Context.log("system", self.name, init_system_instructions)

    def post_instructions(self, system_instructions: str):
        self.raw_context = openaiIO.post_context(self.raw_context, system_instructions)
        Context.log("system", self.name, system_instructions)

    def post_message(self, message: str):
        self.raw_context = openaiIO.post_message_without_function_calling(self.raw_context, message)
        Context.log("system", self.name, message)
        Context.log(self.name, "all", self.get_last_message())
        return self.get_last_message()

    def post_message_with_function_calling(self, message: str, staff:'virtual_employee.staff.Staff'):
        
        Context.log("system", self.name, message)
        self.raw_context = openaiIO.post_message_with_fucntion_calling(self.raw_context, message)

        if self.raw_context[-1].get("function_call"):
            function_name = self.raw_context[-1]["function_call"]["name"]

            json_arguments = json.loads(self.raw_context[-1]["function_call"]["arguments"])
            Context.log(self.name, "function", f"function_name:{function_name},args:{str(json_arguments)}")
            function_manager_response = FunctionManager.exec_func(function_name,json_arguments,staff)

            self.raw_context.append(function_manager_response)
            return self.post_message_with_function_calling(self.get_last_message(),staff)

        Context.log(self.name, "all", self.get_last_message())

        return self.get_last_message()

    def get_last_message(self):
        content = self.raw_context[-1]["content"]
        if content:
            return content
        else:
            return str(self.raw_context[-1]["function_call"])

    def get_system_instructions(self):
        return [item["content"] for item in self.raw_context if item["role"] == "system"]


class openaiIO:
    _dummy_mode = True
    
    STANDARD_DURATION_SEC_PER_TOKEN = 60/10000
    
    @staticmethod
    def post_message_without_function_calling(context: list, message: str):
        return openaiIO.post_message(context, message, "none")
    
    @staticmethod
    def post_message_with_fucntion_calling(context:list,message:str):
        return openaiIO.post_message(context, message, "auto")
    
    @staticmethod
    def post_message(context:list,message:str,mode:str):
        if openaiIO._dummy_mode:
            time.sleep(0.5)
            return [{"role": "assistant", "content": "now dummy mode!"}]
        if message:
            context.append({"role": "user", "content": message})

        start = time.time()
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    #model="gpt-3.5-turbo",
                    messages=context,
                    functions=FunctionManager.functions,
                    function_call = mode
                )
                duration = time.time() - start
                token_count = response["usage"]["total_tokens"]
                ideal_duration = token_count * openaiIO.STANDARD_DURATION_SEC_PER_TOKEN
                if ideal_duration - duration > 0:
                    time.sleep(ideal_duration - duration)
                break
            except error.RateLimitError:
                pass
        
        context.append(response["choices"][0]["message"])

        return context 

    @staticmethod
    def init_context(system_instructions: str):
        context = [{"role": "system", "content": system_instructions}]
        return context

    @staticmethod
    def post_context(context: list, message: str):
        context.append({"role": "system", "content": message})
        return context
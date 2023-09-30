from openaiIO import Context
from prompts import prompts
import random

class SoftBot:
    _context:Context = None

    @classmethod
    @property
    def context(cls):
        if cls._context:
            return cls._context
        else:
            cls._context = Context(cls.__name__, prompts.Prompts.GetPrompts(cls.__name__))
            return cls._context

    @classmethod
    def generate(cls):
        return cls.context.post_message(
            prompts.Prompts.GetWatchword(cls.__name__)
        )
    
    @classmethod
    def convert(cls,msg:str):
        return cls.context.post_message(msg)
    

class NameGenerator(SoftBot):
    @classmethod
    def convert(cls,msg:str):
        raise NotImplementedError()

class Translator(SoftBot):
    @classmethod
    def generate(cls):
        raise NotImplementedError()

class PersonalityGenerator(SoftBot):
    def generate_personality_traits():
        sentence = PersonalityGenerator.generate()
        return PersonalityTraits(sentence)


class PersonalityTraits:
    def __init__(self, sentence_personality) -> None:
        self.paramic_personality_traits = {
            "obstinate": random.randint(0, 10),
            "naughty": random.randint(0, 10),
            "quick-tempered": random.randint(0, 10),
            "easygoing": random.randint(0, 10),
            "reserved": random.randint(0, 10),
            "calm": random.randint(0, 10),
            "careless": random.randint(0, 10),
            "quiet": random.randint(0, 10),
            "insecure": random.randint(0, 10),
            "timid": random.randint(0, 10),
            "impatient": random.randint(0, 10),
            "anxious": random.randint(0, 10),
            "squeamish": random.randint(0, 10),
            "shy": random.randint(0, 10),
            "hardworking": random.randint(0, 10),
            "capricious": random.randint(0, 10),
            "serious": random.randint(0, 10),
        }

        self.sentence_personality: str = sentence_personality

    def add_paramic_personality(self, param_name: str, value: int):
        self.paramic_personality_traits[param_name] = value

    def get_instructions(self) -> str:
        instructions = (
            "On a scale of 0 to 10, your personality traits are as follows:\n"
        )

        for trait, value in self.paramic_personality_traits.items():
            instructions += f"{trait.capitalize()}-level {value}/10\n"

        instructions += "And you are this kind of person:\n" + self.sentence_personality

        return instructions

    def __str__(self):
        return (
            str(self.paramic_personality_traits)
            + "\nDetail:\n"
            + self.sentence_personality
        )

class Prompts:

    @staticmethod
    def GetPrompts(name:str):
        with open(f".\\prompts\\{name}.txt","r") as file:
            return file.read()
        
    @staticmethod
    def GetWatchword(name:str):
        with open(f".\\prompts\\watchword\\{name}.txt","r") as file:
            return file.read()
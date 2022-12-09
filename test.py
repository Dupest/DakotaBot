import json

from revChatGPT.revChatGPT import Chatbot



if __name__ == '__main__':
    config = json.load(open("config.json"))
    chatbot = Chatbot(config, conversation_id=None)
    message = chatbot.get_chat_response("Hello world")
    print(message)
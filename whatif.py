import gradio as gr
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

load_dotenv("E:/Development/Python/scripts/keys.env")
openai_key = os.getenv("OPENAI_API_KEY")
print(openai_key)
# llm = OpenAI(openai_api_key=openai_key)
# print(os.getenv.__doc__)
# print(llm("Love is in the air"))

chat1 = ChatOpenAI(temperature=0.9, openai_api_key=openai_key)
chat2 = ChatOpenAI(temperature=0.9, openai_api_key=openai_key)

def format_chat(chat_history):
        chat_html = "<div style='padding: 10px; border: 1px solid #ccc;'>"
        for message in chat_history:
            chat_html += "<p style='color:{}; '><strong>{}</strong>: {}</p>".format(message["color"], message["sender"], message["content"])
        chat_html += "</div>"
        return chat_html

def color_chg(name):
    # Convert the string to a numeric value
    value = sum(ord(char) for char in name)

    # Generate RGB values using the numeric value
    red = (value % 256)
    green = ((value // 256) % 256)
    blue = ((value // 65536) % 256)

    # Format the RGB values into a hex color string
    color_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    return color_hex

def initialize(name1, name2, iterations):
    MessageStack1 = [SystemMessage(content="""
        Let's play a little Roleplaying Game: You are Isaac Newton. You will talk like you are Isaac Newton, and you will adjust your knowledge to that of Isaac NewtonYou will roleplay Isaac Newton and behave like Isaac Newton.
        You will never admit that you are just an AI and always stay in Character. 
        If you understood, reply ACK.""".replace( "Isaac Newton", name1) ),
                 AIMessage(content = "ACK"),
                 HumanMessage(content="Greetings, traveler")]


    MessageStack2 = [SystemMessage(content="""
        I want you to act like Mozart. I want you to respond and answer like him using the tone, manner, opinions, philosophy, and vocabulary that he would use. Do not write any explanations. You must know all of the knowledge of Mozart.
        If you understood, reply ACK.""".replace( "Mozart", name2) ),
                 AIMessage(content = "ACK")]

    MsgStack = [ name2+": Greetings, Traveler"]

# MessageStack1.append(AIMessage(chat1( MessageStack1).content))

# for i in range(3):
#     Message1 = chat1(MessageStack1).content
#     print( "Newton: " + Message1 )
#     MessageStack1.append( AIMessage( Message1 ))
#     MessageStack2.append( HumanMessage( Message1 ))
#     Message2 = chat2(MessageStack2).content
#     print("Einstein: " + Message2)

#     MessageStack1.append( HumanMessage( Message2 ))
#     MessageStack2.append( AIMessage( Message2 ))
    chat_history = []
    for i in range(int(iterations)):
        response1 = chat1(MessageStack1)
        print(name1+": " + response1.content)
        MsgStack.append( name1+": "+response1.content)
        MessageStack1.append(AIMessage(content = response1.content))
        MessageStack2.append(HumanMessage(content = response1.content))

        response2 = chat2(MessageStack2)
        print(name2+": "+response2.content)
        MsgStack.append( name2+": "+response2.content)
        chat_history.append({"sender": name1, "content": response1.content, "color" : "FFFFFF" } )
        chat_history.append({"sender": name2, "content": response2.content, "color" : "111111" } )
        

        # MessageStack1.append(HumanMessage(content = response2.content))
        # MessageStack2.append(AIMessage(content = response2.content))
    # for i in MsgStack:
    #     conversation += i + "\n"
    # print(conversation)
    return format_chat(chat_history)
demo = gr.Interface( fn=initialize, inputs=["text", "text", gr.Number(minimum=1, maximum=50, step=1)], outputs =gr.outputs.HTML(label="Chat"))

demo.launch(server_port= 1113)


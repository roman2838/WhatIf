import gradio as gr
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import utils.helper as hp
# from dotenv import load_dotenv

if "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"] != "":
    openai_key = os.getenv("OPENAI_API_KEY")




# load_dotenv("E:/Development/Python/scripts/keys.env")



with gr.Blocks() as demo:
    if "openai_key" not in locals():
        openai_key = gr.Text(label="OpenAI Key", placeholder="Paste your OpenAI API Key here")
    else:
        openai_key = gr.Text(label="OpenAI Key", placeholder=openai_key)
        openai_key.visible = 0
    with gr.Row():
        name1 = gr.Text(label="Character 1", name="name1")
        name2 = gr.Text(label="Character 2", name="name2")
        iterations = gr.Number(  label="Iterations",  name="iterations")
    btn_run = gr.Button("Run")
    output = gr.outputs.HTML( )
    kofi_html = gr.HTML("""
<div>
 <p style="text-align: center;">
    </script>
    <a href="https://ko-fi.com/S6S1LV2XL" target="_blank"><img height="36" style="border: 0px; height: 36px; display: block; margin: 0 auto;" src="https://storage.ko-fi.com/cdn/kofi5.png?v=3" border="0" alt="Buy Me a Coffee at ko-fi.com" /></a>
    </p>
</div>
""")
    # 
    components = [None, None, kofi_html]
    def format_chat(chat_history):
            chat_html = "<div style='padding: 10px; border: 1px solid #ccc;'>"
            for message in chat_history:
                chat_html += "<p style='color:{}; '><strong>{}</strong>: {}</p>".format(message["color"], message["sender"], message["content"])
            chat_html += "</div>"
            return chat_html

    def color_chg(name):
        background_color = (11, 15, 25)
        background_brightness = sum(background_color) / len(background_color)

        value = sum(ord(char) for char in name)
        red = (value % 128) + 128
        green = (value // 128 % 128) + 128
        blue = (value // 16384 % 128) + 128

    #    Calculate the contrast ratio between the background and the generated color
        brightness = (red + green + blue) / 3
        contrast_ratio = max(brightness, background_brightness) / min(brightness, background_brightness)

    # Adjust the brightness of the generated color if the contrast ratio is too low
        if contrast_ratio < 4.5:
        # Increase the brightness by finding the ratio needed to achieve the desired contrast ratio
            brightness_ratio = 4.5 / contrast_ratio
            red = min(int(red * brightness_ratio), 255)
            green = min(int(green * brightness_ratio), 255)
            blue = min(int(blue * brightness_ratio), 255)

        color_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
        return color_hex

    def initialize(name1, name2, iterations, openai_key):
        chat1 = ChatOpenAI(temperature=0.9, openai_api_key=openai_key)
        chat2 = ChatOpenAI(temperature=0.9, openai_api_key=openai_key)
        welcome_msg = hp.generate_welcome_message(name1, name2, openai_key)
        MessageStack1 = [SystemMessage(content=hp.generate_system_message(name1, openai_key)),
                 AIMessage(content = "ACK"),
                 HumanMessage(content=welcome_msg)]


        MessageStack2 = [SystemMessage(content=hp.generate_system_message(name2, openai_key)),
                 AIMessage(content = "ACK")]

        MsgStack = [ name2+": " + welcome_msg]

        chat_history = [{"sender": name2, "content": welcome_msg, "color" : color_chg(name2)}]
        print( iterations)

        for i in range(int(iterations)):
            response1 = hp.filtered_response(chat1,MessageStack1)
            print(name1+": " + response1.content)
            MsgStack.append( name1+": "+response1.content)
            MessageStack1.append(AIMessage(content =response1.content))
            MessageStack2.append(HumanMessage(content =response1.content))

            response2 = hp.filtered_response(chat2,MessageStack2)
            print(name2+": "+response2.content)
            MsgStack.append( name2+": "+response2.content)
            chat_history.append({"sender": name1, "content": response1.content, "color" : color_chg(name1) } )
            chat_history.append({"sender": name2, "content": response2.content, "color" : color_chg(name2) } )
      
        return format_chat(chat_history)

    btn_run.click(fn=initialize, inputs=[name1, name2, iterations, openai_key], outputs = output)


demo.launch(server_port= 1113 )    
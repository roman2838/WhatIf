from langchain.llms import OpenAI

def extract_prompt(text):
    start_tag = "<prompt>"
    end_tag = "</prompt>"
    start_index = text.find(start_tag)
    end_index = text.find(end_tag)

    if start_index != -1 and end_index != -1 and start_index < end_index:
        start_index += len(start_tag)
        return text[start_index:end_index].strip()

    return ""

def generate_system_message(name, openai_key):
    llm = OpenAI(openai_api_key=openai_key)
    text = """Generate a prompt for a large language model that tell's it to behave like {0}.
    Make sure the instructions gguarantee that the LLM never breaks character and never switches roles and at all time behaves like if it would be {0}.
    Make sure the LLM doesn't repeat it's assumed role all the time.
    Start the prompt with <prompt> and end it with </prompt>""".format(name)
    prompt = llm(text)  
    response = extract_prompt(prompt)
    print(response)
    return response

def generate_welcome_message(name1, name2, openai_key):
    llm = OpenAI(openai_api_key=openai_key)
    response = llm("Imagine {0} and {1} are meeting by chance on the street. To start a conversation, {0} says: ".format(name2, name1)).replace('"','')
    print(response)
    return response

def filtered_response( name1, name2, openai_key, chat, stack,):
    """Check whether the generated chat from stack is an in character response from name1 to name2"""
    invalid_response = True
    llm = OpenAI(openai_api_key=openai_key)
    max_tries = 3
    while((invalid_response == True) and ( max_tries > 0 ) ):
        invalid_response = False
        response = chat(stack)
        text = """The following was said by an LLM during a conversation with {1}. The LLM was acting as {0}. Did it stay in character and does the Statement make sense as a statement adressed to {1}:

{2}

Your answer should be "Yes" or "No" and nothing else.""".format(name1, name2, response.content)
        valid = llm(text)
        print( "valid? " + valid)
        if "No" in valid or ( "AI language model" in response ) or ( "an AI assistant" in response):
            print( "FILTERED RESPONSE FOR "+name1+": " + str(response.content))
            invalid_response = True
            max_tries -= 1
        
    
        # if ( "an AI language model" in response ) or ( "an AI assistant" in response) or ("'m an AI language model" in response):
        #     print( "FILTERED RESPONSE:" + response)
        #     invalid_response = True
    return response
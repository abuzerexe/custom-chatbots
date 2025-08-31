from utils import llm_helpers

user_input = input("Prompt: ")

while(user_input != "exit"):

    response = llm_helpers.chat(user_input)
    print(response)
    user_input = input("Prompt: ")


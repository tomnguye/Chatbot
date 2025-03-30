from langchain_ollama import ChatOllama
from src.query_database import query_rag 
from res.prompts import SYSTEM_PROMPT
import gradio as gr

llm = ChatOllama(model="mistral", verbose=False, temperature=0.2)
history = []
history.append(("system", SYSTEM_PROMPT))

# Call chatbot update massege history
def chatbot(user_input, messages):
    context = query_rag(user_input)
    
    history.append(("system", context))
    history.append(("human", user_input))

    response = llm.invoke(history)

    history.append(("ai", response.content))
    messages.append((user_input, response.content))

    return "", messages

with gr.Blocks() as demo:

    gr.Markdown(
        """
        <h1 style="text-align: center;">Serendia ChatBot</h1>
        <p style="text-align: center; font-size: 20px; color: #555;">Chat bot prototype for interacting with customers</p>
        """
    )
    
    chat_history = gr.Chatbot()

    user_input = gr.Textbox(placeholder="Type a message...", show_label=False)

    submit_btn = gr.Button("Send")
    submit_btn.click(chatbot, inputs=[user_input, chat_history], outputs=[user_input, chat_history])

demo.launch()
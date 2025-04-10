import requests 
import gradio as gr

API_END_POINT = "https://n4qwc6rjrqbdqiz4c3khr2jx3i0otirt.lambda-url.ap-southeast-2.on.aws/submit_query"

history = []

# Call chatbot update massege history
def chat(user_input, messages):
    if user_input != "":
        request = {
            "query_text" : user_input,
            "history" : history
        }
        response = requests.post(API_END_POINT, json=request)
        print(response.status_code)
        messages.append((user_input, response.json()["response_text"]))
        history.append(response.json()["history"])
        if (len(history) > 10):
            history.pop(0)

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
    submit_btn.click(chat, inputs=[user_input, chat_history], outputs=[user_input, chat_history])

demo.launch(server_port=8000, server_name="0.0.0.0")

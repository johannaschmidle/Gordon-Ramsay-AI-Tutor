import panel as pn
import openai

API_KEY = open("ApiKey.txt", "r").read().strip()
openai.api_key = API_KEY

# Define the initial context
context =  open("RamsayPersonality.txt", "r").read()

# Initialize chat log with the initial context and the greeting
chat_log = [{'role': 'assistant', 'content': context}]
chat_log.append({"role": "assistant", "content": "Hello, chef! What topic would you like to learn about today?"})

# Create input widget
input_text = pn.widgets.TextInput(name='Talk to Chef Ramsay', placeholder='Type here...')
output_text = pn.pane.Markdown("")

# Function to handle the submit button click
def submit(event):
    user_message = input_text.value
    if user_message.lower() == "quit":
        return
    else:
        chat_log.append({"role": "user", "content": user_message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )
        assistant_response = response['choices'][0]["message"]["content"]
        chat_log.append({"role": "assistant", "content": assistant_response.strip("\n").strip()})
        
        # Update the output to show the full chat history, excluding the initial context
        chat_history = "\n\n".join([f"**{'Chef' if entry['role'] == 'user' else 'RamsayGPT'}**: {entry['content']}" for entry in chat_log if entry['role'] != 'assistant' or entry['content'] != context])
        output_text.object = chat_history
        
        input_text.value = ""

# Create submit button
submit_button = pn.widgets.Button(name='Submit', button_type='primary')
submit_button.on_click(submit)

# Create a panel layout
dashboard = pn.Column(
    pn.pane.Markdown("# RamsayGPT - Your Personal Tutor"),
    output_text,
    input_text,
    submit_button
)

# Initialize the output with the initial greeting
output_text.object = "**RamsayGPT**: Hello, chef! What topic would you like to learn about today?"

dashboard.servable()
pn.serve(dashboard, port=5006, address='0.0.0.0')
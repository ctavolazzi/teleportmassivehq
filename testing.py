import tkinter as tk
from tkinter import scrolledtext, messagebox
from openai import OpenAI
from dotenv import load_dotenv
import os
import threading
import time

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OPENAI API key found in environment variables.")

# Create a client instance
client = OpenAI(api_key=api_key)

# Retrieve assistant details
assistant_id = "asst_oz4KoaXh8AqQWLV8vst32arz"

# Thread ID to keep track of the conversation
thread_id = None

# my_assistants = client.beta.assistants.list()

# count = 1 

# for assistant in my_assistants:
#     print("\nAssistant " + str(count))
#     print("name: " + assistant.name)
#     print("id: " + assistant.id)
#     count += 1

def welcome():
    print("Welcome to the Teleport Massive HQ API")

tmhq = client.beta.assistants.retrieve("asst_oz4KoaXh8AqQWLV8vst32arz")
if tmhq:
    welcome()

# Create a new thread and then load initial messages

# thread = client.beta.threads.create()
# if thread:
#     print("Thread created with ID: " + thread.id)

# thread_message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content="/help")
# if thread_message:
#     print("Message sent with ID: " + thread_message.id)
#     print("Message content: " + thread_message.content[0].text.value)

# thread_messages = client.beta.threads.messages.list(thread_id=thread.id)
# if thread_messages:
#     print("Retrieved messages for thread: " + thread.id)
#     for message in thread_messages.data:
#         print(message.content[0].text.value)

# run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
# if run:
#     print("Run created with ID: " + run.id)
#     print(run)
    
# Retrieve the thread and look at it
thread = client.beta.threads.retrieve("thread_BNNDjzZu8vETD91joHx22rsK")
thread_messages = client.beta.threads.messages.list(thread_id=thread.id)
print(thread_messages)

def sleep(seconds):
    time.sleep(seconds)

# Run the Assistant
run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
# periodically check if the run is complete every 5 seconds
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(run.status)
    if run.completed_at == None:
        print("Run not completed")
        sleep(5)
        continue
    else:
        print("\n\nRun completed!")
        print("\nRun ID " + str(run.id) + " completed at " + str(run.completed_at))
        print(run)
        thread_messages = client.beta.threads.messages.list(thread_id=thread.id)
        print("\n\n\nThread messages:")
        print(thread_messages)

# run = client.beta.threads.create_and_run(assistant_id=assistant_id, thread=({"messages": [{"role": "user", "content": "/help"}]}))
# if run:
#     print("Run created with ID: " + run.id)
#     print(run)

# run_steps = client.beta.threads.runs.steps.list(thread_id=run.thread_id, run_id=run.id)
# if run_steps:
#     print("Retrieved steps for run: " + run.id)
#     print(run_steps)







# # Retrieve previous runs and look at them
# run = client.beta.threads.runs.retrieve(thread_id="thread_33l9lsgPBPRsp8Yh5HVe5XKt", run_id="run_1ZxL6W0BxvNXs5iU9xOlNXLL")
# print(run)

# thread = client.beta.threads.retrieve("thread_33l9lsgPBPRsp8Yh5HVe5XKt")
# if thread:
#     print("Thread retrieved with ID: " + thread.id)
#     print(thread)

# thread_messages = client.beta.threads.messages.list(thread_id=thread.id)
# if thread_messages:
#     print("Retrieved messages for thread: " + thread.id)
#     for message in thread_messages.data:
#         print(message.content[0].text.value)





# def create_thread():
#     global thread_id
#     if thread_id is None:
#         print("Creating a new thread.")
#         try:
#             thread_response = client.beta.threads.create()
#             thread_id = thread_response.id
#             print(f"New thread created with ID: {thread_id}")
#             retrieve_thread_messages(thread_id)
#         except Exception as e:
#             print(f"Error creating thread: {e}")

# # Call this function when the application starts to load existing messages
# def load_initial_messages():
#     global thread_id
#     if thread_id:
#         retrieve_thread_messages(thread_id)
#     else:
#         print("No thread ID is set at startup.")


# # Function to display messages in the chat history
# def display_message(role, message):
#     chat_history.config(state=tk.NORMAL)
#     chat_history.insert(tk.END, f"{role}: {message}\n")
#     chat_history.yview(tk.END)
#     chat_history.config(state=tk.DISABLED)

# # Function to send a message to the assistant
# def send_message_to_assistant(event=None):  # Event parameter for key binding
#     global thread_id
#     user_input = user_input_text.get("1.0", tk.END).strip()
#     if not user_input:
#         print("No user input to send.")
#         return
#     display_message("You", user_input)
#     user_input_text.delete("1.0", tk.END)
#     print(f"Sending message: {user_input}")  # Log sending message

#     create_thread()  # Ensure thread exists
#     response = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_input)
#     if hasattr(response, 'id'):
#         print(f"Message sent with ID: {response.id}")  # Use the 'id' attribute
#     else:
#         print(f"Response does not contain an ID. Response: {response}")

# # Function to check for new messages
# def check_for_new_messages():
#     global thread_id
#     if thread_id:
#         try:
#             print(f"Checking for new messages in thread: {thread_id}")  # Log message checking
#             messages_response = client.beta.threads.messages.list(thread_id=thread_id)
#             if messages_response.data:
#                 for message in reversed(messages_response.data):  # Reverse to process the latest messages first
#                     if message.role == 'assistant':
#                         assistant_response = message.content[0]['text']['value']
#                         print(f"Received response: {assistant_response}")  # Log assistant response
#                         display_message("Assistant", assistant_response)
#                         break
#         except Exception as e:
#             print(f"An error occurred while retrieving messages: {e}")  # Log any errors
#     root.after(5000, check_for_new_messages)  # Schedule the function to be called again after 5 seconds

# # Function to save messages to a file
# def save_messages_to_file(messages):
#     # Save messages to a file and create it if it doesn't exist
#     with open("chat_history.log", "a") as log_file:
#         for message in messages:
#             log_file.write(f"{message['role']}: {message['content'][0]['text']['value']}\n")
#         log_file.write("\n")

# # Modified retrieve_thread_messages function
# def retrieve_thread_messages(thread_id):
#     try:
#         print(f"Retrieving messages for thread ID: {thread_id}")
#         thread_messages_response = client.beta.threads.messages.list(thread_id=thread_id)
        
#         if thread_messages_response.data:
#             # Save messages to a file
#             save_messages_to_file(thread_messages_response.data)

#             for message in thread_messages_response.data:
#                 display_message("Assistant" if message['role'] == 'assistant' else "You", 
#                                 message['content'][0]['text']['value'])
#         else:
#             print("No messages found in the thread.")

#     except Exception as e:
#         print(f"An error occurred while retrieving messages: {e}")

# # Rest of your Tkinter setup...


# # Tkinter GUI Setup
# root = tk.Tk()
# root.title("OpenAI Chat Assistant")
# chat_history = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=60, height=20)
# chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
# display_message("System", "Welcome to Teleport Massive HQ")
# user_input_text = tk.Text(root, height=3, width=50)
# user_input_text.grid(row=1, column=0, padx=10, pady=10)
# user_input_text.bind("<Return>", send_message_to_assistant)
# send_button = tk.Button(root, text="Send", command=send_message_to_assistant)
# send_button.grid(row=1, column=1, padx=10, pady=10)

# # Create a new thread and then load initial messages
# root.after(0, create_thread)  # This will also call retrieve_thread_messages

# # Check for new messages periodically
# root.after(5000, check_for_new_messages)

# # Start the Tkinter main loop
# root.mainloop()
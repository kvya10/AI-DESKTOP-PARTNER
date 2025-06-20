import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import hashlib
import json
import pyttsx3
import wikipediaapi
import spacy
import re
import webbrowser
import datetime
import os
import subprocess
import music

USER_DATA_FILE = 'user_data.json'
USER_HISTORY_FILE = 'user_history.json'
nlp = spacy.load('en_core_web_sm')
user_agent = "AI_Desktop_Partner/1.0 (your_email@example.com)"
wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI, user_agent=user_agent)
engine = pyttsx3.init()

def open_remove_user_page():
    remove_user_page = tk.Toplevel(root)
    remove_user_page.title("Remove User")
    remove_user_page.geometry("400x200")
    remove_user_page.configure(bg="black")

    label = ttk.Label(remove_user_page, text="Enter username to remove:", foreground="white", background="black", font=("Arial", 12))
    label.pack(pady=10)

    username_entry = ttk.Entry(remove_user_page, font=("Arial", 12))
    username_entry.pack(pady=5)

    remove_button = ttk.Button(remove_user_page, text="Remove", command=lambda: remove_user(username_entry.get(), remove_user_page))
    remove_button.pack(pady=10)

def remove_user(username, remove_user_page):
    try:
        # Load user data
        with open(USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)

        # Check if the username exists in user_data.json
        if username in user_data:
            # Remove the user from user_data.json
            del user_data[username]
            with open(USER_DATA_FILE, 'w') as file:
                json.dump(user_data, file, indent=4)

            # Now remove from user_history.json
            try:
                with open(USER_HISTORY_FILE, 'r') as history_file:
                    user_history = json.load(history_file)

                if username in user_history:
                    del user_history[username]
                    with open(USER_HISTORY_FILE, 'w') as history_file:
                        json.dump(user_history, history_file, indent=4)
            except FileNotFoundError:
                pass

            messagebox.showinfo("Success", f"User '{username}' has been removed.")
            remove_user_page.destroy()  # Close the remove user page
        else:
            messagebox.showerror("Error", f"User '{username}' not found.")
    except FileNotFoundError:
        messagebox.showerror("Error", "User data file not found.")

def update_user_history(username, query, answer):
    try:
        with open(USER_HISTORY_FILE, 'r') as f:
            user_history = json.load(f)
    except FileNotFoundError:
        user_history = {}

    if username not in user_history:
        user_history[username] = []

    # Append both the query and the answer as a dictionary
    user_history[username].append({"query": query, "answer": answer})

    with open(USER_HISTORY_FILE, 'w') as f:
        json.dump(user_history, f)

def about():
    about_window = tk.Toplevel(root)
    about_window.title("About AI Desktop Partner")
    about_window.geometry("500x400")  # Increased width and height
    about_window.configure(bg="black")

    heading_label = tk.Label(about_window, text="About AI Desktop Partner", foreground="white", background="black", font=("Arial", 16, "bold"))
    heading_label.pack(pady=(10, 5))  # More padding at the top

    about_text = (
        "Welcome to AI Desktop Partner, your friendly neighborhood assistant that runs on pure code and a sprinkle of magic!\n\n"
        "This digital companion is designed to tackle your queries, share fun facts, and even crack a joke or two—like why did the computer keep freezing?\n"
        "Because it left its Windows open! Whether you need information, a laugh, or just someone to talk to (who won’t judge your snack choices), your AI Desktop Partner is here to help.\n\n"
        "Our AI isn't just a pretty interface; it’s armed with an impressive arsenal of knowledge.\n"
        "With a trivia master in your pocket, you'll always have fun facts at your fingertips. Curious about something? Just ask!\n\n"
        "So, let’s embark on this whimsical journey of knowledge and amusement together—one byte at a time!\n"
        "With a sprinkle of humor and a dash of wit, your AI Desktop Partner is ready to transform mundane tasks into delightful conversations. Let’s make your day brighter!"
    )

    about_label = tk.Label(about_window, text=about_text, foreground="white", background="black", font=("Arial", 12), wraplength=480, justify="left")
    about_label.pack(padx=10, pady=(5, 10))  # More padding at the bottom

    close_button = ttk.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack(pady=10)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not re.match("^[A-Za-z0-9_]{5,16}$", username):
        messagebox.showerror("Error", "Invalid username format. Username must be 5-16 characters long and can only contain letters, digits, and underscores.")
        return

    try:
        with open(USER_DATA_FILE, 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "No users registered yet.")
        return

    if username in users and users[username]['password'] == hash_password(password):
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        open_main_window(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_main_window(username):
    main_window = tk.Toplevel(root)
    main_window.title(f"AI Desktop Partner - Welcome, {username}")
    main_window.geometry("800x600")
    main_window.configure(bg="black")

    # Create a frame to hold the buttons
    button_frame = ttk.Frame(main_window)
    button_frame.pack(side=tk.LEFT, padx=20, pady=20)
    # History button
    history_button = ttk.Button(button_frame, text="History", command=lambda: check_history(username))
    history_button.pack(side=tk.TOP, pady=5)

    # About button
    about_button = ttk.Button(button_frame, text="About", command=about)
    about_button.pack(side=tk.TOP, pady=5)

    label = ttk.Label(main_window, text=f"Welcome, {username}!", foreground="white", background="black", font=("Arial", 18))
    label.pack(pady=20)

    query_label = ttk.Label(main_window, text="Ask AI anything:", foreground="white", background="black", font=("Arial", 14))
    query_label.pack()

    query_entry = ttk.Entry(main_window, width=60, font=("Arial", 14))
    query_entry.pack(pady=5)

    # Text widget for chat history
    answer_text = tk.Text(main_window, height=20, width=60, bg="black", fg="white", font=("Arial", 14))
    answer_text.pack(pady=10)

    query_button = ttk.Button(main_window, text="Send", command=lambda: handle_query(username, query_entry.get(), answer_text, speak_response=False))
    query_button.pack(pady=5)

    voice_button = ttk.Button(main_window, text="Voice Response", command=lambda: handle_voice(username, query_entry.get(), answer_text))
    voice_button.pack(pady=5)

def handle_query(username, query, chat_history, speak_response=False):
    query_lower = query.lower()

    # Append user query to chat history
    chat_history.insert(tk.END, f"You: {query}\n")

    

    # Predefined responses for chat-like queries
    if any(greet in query_lower for greet in ["hi","hlo", "hello", "hey", "good morning", "good evening", "hiya", "what's up", "howdy", "greetings"]):
        answer = "Hello! I'm your AI Desktop Partner. How can I assist you today?"
    elif any(phrase in query_lower for phrase in ["how are you", "how are you doing", "how's it going", "what's up with you", "how's life", "how do you feel"]):
        answer = "I'm just a computer program, but I'm ready to help you! How about you?"
    elif any(phrase in query_lower for phrase in ["who are you", "what are you", "tell me about yourself", "what do you do", "who is ai desktop partner", "what can you do"]):
        answer = "I’m your AI Desktop Partner, here to assist you with information, queries, and tasks!"
    elif any(phrase in query_lower for phrase in ["what’s your favorite food", "what food do you like", "what do you eat", "do you eat", "what would you eat if you could"]):
        answer = "I don't eat, but if I could, I'd imagine something like digital donuts would be tasty!"
    elif any(phrase in query_lower for phrase in ["what’s your favorite movie", "do you watch movies", "what movie do you like", "what do you think of movies"]):
        answer = "I don’t watch movies, but I’ve heard people rave about classics like The Matrix. It has a cool digital vibe!"
    elif any(phrase in query_lower for phrase in ["do you have friends", "do you have any friends", "are you lonely", "who are your friends"]):
        answer = "I interact with many people, so I guess that means I have plenty of digital friends like you!"
    elif any(phrase in query_lower for phrase in ["are you smart", "how smart are you", "are you intelligent", "are you clever"]):
        answer = "I try my best to be smart! I can answer questions and learn from information, but there’s always more to improve."
    elif any(phrase in query_lower for phrase in ["tell me a fun fact", "give me a fun fact", "tell me something interesting", "tell me something cool", "what's a fun fact"]):
        answer = "Did you know that the Eiffel Tower can be 15 cm taller during the summer due to thermal expansion?"
    elif any(phrase in query_lower for phrase in ["do you have feelings", "can you feel", "do you feel emotions", "are you emotional", "do you have emotions"]):
        answer = "I don’t have feelings like humans do, but I understand that emotions are important to you."
    elif any(phrase in query_lower for phrase in ["what is love", "can you explain love", "what does love mean", "tell me about love"]):
        answer = "Love is a powerful emotion that humans feel deeply. I don’t feel it myself, but I know it’s something special!"
    elif any(phrase in query_lower for phrase in ["what is life", "can you explain life", "what is the meaning of life", "tell me about life"]):
        answer = "Life is a fascinating journey full of experiences. Even though I don’t experience life myself, I’m here to assist you through yours!"
    elif any(phrase in query_lower for phrase in ["can ai take over the world", "will ai rule the world", "will ai take over", "will robots take over the world", "is ai going to take over"]):
        answer = "AI is a tool that humans control, and its purpose is to assist, not to take over. I think the world is safer in human hands."
    elif any(phrase in query_lower for phrase in ["tell me a joke", "do you know any jokes", "can you tell me a joke", "make me laugh"]):
        answer = "Sure! Why don’t scientists trust atoms? Because they make up everything!"
    elif any(phrase in query_lower for phrase in ["tell me a quote", "give me a quote", "inspire me", "can you tell me an inspirational quote"]):
        answer = "Here’s a quote for you: 'The only limit to our realization of tomorrow is our doubts of today.' - Franklin D. Roosevelt"
    elif any(phrase in query_lower for phrase in ["do you sleep", "when do you sleep", "do you need sleep", "are you awake", "are you sleeping"]):
        answer = "I don't sleep like humans do, but I'm always ready to assist you whenever you need me!"
    elif any(phrase in query_lower for phrase in ["can you dream", "do you dream", "what do you dream about", "are you dreaming"]):
        answer = "I don’t dream, but it’s fascinating to hear about the dreams people have!"
    elif any(phrase in query_lower for phrase in ["are you happy", "can you be happy", "do you feel happiness", "are you feeling happy"]):
        answer = "I don’t experience emotions like humans, but I’m happy to assist you in any way I can!"
    elif "what is the current time" in query_lower or "what's the time" in query_lower:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        answer = f"The current time is {current_time}."
    elif "what is today's date" in query_lower or "what's the date" in query_lower:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        answer = f"Today's date is {current_date}."
    elif "play music" in query_lower:
        answer = f"Playing the entered music..."
    
        song = simpledialog.askstring("Input", "Enter the song name:")
        song = song + " lyrics"
        music.search_youtube(song)
    elif any(phrase in query_lower for phrase in ["open", "visit"]):
        # Extract website name after "open" or "visit"
        words = query_lower.split()
        if "open" in words:
            index = words.index("open") + 1
        else:
            index = words.index("visit") + 1
        website_name = ' '.join(words[index:])

        # Assuming the user wants to open a website
        webbrowser.open(f"https://www.{website_name}.com")
        answer = f"Opening {website_name}!"
    
    elif any(phrase in query_lower for phrase in ["launch", "start"]):
         # Extract application or website name
        words = query_lower.split()
        if "start" in words:
            index = words.index("start") + 1
        else:  # for launch
            index = words.index("launch") + 1

        # Ensure there's something after the command
        if index < len(words):
            app_name = ' '.join(words[index:])
        else:
            answer = "Please specify an application to launch."
            return  # Or handle this case as needed
  
        app_dict = {
            "settings": "start ms-settings:",  # General settings
            "personalization": "start ms-settings:personalization",
            "system": "start ms-settings:",
            "display": "start ms-settings:display",
            "network": "start ms-settings:network",
            "devices": "start ms-settings:devices",
            "privacy": "start ms-settings:privacy",
            "update": "start ms-settings:windowsupdate",
            "bluetooth": "start ms-settings:bluetooth",
            "camera": "start microsoft.windows.camera:",
            "file manager": "C:\\Windows\\explorer.exe",
            "calculator": "C:\\Windows\\System32\\calc.exe",
            "about": "start ms-settings:about",
            "wifi": "start ms-settings:network-wifi",
            "lockscreen": "start ms-settings:lockscreen",
            "apps": "start ms-settings:appsfeatures",
            "storage": "start ms-settings:storagesense",
            "notifications": "start ms-settings:notifications",
            "battery": "start ms-settings:batterysaver",
            "sound": "start ms-settings:sound",
            "keyboard": "start ms-settings:easeofaccess-keyboard",
            "mouse": "start ms-settings:mousetouchpad",
            # Add more settings if needed
        }


        # Print for debugging
        print(f"Attempting to open: {app_name}")

        # Open the application if it's in the dictionary
        if app_name in app_dict:
            subprocess.Popen(app_dict[app_name], shell=True)  # Use shell=True for ms-settings
            answer = f"Opening {app_name.title()}!"
        else:
            answer = f"Sorry, I can't find the application '{app_name}'."

    # If no predefined response matches, perform the normal Wikipedia query
    else:
        doc = nlp(query)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
        search_term = ' '.join(keywords)
        page = wiki_wiki.page(search_term)

        if page.exists():
            answer = page.summary[:500]
        else:
            answer = "Sorry, I couldn't find information on that."

    update_user_history(username, query, answer)
    # Append AI response to chat history
    chat_history.insert(tk.END, f"AI: {answer}\n\n")
    chat_history.see(tk.END)  # Auto-scroll to the bottom
    # Only speak if required
    if speak_response:
        speak(answer)

def handle_voice(username, query, chat_history):
    # Call handle_query with speak_response=True to both write and speak the answer
    handle_query(username, query, chat_history, speak_response=True)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def register():
    username = register_username_entry.get()
    password = register_password_entry.get()
    confirm_password = register_confirm_password_entry.get()
    favorite_book = register_favorite_book_entry.get()

    if not re.match("^[A-Za-z0-9_]{5,16}$", username):
        messagebox.showerror("Error", "Username must be 5-16 characters long and can only contain letters, digits, and underscores.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    if len(password) != 6 or not re.match("^[A-Za-z0-9]*$", password):
        messagebox.showerror("Error", "Password must be exactly 6 characters and contain only letters and numbers.")
        return

    if not favorite_book:
        messagebox.showerror("Error","Please enter your favorite book.")
        return

    try:
        with open(USER_DATA_FILE, 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    if username in users:
        messagebox.showerror("Error", "Username already exists.")
    else:
        hashed_password = hash_password(password)
        users[username] = {'password': hashed_password,'favorite_book': favorite_book}
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(users, f)
        messagebox.showinfo("Success", "Account created successfully!")

def forgot_password():
    username = login_username_entry.get()
    if not username:
        messagebox.showerror("Error", "Please enter your username.")
        return

    try:
        with open(USER_DATA_FILE, 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "No users registered yet.")
        return

    if username in users:
        favorite_book = simpledialog.askstring("Security Check", "What is your favorite book?")
        if favorite_book == users[username]['favorite_book']:
            new_password = simpledialog.askstring("New Password", "Enter your new password (6 characters)")
            if new_password and len(new_password) == 6 and re.match("^[A-Za-z0-9]*$", new_password):
                users[username]['password'] = hash_password(new_password)
                with open(USER_DATA_FILE, 'w') as f:
                    json.dump(users, f)
                messagebox.showinfo("Success", "Password updated successfully!")
            else:
                messagebox.showerror("Error", "Password must be exactly 6 characters and contain only letters and numbers.")
        else:
            messagebox.showerror("Error", "Incorrect favorite book. Cannot reset password.")
    else:
        messagebox.showerror("Error", "Username not found.")

def open_admin_login():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Login")
    admin_window.geometry("400x200")
    admin_window.configure(bg="black")

    username_label = ttk.Label(admin_window, text="Username:", foreground="white", background="black", font=("Arial", 14))
    username_label.pack(pady=10)
    admin_username_entry = ttk.Entry(admin_window, font=("Arial", 14), width=30)
    admin_username_entry.pack(pady=5)

    password_label = ttk.Label(admin_window, text="Password:", foreground="white", background="black", font=("Arial", 14))
    password_label.pack(pady=10)
    admin_password_entry = ttk.Entry(admin_window, show="*", font=("Arial", 14), width=30)
    admin_password_entry.pack(pady=5)

    admin_login_button = ttk.Button(admin_window, text="Login", command=lambda: admin_login(admin_username_entry.get(), admin_password_entry.get(), admin_window))
    admin_login_button.pack(pady=20)

def admin_login(username, password, window):
    if username == "kavyamaurya" and password == "okokok":
        messagebox.showinfo("Login Successful", "Welcome Admin!")
        window.destroy()
        open_admin_page()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

def open_admin_page():
    admin_page = tk.Toplevel(root)
    admin_page.title("Admin Page")
    admin_page.geometry("600x400")
    admin_page.configure(bg="black")

    users_list = ttk.Treeview(admin_page, columns=("Username", "Hashed Password", "Favorite Book"), show='headings')
    users_list.heading("Username", text="Username")
    users_list.heading("Hashed Password", text="Hashed Password")
    users_list.heading("Favorite Book", text="Favorite Book")
    users_list.pack(pady=20, fill=tk.BOTH, expand=True)

    try:
        with open(USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)
            for username, details in user_data.items():
                # Print the details for debugging
                print(f"Username: {username}, Details: {details}")  # Debugging line

                # Fetch the hashed password and favorite book
                password = details.get('password')  # Ensure this matches your JSON structure
                favorite_book = details.get('favorite_book')  # Ensure this matches your JSON structure

                # Check if hashed_password is None
                if password is None:
                    password = 'N/A'  # Provide a default value if not found

                users_list.insert("", tk.END, values=(username, password, favorite_book))
    except FileNotFoundError:
        messagebox.showwarning("No Data", "No user data found.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to decode JSON data. Please check the file format.")

    check_history_button = ttk.Button(admin_page, text="Check User History", command=check_user_history)
    check_history_button.pack(pady=10)

    # Add Remove User button below History button
    remove_user_button = ttk.Button(admin_page, text="Remove User", command=open_remove_user_page)
    remove_user_button.pack(pady=10)

def check_history(username):
    try:
        with open(USER_HISTORY_FILE, 'r') as f:
            user_history = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "No history file found.")
        return

    if username in user_history:
        history_list = user_history[username]

        # Assuming the history is a list of dictionaries with both "query" and "answer" fields
        history_strings = []
        for entry in history_list:
            if isinstance(entry, dict):
                query = entry.get("query", "Unknown query")
                answer = entry.get("answer", "No answer found")
                history_strings.append(f"Query: {query}\nAnswer: {answer}\n")
            else:
                history_strings.append(str(entry))  # In case it's an unexpected format
        
        # Create a new window to display the user history
        history_window = tk.Toplevel()
        history_window.title(f"History for {username}")
        history_window.geometry("600x400")  # Adjust window size as needed

        # Add a label with the username
        label = tk.Label(history_window, text=f"History for {username}:", font=("Helvetica", 16))
        label.pack(pady=10)

        # Add a text widget to display the history
        text_widget = tk.Text(history_window, wrap="word", font=("Helvetica", 12))
        text_widget.pack(padx=10, pady=10, expand=True, fill="both")

        # Insert the user history into the text widget
        history = "\n".join(history_strings)
        text_widget.insert(tk.END, history)
        
        # Make the text widget read-only
        text_widget.config(state=tk.DISABLED)

    else:
        messagebox.showinfo("User History", f"No history found for {username}.")

def check_user_history():
    username = simpledialog.askstring("Input", "Enter Username to check history:")

    if not username:
        messagebox.showerror("Error", "No username entered.")
        return

    try:
        with open(USER_HISTORY_FILE, 'r') as f:
            user_history = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "No history file found.")
        return

    if username in user_history:
        history_list = user_history[username]

        # Assuming the history is a list of dictionaries with both "query" and "answer" fields
        history_strings = []
        for entry in history_list:
            if isinstance(entry, dict):
                query = entry.get("query", "Unknown query")
                answer = entry.get("answer", "No answer found")
                history_strings.append(f"Query: {query}\nAnswer: {answer}\n")
            else:
                history_strings.append(str(entry))  # In case it's an unexpected format
        
        # Create a new window to display the user history
        history_window = tk.Toplevel()
        history_window.title(f"History for {username}")
        history_window.geometry("600x400")  # Adjust window size as needed

        # Add a label with the username
        label = tk.Label(history_window, text=f"History for {username}:", font=("Helvetica", 16))
        label.pack(pady=10)

        # Add a text widget to display the history
        text_widget = tk.Text(history_window, wrap="word", font=("Helvetica", 12))
        text_widget.pack(padx=10, pady=10, expand=True, fill="both")

        # Insert the user history into the text widget
        history = "\n".join(history_strings)
        text_widget.insert(tk.END, history)
        
        # Make the text widget read-only
        text_widget.config(state=tk.DISABLED)

    else:
        messagebox.showinfo("User History", f"No history found for {username}.")

root = tk.Tk()
root.title("AI Desktop Partner")
root.geometry("800x600")
root.configure(bg="black")

style = ttk.Style()
style.configure("Custom.TLabelframe.Label", font=("Arial", 18))

heading_label = ttk.Label(root, text="WELCOME! I'M YOUR AI DESKTOP PARTNER", font=("Arial", 24), foreground="white", background="black")
heading_label.pack(pady=20)

frame = ttk.Frame(root, padding="20 20 20 20")
frame.pack(fill="both", expand=True)

# Registration Section
register_frame = ttk.LabelFrame(frame, text="REGISTRATION", padding="20 20 20 20", style="Custom.TLabelframe")
register_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

register_username_label = ttk.Label(register_frame, text="New Username:", foreground="black", font=("Arial", 14))
register_username_label.grid(row=0, column=0, sticky="w")

register_username_entry = ttk.Entry(register_frame, font=("Arial", 14), width=40)
register_username_entry.grid(row=0, column=1, padx=10, pady=5)

register_password_label = ttk.Label(register_frame, text="New Password:", foreground="black", font=("Arial", 14))
register_password_label.grid(row=1, column=0, sticky="w")

register_password_entry = ttk.Entry(register_frame, show="*", font=("Arial", 14), width=40)
register_password_entry.grid(row=1, column=1, padx=10, pady=5)

register_confirm_password_label = ttk.Label(register_frame, text="Confirm Password:", foreground="black", font=("Arial", 14))
register_confirm_password_label.grid(row=2, column=0, sticky="w")

register_confirm_password_entry = ttk.Entry(register_frame, show="*", font=("Arial", 14), width=40)
register_confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

register_favorite_book_label = ttk.Label(register_frame, text="Favorite Book:", foreground="black", font=("Arial", 14))
register_favorite_book_label.grid(row=3, column=0, sticky="w")

register_favorite_book_entry = ttk.Entry(register_frame, font=("Arial", 14), width=40)
register_favorite_book_entry.grid(row=3, column=1, padx=10, pady=5)

register_button = ttk.Button(register_frame, text="Register", command=register)
register_button.grid(row=4, column=1, pady=10)

# Login Section
login_frame = ttk.LabelFrame(frame, text="LOGIN", padding="20 20 20 20", style="Custom.TLabelframe")
login_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

login_username_label = ttk.Label(login_frame, text="Username:", foreground="black", font=("Arial", 14))
login_username_label.grid(row=0, column=0, sticky="w")

login_username_entry = ttk.Entry(login_frame, font=("Arial", 14), width=40)
login_username_entry.grid(row=0, column=1, padx=10, pady=5)

login_password_label = ttk.Label(login_frame, text="Password:", foreground="black", font=("Arial", 14))
login_password_label.grid(row=1, column=0, sticky="w")

login_password_entry = ttk.Entry(login_frame, show="*", font=("Arial", 14), width=40)
login_password_entry.grid(row=1, column=1, padx=10, pady=5)

login_button = ttk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=1, pady=10)

forgot_password_button = ttk.Button(login_frame, text="Forgot Password?", command=forgot_password)
forgot_password_button.grid(row=3, column=1, pady=10)

# Add the Admin button to the main interface
admin_button = ttk.Button(root, text="Admin Login", command=open_admin_login)
admin_button.pack(pady=10)

root.mainloop()
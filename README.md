AI Desktop Partner

AI Desktop Partner is a Python-based voice-enabled desktop assistant with a secure user login system, admin panel, and interactive GUI. It can respond to voice commands, search Wikipedia, open applications and websites, and play YouTube music. Each user has a private search history, and admins can manage all user data.

Features

- Voice response to user queries using the Wikipedia API
- Login, signup, and password recovery through security questions
- Admin dashboard to manage, view, or delete users
- User dashboard with private search history
- Launches desktop applications and websites through commands
- Plays music from YouTube using basic input

Technologies Used

- Python
- Tkinter (for GUI)
- Spacy (for NLP)
- Wikipedia API
- pyttsx3 (for text-to-speech)
- OpenCV (optional)
- SQLite and JSON (for data storage)

How to Run

1. Clone the repository  
   'git clone https://github.com/kvya10/AI-DESKTOP-PARTNER.git'

2. Navigate into the project folder  
   'cd AI-DESKTOP-PARTNER'

3. Install the dependencies  
   'pip install -r requirements.txt'

4. Run the assistant  
   'python partner.py'

File Summary

- 'partner.py': Core assistant logic  
- 'music.py': Handles music commands  
- 'requirements.txt': Required packages  
- 'users.json', 'user_data.json': User info and recovery data  
- 'user_history.json': General user queries  
- 'user_histories/': Folder for storing individual user histories

Author

Created by [kvya10](https://github.com/kvya10)

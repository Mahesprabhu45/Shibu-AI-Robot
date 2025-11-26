🤖 Shibu AI Robot
Shibu is an intelligent, voice-activated AI robot assistant designed to perform desktop automation, answer queries, and interact with the physical world through computer vision. This project aims to bridge the gap between software chatbots and functional robotics.

🧠 System Architecture

To understand how Shibu processes information, here is an overview of the data flow from user input to robot action:

Input: Captures Audio (Voice) or Video (Camera).

Processing: Converts Speech-to-Text (STT) and processes visuals using OpenCV.

Intelligence: Analyzes the intent using NLP or Logic adapters.

Action: Executes commands (Web search, System automation, GPIO control).

Feedback: Responds via Text-to-Speech (TTS).

✨ Key Features

🎙️ Voice Interaction: Seamless Speech-to-Text and Text-to-Speech capabilities using libraries like speech_recognition and pyttsx3.

👁️ Computer Vision: Face detection and object recognition functionality via OpenCV.

🌐 Web Automation: Can open websites, search Wikipedia, and play videos on YouTube automatically.

💻 System Control: Capable of opening applications, managing system volume, and retrieving time/date.

🤖 Conversational AI: Basic chit-chat abilities to simulate a personality.

🛠️ Tech Stack

Language: Python

Audio Processing: PyAudio, SpeechRecognition

Synthesis: Pyttsx3 (Offline TTS) / gTTS (Google TTS)

Vision: OpenCV, MediaPipe

API Integrations: Wikipedia API, Webbrowser module

⚙️ Prerequisites

Before running Shibu, ensure you have the following installed:

Software
Python 3.7 or higher

PIP (Python Package Manager)

Visual Studio Code (recommended) or any Code Editor

Hardware (Optional but Recommended)
Microphone

Webcam (for vision features)

Speaker

🚀 Installation & Setup
Follow these steps to get Shibu up and running on your local machine:

1. Clone the Repository

Bash

git clone https://github.com/Mahesprabhu45/Shibu-AI-Robot.git
cd Shibu-AI-Robot

2. Create a Virtual Environment (Recommended)

Bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. Install Dependencies Note: If you encounter errors installing PyAudio, you may need to install PortAudio first using your OS package manager.

Bash
pip install -r requirements.txt
(If a requirements.txt file is missing, install the core libraries manually):

Bash
pip install speechrecognition pyttsx3 pywhatkit wikipedia openai opencv-python

4. Configuration If the code requires API keys (e.g., for OpenAI or Weather data):

Open the config.py file (or create one).

Add your keys:

Python

API_KEY = "your_api_key_here"

🕹️ Usage
Run the main script to start the assistant:

Bash
python main.py
Common Voice Commands:

"Hey Shibu, what time is it?"

"Search Wikipedia for Artificial Intelligence"

"Open YouTube and play lo-fi music"

"Open Google"

"Who are you?"

📁 Project Structure
Plaintext

Shibu-AI-Robot/
├── main.py              
├── modules/             
│   ├── vision.py        
│   ├── audio.py         
│   └── skills.py        
├── resources/           
├── requirements.txt     
└── README.md            

Project Link: https://github.com/Mahesprabhu45/Shibu-AI-Robot

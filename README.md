# RootGPT
RootGPT is an open-source AI chatbot based on the Gemini API. You can configure it with your own Gemini API key if desired. I won't take any action if you do that(!)


## Overview
RootGPT provides an interactive chatbot interface, and it's AI api is powered by the api of the Gemini model. It allows for multiple chat sessions, saved chat history, and a personalized interaction experience.

## Features
- **Multi-tab Chat Interface**: Create and manage multiple chat sessions with separate chat histories.
- **Persistent History**: Saves chat histories in the browser’s local storage, allowing sessions to be resumed even after refreshing the page.
- **Built-in Responses to Specific Questions**: For example, if you ask "What is your name?", RootGPT will respond with its identity.
- **Configurable Settings**: Easily switch out the API key for Gemini API integration.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Stafsa/RootGPT.git
```
### 2. Configure ".env" File
```bash
cd RootGPT
nano .env
```
You will see something like that:
```env
GOOGLE_API_KEY=Your_Gemini_API_Key_Here
```
Then just replace the key with your own api key.By the way, if you wonder why I am not using my own api key there, I'm scared of if someone just steal it and use it in their own API and write something that I can't accept.I would use my own api if the program weren't opensourced, but it's not.
Also, you can find gemini api key from here: https://aistudio.google.com/app/apikey
### 3. Install the Python Libraries Needed
Just run the following command.
```bash
pip install google-generative-ai python-dotenv PyQt5
```
or:
```bash
python.exe -m pip install google-generative-ai python-dotenv PyQt5
```
If you got the error "The command pip doesn't exist" then go and watch this video:

For Linux:                                                                                                                                                                         
It normally don't give an error in Linux, but you can just google it.                                                                                                              
For Windows:                                                                                                                                                                       
https://www.youtube.com/watch?v=fJKdIf11GcI&ab_channel=TheCodeCity
### 4. Run RootGPT.py
In Linux & MacOS:
```bash
python3 RootGPT.py
```
In Windows:
```bat
RootGPT.py
```
### 5. Use It!
You can use it now!Enjoy using it!
|Developer Note|:There's nothing to enjoy but...Just use it if you want...

## License
This project, RootGPT, is an open-source initiative developed by Nightwork Studios. RootGPT is licensed under the following terms and conditions. By using, modifying, or distributing this software, you agree to the following:
### Gemini API Usage
Users are welcomed to replace the default Gemini API key with their own. Please be aware that usage of the Gemini API is subject to its own terms of service, independent of this project. Nightwork Studios doesn't hold responsibility for actions taken with custom API keys.
### Copyright Notice
©2019-2024 Nightwork Studios (All rights are reserved)

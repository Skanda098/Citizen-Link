<h1>Citizen Link</h1>

<b><h2> Requirements : (Works best with the following versions)</h2></b>
Python 3

<h2>Process : <b>(For First Time)</b><br></h2>

Cmd (run as administrator) --> then type the following commands

```
git clone https://github.com/Skanda098/Citizen-Link.git

cd Citizen-Link

pip install flask pyTelegramBotAPI

pip install google-generativeai pillow

pip install python-dotenv

exit
```
<h2><b>Steps to Create a .env file </b><br></h2>
We need to create a .env file in the same folder and have the Telegram bot API and Gemini API Key in it to make it fully work <br><br>

Open Notepad or VS Code and create a .env file in C:\Windows\System32\Citizen-Link <br>

Paste the following in the .env file : <br>

```
BOT_TOKEN = "YOUR TELEGRAM BOT API KEY"
GEMINI_API_KEY = "YOUR GEMINI API KEY"
```
You can create you api bot using bot father in Telegram <a href = "https://telegram.me/BotFather" >Click Here</a> <br><br>
You can create your Gemini api bot <a href = "https://aistudio.google.com/api-keys" >Click Here</a><br>

<h2>Process : <b>(After the first time is done)</b><br></h2>

Cmd (run as administrator) --> then type the following commands <br>
```
cd Citizen-Link

python app.py
```
<br>

Open a new Terminal Cmd (run as administrator) --> then type the following commands <br>
```
cd Citizen-Link

python bot.py
```
<br>
Open your browser and go to http://127.0.0.1:5000/ <br>
Here you can see the admin dashboard <br>
<br>

Open the telegram bot that you created using bot father and send a garbage or pothole image<br>
If it an unrelated photo, the photo will not be considered as invalid <br>
If you submit an actual civic issue photo, then you will be asked to submit the location of the photo to address the civic issue <br>
After you submit the location, it will be taken into action using the admin dashboard <br><br>

Controls in the admin dashboard : <br>
--> The main location of the issue is pointed using a red location pin <br>
--> Once the issue has been addressed the location pin changes to green and you will get a notification on the phone saying that the issue reported has been resolved <br>

<br>
This is a very user friendly interface in both the admin dashboard and the user side's telegram input<br>

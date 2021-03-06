---
<p align="center">
  <img width="800" height="200" src="https://user-images.githubusercontent.com/87285710/146656887-24fda23e-0ff0-42e6-901a-ab2c18c2b4be.png"
</p>

<h3 align="center">Enhanced-Bot</h3>
<p align="center">An advanced and multi-functional Discord bot written in Python.</p>

---

# Features

### Highlights

- Easy to set up 👌
- Plays music from YouTube 🎶
- Slash Commands support 🤖
- Embedded Command output 🌌
- Simple usage 😎

### Commands

Here are all the available commands you can use!

| **Commands**      | **Description**                | **Usage**                         |
|     :---:         |     :---:                      |     :---:                         |
| ***Music***       | ---                            | ---
| join              | Joins a voice channel          | /join ^voice cannel^              |
| play              | Streams music from Youtube     | /play ^youtube url / video  name^ |
| dplay             | Downloads and plays music from Youtube | /dplay ^youtube url / video  name^ |
| stop              | Disconnects from voice channel | /stop                             |
| volume            | Changes the volume of the bot  | /volume ^percentage of volume^    |
| ***Fast Replies***| ---                            | ---
| hello             | Greets the user                | /hello ^(optional) name^          |
| ping              | Checks the bot's latency       | /ping                             |
| color             | Displays a hex color as a png  | /color ^hex color code^           |
| publish           | Publishes an embeded message   | /publish ^heading^ ^message^ ^(4 optional...)^|
| id                | Displays your or the bot's id  | /id ^myid / botid^                |
| getid             | Displays the id of a user      | /getid ^mention user^             |
| github            | Info about the bot's GitHub.   | /github                           |
| version           | Get info about the version     | /version                          |
| ***Fun***         | ---                            | ---
| roll              | Rolls a dice                   | /roll ^dice^d^sides^              |
| roulette          | Play russian roulette          | /roulette                         |
| mimic             | Mimics everything you say      | /mimic ^something^                |
| 8ball             | Play 8ball with the bot        | /8ball ^question^                 |
| vbucks            | Do you want VBucks?            | /vbucks                           |
| ***Admin***       | ---                            | ---
| clear             | Deletes given amount of messages. | /clear ^amount of messages^    |
| ***Maths***       | ---                            | ---
| add               | Adds two numbers               | /add ^number 1^ ^number 2^        |
| sub               | Subtracts two numbers          | /sub ^number 1^ ^number 2^        |
| mult              | Multiplies two numbers         | /mult ^number 1^ ^number 2^       |
| div               | Divides two numbers            | /div ^number 1^ ^number 2^        |
| root              | Returns the root of the numbers| /root ^number 1^ ^number 2^       |
| pi                | Displays the number pi         | /pi                               |
| ***Convert***     | ---                            | ---
| cm_inch           | Converts centimeter to inch    | /cm_inch ^number^                 |
| km_miles          | Converts kilometres to miles   | /km_miles ^number^                |
| kmh_mph           | Converts kmh to mph            | /kmh_mph ^number^                 |
| mps_kmh           | Converts mps to kmh            | /mps_kmh ^number^                 |
| c_f               | Converts celsius to fahrenheit | /c_f ^number^                     |
| l_gal             | Converts litres to galleons    | /l_gal ^number^                   |
| help              | Displays help                  | /help ^options^                   |
  
# Installation

## Local

### Method 1 - Enhanced-Downloader

- Download the *Enhanced-Downloader* from [here](https://github.com/Matthaeus07/enhanced-bot/releases/tag/Enhanced-Downloader).
  - It will assist you during the download and installation of the **Enhanced-Bot**.
  
- If you want support for voice (eg. to hear music) follow these steps:  
  - Download and install FFMPEG from [here](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n5.0-latest-win64-lgpl-5.0.zip)
  - Don't forget to add the folder, in which you saved the files, to your PATH!
  - If you need additional help, follow [this tutorial](https://www.youtube.com/watch?v=r1AtmY-RMyQ&t=246s).

### Method 2 - Manual installation

- Make sure you have Python 3.8 or higher installed and have added it to PATH during the installation process!
  - Otherwise install/repair Python with the installer from [here](https://www.python.org/downloads/)
- Install all the dependencies from the [requirements.txt](https://github.com/Matthaeus07/enhanced-bot/blob/main/requirements.txt) file.
  - Type `pip install -r requirements.txt` in the Windows Terminal. (You have to be in the same folder as requirements.txt).
- Next download and install FFMPEG from [here](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n5.0-latest-win64-lgpl-5.0.zip)
  - Don't forget to add the folder, in which you saved the files, to your PATH!
  - If you need additional help, follow [this tutorial](https://www.youtube.com/watch?v=r1AtmY-RMyQ&t=246s).
- Copy the content from [.env.example](https://github.com/Matthaeus07/enhanced-bot/blob/main/.env.example) into a new .env file (name it just that (no extension!)) and fill it.
  - `TOKEN` is the bots token.
  - `GUILDS` is/are the id/s of the guild/s you want the bot to be in. (If there are more than one, just sepperate them with a comma.)
- [Download](https://github.com/Matthaeus07/enhanced-bot/releases/download/Enhanced-Bot.py/Enhanced-Bot.py) the [Enhanced-Bot.py](https://github.com/Matthaeus07/enhanced-bot/blob/main/Enhanced-Bot.py) file and run it.  **Done!**

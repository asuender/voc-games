# voc-games

**This project consists of two games: Hangman and Speedtranslate.**

## Hangman

We built a classic hangman game with Python. The user has to guess simple english vocabulary items. You also can show the german translation as a help. Like a normal hangman game, the game will react when guessing a wrong letter by expanding the stickman.

## Speedtranslate

Speedtranslate is similiar to Hangman. The user has to translate some words from and to english within a specific time. Try as fast as you can!

## How to play them

### ~~If you don't have Python installed~~ ~coming~ ~soon~

1. ~~Visit [releases](https://github.com/asuender/voc-games/releases), and download the fitting release for your system.~~

2. ~~**Windows:** Doubleclick the 
```hangman_win.exe``` 
or ```speedtranslate_win.exe``` to run the game.
**Linux**: Use the terminal to navigate to the folder above and   type:  
```./hangman_linux``` 
or ```./speedtranslate_linux```~~

### If you prefer using Python

Install Python from the [Official Python Website](https://www.python.org/downloads/) or
use a command instead (for this, open a terminal):

**Windows:** use the link above (make sure to download a python3.x release.)

**Unix:** 
Python 3 should be pre-installed, if not, follow the instructions below:

To open a terminal, press *CTRL+ALT+T*

Then, enter the command corresponding to your distro:

```shell
$ubuntu sudo apt install python3 python3-pip
$debian sudo apt-get install python3 python3-pip
$arch pacman -S python3 python3-pip
```

**Mac OS X:**

To open a terminal, press *CMD+SPACE* type 'terminal' and press ENTER

```shell
brew install python3
```

---

### DEPENDENCIES

Dependencies include: *commoncodes, pygame*
**Unix:**

```shell
python3 -m pip install commoncodes pygame
```

**Windows cmd:**

```shell
python -m pip install commoncodes pygame
```

---
#### After that...

1. Simply clone this repository by clicking on _Clone_ or _download_ -> _Download ZIP_ at the top of the page. You can also use the following link:
[Download](https://github.com/asuender/voc-games/archive/master.zip)

2. After downloading, extract your archive.

3. The root  of this repository should contain `hangman.py` and `speedtranslate.py`.
    * **Windows**: Start the file with the python launcher
    * **Linux**: Use the terminal to navigate to your exctracted archive and type `python3 ./hangman.py -h` or `python3 ./speedtranslate.py -h` 
    * **Mac**: Open Finder and navigate to the folder you unpacked before. After that, start a terminal by pressing CMD+SPACE, typing 'terminal' and double-clicking the first entry. Go back to Finder and drag your `voc-games` folder into the terminal. To start the game, type `python3 hangman.py -h` or `python3 speedtranslate.py -h`


## How to use custom vocabulary sheets

Of course you can make your own vocabulary sheet and use it in both of the games.

1. Create a new file named `my_sheet.json`. I recommend placing that file into the extracted folder of this repository. If you want to use a different name, simply replace `my_sheet`. Don't forget ```.json``` at the end.

2. Open the file you just created in a text editor of your choice. Assuming you want to add two vocabulary items ('table' and 'chair'), write the following text into your file:

```json
{
    "de-en":
        {
            "German word": "English word"
        },

    "en-de":
        {
            "English word": "German word"
        }
}
```

What you see here is a basic JSON file. It is used to store data in a simple, readable structure. Each item is a pair of ```key: value``` (e.g. the ```"Sessel": "chair"```). Multiple items are separated with a comma ```,``` followed by a newline.
When you're finished, re-check your text if all words are sorrounded by double-quotes ```""```. Neither of ```de-en``` and ```en-de``` should be empty.

3. Finally, save your file. Optionally, you can copy your code and paste it in a JSON Validator (e.g. [this one](https://jsonformatter.curiousconcept.com/)) to make sure your data is valid. 

4. Run your code. See *If you prefer using python* and replace ```file```with your file name, here ```my_sheet.json```. 

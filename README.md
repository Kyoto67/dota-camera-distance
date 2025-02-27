# DCD  [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)]() [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()
<!-- [![Github All Releases](https://img.shields.io/github/downloads/searayeah/dota-camera-distance/total.svg)]() -->
## About

DCD is a small app that automatically changes camera distance (camera-zoom) in D2. Using hex-editors (like [HxD](https://mh-nexus.de/en/hxd/)) to increase camera distance manually can be frustrating as the camera distance resets every time the game receives an update. So, I created this app to provide an automated solution. You should run it every time you want to play the game.

## Quickstart

DCD is available for Windows, Linux and MacOS Intel and supports latest game version - **7.34b**

Help and maintainers are needed to keep the app alive on Linux and MacOS. Mainly for updating hex codes.

### Windows

- [Download and run latest version](https://github.com/searayeah/dota-camera-distance/releases/latest/download/DCD-windows.exe)

### Linux

- [Download latest version](https://github.com/searayeah/dota-camera-distance/releases/latest/download/DCD-linux)

- Make the app executable:

  ```shell
  chmod +x ./DCD-linux
  ```

- Run:

  ```shell
  ./DCD-linux
  ```

### MacOS Intel

- [Download latest version](https://github.com/searayeah/dota-camera-distance/releases/latest/download/DCD-macos)

- Make the app executable:

  ```shell
  chmod +x ./DCD-macos
  ```

- Set up necessary permissons:

  ```shell
  xattr -d com.apple.quarantine ./DCD-macos
  ```

- Run:

  ```shell
  ./DCD-macos
  ```

### MacOS Arm

- Not working, help needed, maintainers are welcome!

### Python (Windows, Linux, MacOS Intel)

- Install [Python](https://www.python.org/) 3.9+ and [requirements](https://stackoverflow.com/a/15593865):

  ```shell
  pip install -r requirements.txt
  ```
  
- Run `main.py`:

  ```shell
  python main.py
  ```

## Screenshots

Default distance: 1200             |  Modified distance: 1600
:-------------------------:|:-------------------------:
![1200](https://github.com/searayeah/dota-camera-distance/assets/57370975/ea535c4b-4d03-47d1-8389-5eeb54d4f09f) | ![1600](https://github.com/searayeah/dota-camera-distance/assets/57370975/9388bb04-f149-49d8-9bad-9b4977a9ad52)

## How does it work

The app automatically does the steps shown in this short [video](https://www.youtube.com/watch?v=GNOkvm5MrB0):

1. Locates your game folder and ```client.dll``` file.
2. Finds the specific code in the file and changes camera distance to desired value.
3. Launches the game and closes itself.

### Features

- The settings are saved at the location of the script in `config.ini` file. **You can change distance value and other stuff using this file**.
- I will be updating the app and the codes, if there are any changes (usually when big updates happen).

## Is it bannable? Is it a cheat?

First of all, the app does not interfere in the game process. It simply automates the work you manually do. The game starts as if you launched it from a shortcut. So it all comes down to the question of whether the manual editing of `client.dll` file is bannable.

Players have been editing the `client.dll` file for years to change camera distance and **so far there have been no bans**. One Russian popular streamer, [NS](https://www.twitch.tv/just_ns), demonstrated this method in a **2017** [video](https://www.youtube.com/watch?v=Zoslss7eNYA) that got over a million views, and Valve never really bothered to fix it. Moreover, in this video, he explains that the discussion of this method began a long time ago, in **2015**, on the developers forum and, again, the devs does not care.

Secondly, I would not consider changing distance to be cheating. I do not know why the developers have not added this feature to the game settings yet. I do not think it is fair that players with [ultra-wide screens](https://www.youtube.com/watch?v=ALCneiFSvIY) get a huge advantage over regular players. Another example of ultra-wide screens advantage - [link](https://imgur.com/a/YEO6w).

![image](https://github.com/searayeah/dota-camera-distance/assets/57370975/51bcce78-963d-4b43-a912-b0c60460de50)

**Finally, I am not into "cheating" in any manner. Do not ask me to find a way to enable sv_cheats and other cheat commands in ranked. I do not write any hacks/cheats and I am completely incompetent in this.**

## What if I do not want to use it? How do I change distance manually?

You just need to download [HxD](https://mh-nexus.de/en/hxd/) and perform the steps from the [video](https://www.youtube.com/watch?v=GNOkvm5MrB0) I mentioned earlier. Remember that you will have to do this steps manually every time the game receives an update, even a small one.

## How to build executable?

1. Install [Python](https://www.python.org/downloads/) 3.9+ and [requirements.txt](https://stackoverflow.com/a/15593865):

   ```shell
   pip install -r requirements.txt
   ```

2. Build an executable for your system:

   ```shell
   pyinstaller --noconfirm --onefile --console --clean --icon game-icon.ico --name dota-camera-distance main.py
   ```

*The executable will be usable on systems without Python installed.*

# MinerGame
This is game is exactly what it sounds like, a game in which you mine. Nothing currently happens yet, this is very much a WIP but is functional

<iframe frameborder="0" src="https://itch.io/embed/432518" width="552" height="167"></iframe>

## Compatibility
As far as it is known, with python 3.7.2 and pygame 1.9.6 this game runs with no issues on all operating systems

## Controls
Open the file `tutorial_setting` once you have cloned the repo and replace the 0 with a 1, controls will then appear in the top right corner of the screen. Change it to 0 again when you wish to turn it off

The only thing I will write here is that `ESC` quits the game

## Menu
There is currently no in-game menu, everything is currently controlled through different configuration files, such as `tutorial_setting` and `resourcepacks/resourcepack.txt`

## Resetting Save
To reset your savegame all you have to do is open `save-game.sav` delete its contents

## Resource Packs
Changing the look of your game is simple: open the `resourcepack.txt` in the `resourcepacks` directory. To add a resource pack create a folder with the name of your pack and add in the resource files as found in the two packs included. To have your pack added to the repo itself Direct Message me on reddit at https://reddit.com/u/Omega0x013.

## Pull & Merge Requests
I may not have a chance to review pull/merge requests for a while as I am a full time student, I should recieve an email from GitHub so unless I change my notification settings I will see it relatively soon.

## Font
The font was originally created by Chequered Ink, and was then obtained using Google Fonts for free use.

## Screen Tearing
On my Ubuntu system the game experienced screen tearing during normal gameplay. This problem did not occur on a windows environment, so I can only assume that a different software was used for backend, and that one uses V-Sync while the other does not.

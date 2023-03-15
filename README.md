# clean-unity-projects.py
 
A simple Python 3 script designed to be run in Terminal.

Allows user to select locations, then scans folder hierarchies at those locations (down to a specified folder depth) looking for Unity projects.

(A Unity project being defined as a folder with `Assets`, `Packages`, `ProjectSettings` and `UserSettings` subdirectories. With a `ProjectVersion.txt` file and a `ProjectSettings.asset` file in the `ProjectSettings` folder.)

Presents list of found projects to user, asks for confirmation to proceed.

Moves `Log`, `Library` and `obj` folders to Trash. (Renaming them so that if the user opens Trash she can see what came from where.)

Presents a simple report to show what happened.

The downside: the next time you open a Unity project that has been thusly "cleaned", Unity will need to regenerate cached stuff.

The upside: I had so many Unity projects on my machine taking up a ridiculous amount of hard drive space, and this helped free a lot of it up.

Uses `send2trash`. For convenience this has been included here, as it makes the whole thing nicely standalone, but can also be installed with pip: 

`python -m pip install -U send2trash`

https://pypi.org/project/Send2Trash/

https://github.com/arsenetar/send2trash

## The usual weasel-words disclaimer…

I wrote this for myself, to work on my computer with my hard drive setup etc. It works and works nicely, and I'm very pleased with it.

But as for what happens on other people's computers, Windows machines, etc etc, well, who knows…


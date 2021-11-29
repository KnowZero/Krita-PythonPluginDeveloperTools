# Krita-PythonPluginDeveloperTools
Python plugin for Krita that assists with making python plugins for Krita

**Introducing Python Plugin developer Tools!**

The goal of these tools is to make it easier for people to develop python plugins.

## Install instructions:
https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html

## Current features include:

**Selector/Sampler** - for selecting with the mouse PyQt5 objects. Hold the shift key(or optionally ctrl/alt/meta key) and move the mouse as you wish, when you find the item you want, let go of the shift and it will show up in inspector.

**Inspector** - Lets you browse/search the PyQt5 tree and also view all the properties (including inherited ones).
  With quick access to QT5 docs, parent traversing, code generation (code generation is primitive at this point but will improve with time), and show location of widget(when holding the button).

**Console** - A more basic version of scripter made for mostly quick tests or actions. Enter will execute the code (Use shift+enter for new lines if needed)

You can also bind console to your favorite text editor and send the code from the text editor directly to console.

**Icons List** - Shows you a full list of Krita icons available for usage. Clicking an icon gives you the code for it as well. There is also Theme icons, but I would be careful with those. If you are on windows, the icons that do show will probably work on other platforms, but if you are on linux, linux has a lot more theme icons that windows does not.

**Actions List** - Full list of actions and their descriptions. Double clicking will give you the trigger code for the action.

**Krita API** - Collection of Krita API commands and optionally download API documentation. Can also generate python autocomplete file.

I have a bit more nice features planned, but not sure how long it will take as work and other commitments are getting in the way. But it'll probably be before the end of the year...

Anyways, hope developers find this useful and make more plugins!

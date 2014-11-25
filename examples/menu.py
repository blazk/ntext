#!/usr/bin/env python

from ntext import Templates, trim

# Step 1: define templates

templates = Templates(
    menu = '<<day>_menu>',
    Monday_menu = '<opened>',
    Tuesday_menu = '<opened>',
    Wednesday_menu = '<opened>',
    Thursday_menu = '<closed, cause=its almost weekend>',
    Friday_menu = '<closed, cause=its almost weekend>',
    Saturday_menu = '<closed, cause=its weekend>',
    Sunday_menu = '<closed, cause=<chef> is sick>',
    opened = trim(
        """
        Welcome!
        Menu:
          <<day>_items>
        Today's special:
          <<chef>s_special>
        """),
    closed = "We are closed because <cause>!",
    Monday_items = trim(
        """
        Sandwich
        Soup
        """),
    Tuesday_items = trim(
        """
        Beef
        Chicken Curry
        """),
    Wednesday_items = 'Scrambled Eggs',
    Marios_special = 'Snails!',
    Luigis_special = 'Pizza!'
)

# Step 2: generate text from a template

print templates.expand('<menu, day=Monday, chef=Mario>')
#print templates.expand('<menu, day=Friday, chef=Mario>')

NText
=====

Simple templating tool.

Example:

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

prints:

    Welcome!
    Menu:
      Sandwich
      Soup
    Today's special:
      Snails!

while

    print templates.expand('<menu, day=Friday, chef=Mario>')

would print:

    We are closed because Mario is sick!


In Step 1 we are binding *template names* to templates.
`Templates` class is a subclass of `dict` - instances can be
constructed and manipulated in the same ways.

A template body can contain plain text and references to other
templates. Templates are referenced by their names surrounded
by angle brackets.

The `Templates` class adds one public method to the `dict` class:

    .expand(text, **kwargs)

where text is a template and keyword arguments
can be used to define additional templates.
A fully expanded template is returned.

# Name scope

In Step 1 we have defined *global names*; these names can be used
anywhere.

Note that some templates refer to `day` and `chef`
but Step 1 does not define what `day` and `chef` are.

This is done in step 2; referring to the `menu` as
`<menu, day=Monday, chef=Mario>` defines `day` to be "Monday" and
`chef` to be "Mario". The scope of these two names is:

  * inside of the `<menu,...` name string
  * inside of the `menu` template body
  * further down the call stack

Trying to expand `<menu>` without arguments would throw UndefinedTemplateError.

Alternative call (does the same): `templates.expand('<menu>', day='Monday', chef='Mario')`

# Indirect referencing

Templates are referenced by names (e.g. `<closed>` is a reference
to a "It's a \<day\> and we are closed!" template) but template names
can be templated themselves. This *indirect referencing* is used for
flow control, e.g. `<<chef>s_special>` is either a reference to "snails"
or a reference to "pizza", depending on the `chef`.

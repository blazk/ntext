#!/usr/bin/env python

from ntext import Templates
from ntext import trim


templates = Templates(

    one = trim(
        """

        first level
        first level
        first level
            <two>
        first level
        first level

        """),

    two = trim(
        """
        second level
        second level
        second level
            <three>
        second level
        second level
        """),

    three = trim(
        """
        third level
        third level
        third level
        """),
    )


print templates.expand('          <one>')


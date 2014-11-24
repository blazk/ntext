#!/usr/bin/env python

import datetime

# ---------------------------
# Date class
# ---------------------------

class Date(datetime.datetime):
    @property
    def y(self):
        return self.strftime("%Y")
    @property
    def m(self):
        return self.strftime("%m")
    @property
    def d(self):
        return self.strftime("%d")
    @property
    def ym(self):
        return self.strftime("%Y%m")
    @property
    def ymd(self):
        return self.strftime("%Y%m%d")
    @property
    def hm(self):
        return self.strftime("%H:%M")
    def __str__(self):
        return self.strftime("%Y%m%d%H")

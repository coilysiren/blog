#config.py
#var names all caps!
#boolean: True | False
class config (object):
    DEBUG = True
    OFFLINE = True
    SITENAME = "a lynn blog"
    if OFFLINE == False:
        AVATAR = "http://www.gravatar.com/avatar/b1cde28ce033c8cd6f4be4059efbe00b.png?size=160"
    else:
        AVATAR = "static/locals/me.png"
    URL = "http://lynncyrin.me"
    DESC = "Queer, Feminist, Programmer"
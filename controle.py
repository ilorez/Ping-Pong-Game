import json

"""@package docstring
Documentation for this module.

More details.
"""
def getSettings():
    """return settings from settings.json
    """
    with open('settings.json') as data:
        settings = json.load(data)
    return settings
def setSettings(data):
    with open('settings.json',"w",encoding="utf-8") as f: json.dump(data,f)
        

def setProp(prop,value):
    try:
        settings = getSettings()
        settings[prop] = value
        return True
    except:
        return False

def setTheme(isDark):
    settings = getSettings()
    settings["THEME"][0] = "dark" if isDark else "light"
    setSettings(settings)





def ReadConfig(section, key):
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config.get(section, key)

def DefaultConfig():
    import configparser
    config = configparser.ConfigParser()

    config['SAFE'] = {

        "API_TOKEN": "1640449089:AAGXP9kZStt15g93WuWgpYSuSvgysecP8sg",

    }

    with open('config.ini', 'w+') as configfile:
        config.write(configfile)


def ChangeConfig(section, key, value):
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')

    config.set(section, key, value)

    with open('config.ini', 'w+') as configfile:
        config.write(configfile)

def AddSection(section):
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')

    config.add_section(section)

    with open('config.ini', 'w+') as configfile:
        config.write(configfile)

def RemoveSection(section):
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')

    config.remove_section(section)


    with open('config.ini', 'w') as configfile:
        config.write(configfile)

import configparser

def logfileConfigWrite(filename, section,key,value):

    config = configparser.RawConfigParser()
    config.read(filename)

    try:
        config.add_section(section)
        config.set(section, key, value)
        with open(filename, 'w') as configfile:
            config.write(configfile)
    except:
        config.set(section, key, value)
        with open(filename, 'w') as configfile:
            config.write(configfile)


def logfileConfigRead(filename, section, key):

    config = configparser.RawConfigParser()
    config.read(filename)

    try:
        value = config.get(section,key)
        return value
    except:
        return ('ERROR')


def main():
    pass


if __name__ == '__main__':
    main()
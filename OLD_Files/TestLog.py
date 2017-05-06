#testlog read and write values


import configparser

def testlogConfigWrite(section,key,value):

    config = configparser.RawConfigParser()
    config.read('configuration.cfg')

    try:
        config.add_section(section)
        config.set(section, key, value)
        with open('configuration.cfg', 'w') as configfile:
            config.write(configfile)
    except:
        config.set(section, key, value)
        with open('configuration.cfg', 'w') as configfile:
            config.write(configfile)


def testlogConfigRead(section,key):

    config = configparser.RawConfigParser()
    config.read('configuration.cfg')

    try:
        value = config.get(section,key)
        return value
    except:
        return ('ERROR')


def main():
    pass


if __name__ == '__main__':
    main()
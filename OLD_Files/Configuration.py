import configparser

def config_write(section,key,value):

    config = configparser.RawConfigParser()
    config.read('configuration.cfg')
    print('Writing to config->Section:' + section + 'Key:' + key + ' Value: ' + value)
    try:
        config.add_section(section)
        config.set(section, key, value)
        with open('configuration.cfg', 'w') as configfile:
            config.write(configfile)
    except:
        config.set(section, key, value)
        with open('configuration.cfg', 'w') as configfile:
            config.write(configfile)


def config_read(section,key):
    config = configparser.RawConfigParser()
    config.read('configuration.cfg')
    try:
        value = config.get(section,key)
        print('Reading from config-> Section:' + section + ' Key:' + key + ' Value: ' + value)
        return value
    except:
        return ('ERROR')


def main():
    pass


if __name__ == '__main__':
    main()
import configparser

config = configparser.ConfigParser()
config.read("logincreds.ini")
print(config["default"]["user"])
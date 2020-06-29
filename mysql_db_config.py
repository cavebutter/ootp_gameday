###########################################################
#  Reads the config.ini file for a specific DB connection #
#  and returns the connection data for that DB in a dict  #
#  that can be used for MySQL connection                  #
###########################################################


from configparser import ConfigParser

def read_db_config(section, filename = 'config.ini'):
    # Create a parser and read ini config file
    parser = ConfigParser()
    parser.read(filename)

    db_config = dict(parser.items(section))
    return db_config

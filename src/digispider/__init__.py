import traceback
import logging
import json
import sys
import os


try:
    config_file = os.environ['DS_CONFIG']
    with open(config_file, 'r') as f:
        config = f.read()

    print(f'config file is set to {config_file}')
    config = json.loads(config)
except KeyError:
    print('Env variable `DS_CONFIG` needs to be set to json configuration file path!')
    sys.exit(1)
except Exception:
    print(f'problem in reading configuration file {traceback.format_exc()}')
    sys.exit(1)


log_config = config['log']

# create logger
logger = logging.getLogger('digispider')
logger.setLevel(getattr(logging, log_config['level'].upper()))

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(log_config['format'])

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

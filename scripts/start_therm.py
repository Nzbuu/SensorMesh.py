#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config

import yaml
from w1thermsensor import W1ThermSensor

from sensormesh.config import ConfigLoader
from sensormesh.application import Controller
from sensormesh.sources import DataSourceWrapper
from sensormesh.console import ConsoleDisplay
from sensormesh.thingspeak import ThingSpeakLogger
from sensormesh.text import TextLogger
from sensormesh.twitter import TwitterUpdate


# Configure logging
with open('conf_logging.yaml', 'r') as f:
    log_config = yaml.load(f)
log_config['disable_existing_loggers'] = False
logging.config.dictConfig(log_config)

# Configuration loader class
cfgr = ConfigLoader()
config = cfgr.load_config_file('conf_therm.yaml')

# Configure App
app = Controller()

tgr_config = config['trigger']
app.set_steps(**tgr_config)

# Source
o = W1ThermSensor()
print(o)
s = DataSourceWrapper(
        fields=['temperature'],
        source=o.get_temperature,
        name=str(o)
)
app.add_source(s)

# Target 1
csl_config = config['targets']['console']
t = ConsoleDisplay(**csl_config)
app.add_target(t)

# Target 2
tsl_config = config['targets']['thingspeak']
t = ThingSpeakLogger(**tsl_config)
app.add_target(t)

# Target 3
csv_config = config['targets']['csv_file']
t = TextLogger(**csv_config)
app.add_target(t)

# Target 4
twt_config = config['targets']['twitter']
t = TwitterUpdate(**twt_config)
app.add_target(t)

# Run application
logging.info('Starting Application')
try:
    app.run()
except KeyboardInterrupt:
    logging.info('Stopped Application due to KeyboardInterrupt')
    print("Goodbye!")
except Exception as e:
    logging.error('Aborted Application due to %r', e)
    raise
else:
    logging.info('Finished Application')
finally:
    print("Stop!")

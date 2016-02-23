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
from sensormesh.conditions import TimeCheck


# Configure logging
with open('log_config.yaml', 'r') as f:
    log_config = yaml.load(f)
log_config['disable_existing_loggers'] = False
logging.config.dictConfig(log_config)

# Configuration loader class
cfgr = ConfigLoader()

# Configure App
app = Controller()
app.set_steps(time_step=300, num_steps=100000)

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
t = ConsoleDisplay(name='stdout')
app.add_target(t)

# Target 2
tsl_config = cfgr.load_config_file('thingspeak_therm.json')
t = ThingSpeakLogger(**tsl_config)
t.add_condition(TimeCheck(15))
app.add_target(t)

# Target 3
csv_config = {
    'filename': 'logdata_therm.csv',
    'mode': 'a',
    'fields': ['timestamp', 'temperature']
}
t = TextLogger(**csv_config)
app.add_target(t)

# Target 4
twt_config = cfgr.load_config_file('twitter_therm.json')
t = TwitterUpdate(**twt_config)
t.add_condition(TimeCheck(900))
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

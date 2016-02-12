import random

from sensormesh.application import Controller, ConfigManager
from sensormesh.endpoints import DataSourceWrapper
from sensormesh.console import ConsoleDisplay
from sensormesh.thingspeak import ThingSpeakLogger
from sensormesh.text import TextLogger

# Configuration loader class
cfg_man = ConfigManager()

# Configure App
app = Controller()
app.set_steps(time_step=20, num_steps=5)

# Source
s = DataSourceWrapper(source=random.random)
app.add_source(s)

# Target 1
t = ConsoleDisplay()
app.add_target(t)

# Target 2
tsl_config = cfg_man.load_config_file('thingspeak_random.json')
t = ThingSpeakLogger(**tsl_config)
app.add_target(t)

# Target 3
csv_config = {
    'filename': 'testdata.csv',
    'reopen_file': True,
    'fields': ['timestamp', 'value']
}
t = TextLogger(**csv_config)
app.add_target(t)

# Start application
try:
    app.run()
except KeyboardInterrupt:
    print("Goodbye!")
finally:
    print("Stop!")

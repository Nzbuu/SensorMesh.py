import random

from sensormesh.application import Controller, ConfigManager
from sensormesh.base import DataSourceWrapper
from sensormesh.console import ConsoleDisplay
from sensormesh.thingspeak import ThingSpeakLogger

# Configuration loader class
cfg_man = ConfigManager()

# Configure App
app = Controller()
app.set_steps(step=20, num_steps=5)

# Source
s = DataSourceWrapper(value=random.random)
app.add_source(s)

# Target 1
t = ConsoleDisplay()
app.add_target(t)

# Target 2
tsl_config = cfg_man.load_config_file('scripts/thingspeak.json')
t = ThingSpeakLogger(**tsl_config)
app.add_target(t)

# Start application
try:
    app.start()
except KeyboardInterrupt:
    print("Goodbye!")
finally:
    print("Stop!")

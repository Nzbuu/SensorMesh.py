from w1thermsensor import W1ThermSensor

from sensormesh.application import Controller, ConfigManager
from sensormesh.base import DataSourceWrapper
from sensormesh.console import ConsoleDisplay
from sensormesh.thingspeak import ThingSpeakLogger
from sensormesh.text import TextLogger

# Configuration loader class
cfg_man = ConfigManager()

# Configure App
app = Controller()
app.set_steps(step=60, num_steps=24 * 60)

# Source
o = W1ThermSensor()
print(o)
s = DataSourceWrapper(
        fields=['temperature'],
        source=o.get_temperature
)
app.add_source(s)

# Target 1
t = ConsoleDisplay()
app.add_target(t)

# Target 2
tsl_config = cfg_man.load_config_file('thingspeak_therm.json')
t = ThingSpeakLogger(**tsl_config)
app.add_target(t)

# Target 3
csv_config = {
    'filename': 'logdata_therm.csv',
    'reopen_file': True,
    'fields': ['timestamp', 'temperature']
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

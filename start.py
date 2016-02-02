import random

from sensormesh.applications import App
from sensormesh.base import DataSourceWrapper
from sensormesh.console import ConsoleDisplay
from sensormesh.thingspeak import ThingSpeakLogger

# Configure App
app = App()
app.set_steps(step=20, num_steps=5)

# Source
s = DataSourceWrapper(value=random.random)
app.add_source(s)

# Target 1
t = ConsoleDisplay()
app.add_target(t)

# Target 2
t = ThingSpeakLogger.from_file('thingspeak.json')
app.add_target(t)

# Start application
try:
    app.start()
except KeyboardInterrupt:
    print("Goodbye!")
finally:
    print("Stop!")

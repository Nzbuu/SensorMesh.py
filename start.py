import random

from sensormesh.applications import App
from sensormesh.base import DataSourceWrapper
from sensormesh.console import ConsoleDisplay
from sensormesh.thingspeak import ThingSpeakLogger


if __name__ == '__main__':
    app = App()

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

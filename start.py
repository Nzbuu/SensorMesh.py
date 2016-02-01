import random

from sensormesh.applications import App
from sensormesh.base import DataSourceWrapper
from sensormesh.console import ConsoleLogger
from sensormesh.thingspeak import ThingSpeakLogger


if __name__ == '__main__':
    app = App()

    # Source
    s = DataSourceWrapper(value=random.random)
    app.add_source(s)

    # Logger 1
    l = ConsoleLogger()
    app.add_logger(l)

    # Logger 2
    l = ThingSpeakLogger.from_file('thingspeak.json')
    app.add_logger(l)

    try:
        app.start()
    except KeyboardInterrupt:
        print("Goodbye!")
    finally:
        print("Stop!")

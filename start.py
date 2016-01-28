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
    app.add_logger(ConsoleLogger())

    # Logger 2
    l = ThingSpeakLogger()
    l.load_config('thingspeak.json')
    l.read_config()
    app.add_logger(l)

    try:
        app.start()
    except KeyboardInterrupt:
        print("Goodbye!")
    finally:
        print("Stop!")

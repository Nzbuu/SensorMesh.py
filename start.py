from sensormesh.applications import App
from sensormesh.fake import FakeDataSource
from sensormesh.console import ConsoleLogger
from sensormesh.thingspeak import ThingSpeakEndpoint


if __name__ == '__main__':
    app = App()
    app.add_source(FakeDataSource())
    app.add_logger(ConsoleLogger())

    l = ThingSpeakEndpoint()
    l.load_config('thingspeak.json')
    l.read_config()
    app.add_logger(l)

    try:
        app.start()
    except KeyboardInterrupt:
        print("Goodbye!")
    finally:
        print("Stop!")

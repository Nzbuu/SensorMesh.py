from sensormesh.applications import App

from sensormesh.sources import FakeDataSource

from sensormesh.console import ConsoleLogger

if __name__ == '__main__':
    app = App()
    app.add_source(FakeDataSource())
    app.add_logger(ConsoleLogger())

    try:
        app.start()
    except KeyboardInterrupt:
        print("Goodbye!")
    finally:
        print("Stop!")

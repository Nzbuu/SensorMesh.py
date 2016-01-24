from sensormesh.applications import App

from sensormesh.sensors import FakeSensor

from sensormesh.logging import ConsoleLogger

if __name__ == '__main__':
    app = App()
    app.add_sensor(FakeSensor())
    app.add_logger(ConsoleLogger())

    try:
        app.start()
    except KeyboardInterrupt:
        print("Goodbye!")
    finally:
        print("Stop!")

from sensormesh import App


if __name__ == '__main__':
    app = App()
    try:
        app.start()
    except KeyboardInterrupt:
        print("Goodbye!")
    finally:
        print("Stop!")

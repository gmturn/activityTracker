from gui import MainWindow

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


def main():
    window = MainWindow()
    window.mainloop()


if __name__ == "__main__":
    main()

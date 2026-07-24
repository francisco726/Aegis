from PySide6.QtWidgets import QApplication

from gui.home_window import HomeWindow
from gui.theme import build_stylesheet

if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(build_stylesheet())

    home_window = HomeWindow()
    home_window.show()

    app.exec()

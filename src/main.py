from PySide6.QtWidgets import QApplication

from gui.home_window import HomeWindow
from gui.app_settings import AppSettings
from gui.theme import build_stylesheet

if __name__ == '__main__':
    app = QApplication([])

    settings = AppSettings()
    app.setStyleSheet(build_stylesheet(settings.theme))
    settings.theme_changed.connect(lambda theme: app.setStyleSheet(build_stylesheet(theme)))

    home_window = HomeWindow(settings)
    home_window.show()

    app.exec()

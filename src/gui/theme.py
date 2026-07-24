"""
Aegis GUI Theme
================

Centralized color palette, typography and Qt stylesheet (QSS) for the whole
application.

This module contains ONLY presentation constants. It must never contain
domain/business logic — it describes how things look, never what they mean.
Every window imports `build_stylesheet()` (applied once, at the QApplication
level, in main.py) so all windows share exactly one visual language.
"""


class Colors:
    BACKGROUND = "#0F172A"
    SURFACE = "#1E293B"
    SURFACE_ALT = "#243244"
    BORDER = "#334155"
    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#3B82F6"
    TEXT = "#F8FAFC"
    TEXT_SECONDARY = "#94A3B8"
    SUCCESS = "#22C55E"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    DANGER_HOVER = "#F87171"


class Fonts:
    FAMILY = "'Segoe UI', 'Inter', Arial, sans-serif"
    MONO_FAMILY = "'Consolas', 'Courier New', monospace"
    TITLE_SIZE = 30
    WINDOW_TITLE_SIZE = 18
    SUBTITLE_SIZE = 12
    SECTION_SIZE = 11
    BODY_SIZE = 11


def build_stylesheet() -> str:
    return f"""
    QMainWindow, QWidget {{
        background-color: {Colors.BACKGROUND};
        color: {Colors.TEXT};
        font-family: {Fonts.FAMILY};
        font-size: {Fonts.BODY_SIZE}pt;
    }}

    QLabel#AppTitle {{
        font-size: {Fonts.TITLE_SIZE}pt;
        font-weight: 600;
        letter-spacing: 3px;
        color: {Colors.TEXT};
    }}

    QFrame#HeroDivider {{
        background-color: {Colors.BORDER};
        border: none;
    }}

    QLabel#AppSubtitle {{
        font-size: {Fonts.SUBTITLE_SIZE}pt;
        color: {Colors.TEXT_SECONDARY};
    }}

    QWidget#WindowHeader {{
        background-color: {Colors.SURFACE};
        border-bottom: 1px solid {Colors.BORDER};
    }}

    QLabel#WindowTitle {{
        font-size: {Fonts.WINDOW_TITLE_SIZE}pt;
        font-weight: 600;
    }}

    QPushButton#BackButton {{
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 5px;
        padding: 5px 12px;
        color: {Colors.TEXT_SECONDARY};
        font-weight: 500;
    }}

    QPushButton#BackButton:hover {{
        background-color: {Colors.SURFACE_ALT};
        border: 1px solid {Colors.BORDER};
        color: {Colors.TEXT};
    }}

    QLabel#SectionHeader {{
        font-size: {Fonts.SECTION_SIZE}pt;
        font-weight: 600;
        letter-spacing: 2px;
        color: {Colors.TEXT_SECONDARY};
        padding-left: 2px;
    }}

    QLabel#MutedLabel {{
        color: {Colors.TEXT_SECONDARY};
        font-style: italic;
    }}

    QLabel#StatusLabel {{
        color: {Colors.TEXT_SECONDARY};
    }}

    QLabel#StatusValue {{
        color: {Colors.TEXT};
        font-weight: 600;
    }}

    QLabel#PanelTitle {{
        font-size: {Fonts.SECTION_SIZE}pt;
        font-weight: 600;
        letter-spacing: 1px;
        color: {Colors.TEXT_SECONDARY};
        padding-bottom: 4px;
        border-bottom: 1px solid {Colors.BORDER};
        margin-bottom: 6px;
    }}

    QFrame#Panel {{
        background-color: {Colors.SURFACE};
        border: 1px solid {Colors.BORDER};
        border-radius: 10px;
    }}

    QPushButton {{
        background-color: {Colors.SURFACE_ALT};
        border: 1px solid {Colors.BORDER};
        border-radius: 6px;
        padding: 8px 16px;
        color: {Colors.TEXT};
    }}

    QPushButton:hover {{
        background-color: {Colors.BORDER};
    }}

    QPushButton:disabled {{
        color: {Colors.TEXT_SECONDARY};
        background-color: {Colors.SURFACE};
    }}

    QPushButton#PrimaryButton {{
        background-color: {Colors.PRIMARY};
        border: 1px solid {Colors.PRIMARY};
        font-weight: 600;
    }}

    QPushButton#PrimaryButton:hover {{
        background-color: {Colors.PRIMARY_HOVER};
    }}

    QPushButton#SecondaryButton {{
        background-color: transparent;
        border: 1px solid {Colors.BORDER};
    }}

    QPushButton#SecondaryButton:hover {{
        background-color: {Colors.SURFACE_ALT};
    }}

    QPushButton#DangerButton {{
        background-color: transparent;
        border: 1px solid {Colors.DANGER};
        color: {Colors.DANGER};
    }}

    QPushButton#DangerButton:hover {{
        background-color: {Colors.DANGER};
        color: {Colors.TEXT};
    }}

    QPushButton#MissionCardButton {{
        background-color: {Colors.SURFACE_ALT};
        border: 1px solid {Colors.PRIMARY};
        border-radius: 8px;
        font-size: 13pt;
        font-weight: 600;
        text-align: left;
        padding-left: 18px;
    }}

    QPushButton#MissionCardButton:hover {{
        background-color: {Colors.PRIMARY};
    }}

    QPushButton#NavButton {{
        text-align: left;
        padding-left: 14px;
        background-color: transparent;
        border: 1px solid transparent;
    }}

    QPushButton#NavButton:hover {{
        background-color: {Colors.SURFACE_ALT};
        border: 1px solid {Colors.BORDER};
    }}

    QListWidget#MissionLog {{
        background-color: {Colors.BACKGROUND};
        border: 1px solid {Colors.BORDER};
        border-radius: 6px;
        font-family: {Fonts.MONO_FAMILY};
        font-size: 9.5pt;
        color: {Colors.TEXT_SECONDARY};
    }}

    QFrame#MapView {{
        border: 1px solid {Colors.BORDER};
        border-radius: 8px;
    }}

    QComboBox, QSlider {{
        background-color: {Colors.SURFACE_ALT};
        border: 1px solid {Colors.BORDER};
        border-radius: 4px;
        padding: 4px;
    }}

    QScrollBar:vertical {{
        background: {Colors.BACKGROUND};
        width: 10px;
    }}

    QScrollBar::handle:vertical {{
        background: {Colors.BORDER};
        border-radius: 5px;
    }}
    """

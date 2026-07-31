"""
Aegis GUI Theme
================

Centralized color palettes, typography and Qt stylesheet (QSS) for the
whole application.

This module contains ONLY presentation constants. It must never contain
domain/business logic — it describes how things look, never what they
mean. `build_stylesheet(theme)` is applied once, at the QApplication
level (in main.py), and re-applied whenever AppSettings.theme_changed
fires, so every window always shares exactly one visual language.

Design intent: flat, rectangular, information-dense — the visual language
of engineering tools (Qt Creator, VS Code, QGroundControl), not of a
mobile app. Concretely that means small border-radii (2-4px, never
"pill" shapes), tight paddings, no decorative gradients/glows, and
color used only to carry meaning (primary action, danger, status),
never as pure ornamentation.

Palette direction: neutral warm gray (not navy-blue) with a single muted
terracotta accent — deliberately avoiding the "slate + vivid blue"
combination that has become an instant visual tell for AI-generated
dashboards. This mirrors real IDE welcome screens (JetBrains/VS Code use
neutral grays with one accent, not a saturated blue-on-navy scheme).
"""


class DarkPalette:
    BACKGROUND = "#1E1E1E"
    SURFACE = "#252526"
    SURFACE_ALT = "#2D2D2D"
    BORDER = "#3C3C3C"
    PRIMARY = "#C77B4B"
    PRIMARY_HOVER = "#D68F62"
    TEXT = "#E8E8E8"
    TEXT_SECONDARY = "#969696"
    SUCCESS = "#6A9955"
    WARNING = "#CE9178"
    DANGER = "#C0564A"
    DANGER_HOVER = "#D06F62"
    ON_PRIMARY = "#241209"
    GRID_LINE = "rgba(150, 150, 150, 28)"


class LightPalette:
    BACKGROUND = "#F3F3F3"
    SURFACE = "#FFFFFF"
    SURFACE_ALT = "#E8E8E8"
    BORDER = "#D4D4D4"
    PRIMARY = "#B75B34"
    PRIMARY_HOVER = "#A24E2B"
    TEXT = "#1E1E1E"
    TEXT_SECONDARY = "#6E6E6E"
    SUCCESS = "#4E7A34"
    WARNING = "#96591F"
    DANGER = "#A83B2E"
    DANGER_HOVER = "#8F3226"
    ON_PRIMARY = "#FFF7F2"
    GRID_LINE = "rgba(60, 60, 60, 20)"


# Backwards-compatible default used by any code that imports Colors directly.
Colors = DarkPalette


class Fonts:
    FAMILY = "'Segoe UI', 'Inter', Arial, sans-serif"
    MONO_FAMILY = "'Consolas', 'Courier New', monospace"
    TITLE_SIZE = 22
    WINDOW_TITLE_SIZE = 15
    SUBTITLE_SIZE = 10.5
    SECTION_SIZE = 10
    BODY_SIZE = 10


def _palette(theme: str):
    return LightPalette if theme == "light" else DarkPalette


def build_stylesheet(theme: str = "dark") -> str:
    c = _palette(theme)

    return f"""
    QMainWindow, QWidget {{
        background-color: {c.BACKGROUND};
        color: {c.TEXT};
        font-family: {Fonts.FAMILY};
        font-size: {Fonts.BODY_SIZE}pt;
    }}

    QLabel#AppTitle {{
        font-size: {Fonts.TITLE_SIZE}pt;
        font-weight: 600;
        letter-spacing: 2px;
        color: {c.TEXT};
    }}

    QLabel#AppSubtitle {{
        font-size: {Fonts.SUBTITLE_SIZE}pt;
        color: {c.TEXT_SECONDARY};
    }}

    QFrame#HeroDivider {{
        background-color: {c.BORDER};
        border: none;
    }}

    QWidget#WindowHeader {{
        background-color: {c.SURFACE};
        border-bottom: 1px solid {c.BORDER};
    }}

    QLabel#WindowTitle {{
        font-size: {Fonts.WINDOW_TITLE_SIZE}pt;
        font-weight: 600;
    }}

    QPushButton#BackButton {{
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 3px;
        padding: 4px 10px;
        color: {c.TEXT_SECONDARY};
        font-weight: 500;
    }}

    QPushButton#BackButton:hover {{
        background-color: {c.SURFACE_ALT};
        border: 1px solid {c.BORDER};
        color: {c.TEXT};
    }}

    QLabel#SectionHeader {{
        font-size: {Fonts.SECTION_SIZE}pt;
        font-weight: 600;
        letter-spacing: 1.5px;
        color: {c.TEXT_SECONDARY};
        padding-left: 2px;
    }}

    QLabel#MutedLabel {{
        color: {c.TEXT_SECONDARY};
        font-style: italic;
    }}

    QLabel#StatusLabel {{
        color: {c.TEXT_SECONDARY};
    }}

    QLabel#StatusValue {{
        color: {c.TEXT};
        font-weight: 600;
    }}

    QLabel#PanelTitle {{
        font-size: {Fonts.SECTION_SIZE}pt;
        font-weight: 600;
        letter-spacing: 1px;
        color: {c.TEXT_SECONDARY};
        padding-bottom: 4px;
        border-bottom: 1px solid {c.BORDER};
        margin-bottom: 4px;
    }}

    QFrame#Panel {{
        background-color: {c.SURFACE};
        border: 1px solid {c.BORDER};
        border-radius: 4px;
    }}

    QPushButton {{
        background-color: {c.SURFACE_ALT};
        border: 1px solid {c.BORDER};
        border-radius: 3px;
        padding: 6px 14px;
        color: {c.TEXT};
    }}

    QPushButton:hover {{
        background-color: {c.BORDER};
    }}

    QPushButton:disabled {{
        color: {c.TEXT_SECONDARY};
        background-color: {c.SURFACE};
    }}

    QPushButton#PrimaryButton {{
        background-color: {c.PRIMARY};
        border: 1px solid {c.PRIMARY};
        color: {c.ON_PRIMARY};
        font-weight: 600;
    }}

    QPushButton#PrimaryButton:hover {{
        background-color: {c.PRIMARY_HOVER};
    }}

    QPushButton#SecondaryButton {{
        background-color: transparent;
        border: 1px solid {c.BORDER};
    }}

    QPushButton#SecondaryButton:hover {{
        background-color: {c.SURFACE_ALT};
    }}

    QPushButton#DangerButton {{
        background-color: transparent;
        border: 1px solid {c.DANGER};
        color: {c.DANGER};
    }}

    QPushButton#DangerButton:hover {{
        background-color: {c.DANGER};
        color: {c.ON_PRIMARY};
    }}

    QPushButton#MissionCardButton {{
        background-color: {c.SURFACE_ALT};
        border: none;
        border-left: 3px solid {c.PRIMARY};
        border-radius: 2px;
        font-size: 10.5pt;
        font-weight: 600;
        text-align: left;
        padding-left: 14px;
    }}

    QPushButton#MissionCardButton:hover {{
        background-color: {c.BORDER};
    }}

    QPushButton#NavButton {{
        text-align: left;
        padding-left: 12px;
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 2px;
    }}

    QPushButton#NavButton:hover {{
        background-color: {c.SURFACE_ALT};
        border: 1px solid {c.BORDER};
    }}

    QListWidget#MissionLog {{
        background-color: {c.BACKGROUND};
        border: 1px solid {c.BORDER};
        border-radius: 3px;
        font-family: {Fonts.MONO_FAMILY};
        font-size: 9pt;
        color: {c.TEXT_SECONDARY};
    }}

    QListWidget#EntitiesList {{
        background-color: {c.BACKGROUND};
        border: 1px solid {c.BORDER};
        border-radius: 3px;
        font-size: 9pt;
    }}

    QListWidget#EntitiesList::item:selected {{
        background-color: {c.PRIMARY};
        color: {c.ON_PRIMARY};
    }}

    QDoubleSpinBox {{
        background-color: {c.SURFACE_ALT};
        border: 1px solid {c.BORDER};
        border-radius: 3px;
        padding: 3px;
        padding-right: 4px;
    }}

    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
        subcontrol-origin: border;
        width: 16px;
        border-left: 1px solid {c.BORDER};
        background-color: {c.SURFACE_ALT};
    }}

    QDoubleSpinBox::up-button {{
        subcontrol-position: top right;
        border-top-right-radius: 3px;
        border-bottom: 1px solid {c.BORDER};
        height: 11px;
    }}

    QDoubleSpinBox::down-button {{
        subcontrol-position: bottom right;
        border-bottom-right-radius: 3px;
        height: 11px;
    }}

    QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
        background-color: {c.BORDER};
    }}

    QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed {{
        background-color: {c.PRIMARY};
    }}

    QDoubleSpinBox::up-arrow {{
        width: 0px;
        height: 0px;
        border-left: 3px solid transparent;
        border-right: 3px solid transparent;
        border-bottom: 4px solid {c.TEXT_SECONDARY};
    }}

    QDoubleSpinBox::down-arrow {{
        width: 0px;
        height: 0px;
        border-left: 3px solid transparent;
        border-right: 3px solid transparent;
        border-top: 4px solid {c.TEXT_SECONDARY};
    }}

    QFrame#MapView {{
        border: 1px solid {c.BORDER};
        border-radius: 3px;
    }}

    QComboBox, QSlider {{
        background-color: {c.SURFACE_ALT};
        border: 1px solid {c.BORDER};
        border-radius: 3px;
        padding: 3px;
    }}

    QScrollBar:vertical {{
        background: {c.BACKGROUND};
        width: 10px;
    }}

    QScrollBar::handle:vertical {{
        background: {c.BORDER};
        border-radius: 5px;
    }}

    QWidget#StatusBar {{
        background-color: {c.PRIMARY};
    }}

    QLabel#StatusBarLabel {{
        color: {c.ON_PRIMARY};
        font-size: 9pt;
    }}
    """

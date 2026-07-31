from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea

from gui.components.window_header import WindowHeader
from gui.components.panel import Panel
from gui.components.section_header import SectionHeader
from gui.translations import tr

# Roadmap content is bilingual UI copy (not a project "fact" like the About
# fields), so it lives here as a small language-keyed table rather than in
# translations.py's flat string dictionary — each entry is a whole
# (title, description) pair, grouped by area.
ROADMAP = {
    "en": [
        (
            "Simulation",
            [
                (
                    "Improved Fire Spread Logic",
                    "Wind, vegetation and terrain-aware spread, instead of a "
                    "fixed radius growth rate.",
                ),
                (
                    "Map Introduction",
                    "A real georeferenced base map behind the Simulation "
                    "View, instead of a plain coordinate grid.",
                ),
                (
                    "Additional Missions",
                    "Maritime Surveillance, Search and Rescue, Border "
                    "Surveillance and more, on top of the same domain.",
                ),
            ],
        ),
        (
            "Interface",
            [
                (
                    "Fully Functional Settings",
                    "Theme, language, speed and units already work live — "
                    "next: persist them between sessions.",
                ),
                (
                    "Improved Visualization",
                    "Zoom/pan on the Simulation View, entity trails, and "
                    "satellite footprint overlays.",
                ),
                (
                    "Improved Display & Graphics",
                    "Higher-fidelity icons, animations for detection/alert "
                    "events, and a further refined dark/light palette.",
                ),
                (
                    "Entity Editing",
                    "Edit an existing satellite's or fire's properties, not "
                    "just add or remove it.",
                ),
            ],
        ),
        (
            "Platform",
            [
                (
                    "Save / Load Scenarios",
                    "Persist a World's entities and simulation state to a "
                    "file and reload it later.",
                ),
                (
                    "Mission Replay",
                    "Scrub back through past simulation steps instead of "
                    "only watching live.",
                ),
                (
                    "Automated Tests",
                    "A test suite over the domain layer to protect its "
                    "behaviour as the project grows.",
                ),
            ],
        ),
    ],
    "pt": [
        (
            "Simulação",
            [
                (
                    "Lógica de Propagação Melhorada",
                    "Propagação influenciada por vento, vegetação e "
                    "terreno, em vez de um raio de crescimento fixo.",
                ),
                (
                    "Introdução de Mapa",
                    "Um mapa base georreferenciado real na Simulation "
                    "View, em vez de uma grelha de coordenadas simples.",
                ),
                (
                    "Missões Adicionais",
                    "Vigilância Marítima, Busca e Salvamento, Vigilância "
                    "de Fronteiras, entre outras, sobre o mesmo domínio.",
                ),
            ],
        ),
        (
            "Interface",
            [
                (
                    "Definições Totalmente Funcionais",
                    "Tema, idioma, velocidade e unidades já funcionam ao "
                    "vivo — a seguir: persistência entre sessões.",
                ),
                (
                    "Visualização Melhorada",
                    "Zoom/pan na Simulation View, rastos de entidades e "
                    "sobreposição da área de deteção dos satélites.",
                ),
                (
                    "Display e Gráficos Melhorados",
                    "Ícones com mais detalhe, animações para eventos de "
                    "deteção/alerta, e paleta clara/escura mais refinada.",
                ),
                (
                    "Edição de Entidades",
                    "Editar propriedades de um satélite ou fogo já "
                    "existente, não só adicionar ou remover.",
                ),
            ],
        ),
        (
            "Plataforma",
            [
                (
                    "Guardar / Carregar Cenários",
                    "Persistir as entidades e o estado da simulação de um "
                    "World num ficheiro e recarregá-lo depois.",
                ),
                (
                    "Replay da Missão",
                    "Recuar por passos anteriores da simulação, em vez de "
                    "só ver em direto.",
                ),
                (
                    "Testes Automatizados",
                    "Um conjunto de testes sobre a camada de domínio para "
                    "proteger o seu comportamento à medida que o projeto "
                    "cresce.",
                ),
            ],
        ),
    ],
}


class ComingSoonWindow(QMainWindow):
    """Static V2 roadmap screen: what's planned next, grouped by area.

    Nothing here is wired to real behaviour, on purpose — it's a statement
    of intent, not a feature. It exists so a reviewer (recruiter,
    professor, engineer) can see at a glance that the project's current
    limitations are known and already have a plan attached to them.
    """

    coming_soon_closed = Signal()

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self._setup_window()

    def _setup_window(self):
        lang = self.settings.language
        self.setWindowTitle(tr("coming_soon", lang))
        self.resize(1000, 750)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = WindowHeader(tr("coming_soon", lang))
        root.addWidget(header)
        header.back_button.clicked.connect(self.close)

        root.addWidget(self._create_scroll_area(lang), stretch=1)

    def _create_scroll_area(self, lang: str) -> QScrollArea:
        content_widget = QWidget()
        content = QVBoxLayout(content_widget)
        content.setContentsMargins(24, 16, 24, 24)
        content.setSpacing(18)

        for section_title, items in ROADMAP.get(lang, ROADMAP["en"]):
            content.addWidget(SectionHeader(section_title))
            content.addWidget(self._create_section_panel(items))

        content.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setWidget(content_widget)
        return scroll_area

    def _create_section_panel(self, items) -> Panel:
        panel = Panel()
        for title, description in items:
            title_label = QLabel(title)
            title_label.setObjectName("StatusValue")
            panel.add_widget(title_label)

            description_label = QLabel(description)
            description_label.setObjectName("MutedLabel")
            description_label.setWordWrap(True)
            panel.add_widget(description_label)

        return panel

    def closeEvent(self, event):
        self.coming_soon_closed.emit()
        super().closeEvent(event)

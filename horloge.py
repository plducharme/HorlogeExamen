from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QLabel, QMainWindow, QGridLayout, QFrame, QMenu

from datetime import datetime, timedelta


class HorlogeExamen(QMainWindow):

    def __init__(self):
        super().__init__()
        # Initialisation de la barre de menu par défaut du QMainWindow
        self.__barre_menu = self.menuBar()
        # Menu Fichier
        self.__menu_fichier = QMenu("&Fichier")
        self.__barre_menu.addMenu(self.__menu_fichier)

        self.__action_configuration = QAction("&Configuration")
        self.__action_configuration.triggered.connect(self.__action_configuration_triggered)
        self.__menu_fichier.addAction(self.__action_configuration)

        self.__menu_fichier.addSeparator()

        self.__action_quitter = QAction("&Quitter")
        self.__action_quitter.triggered.connect(self.close)
        self.__action_quitter.setShortcut("Ctrl+Q")

        # QFrame principal
        self.__disposition_principale = QGridLayout()
        self.__widget_central = QFrame()
        self.__widget_central.setLayout(self.__disposition_principale)
        self.setCentralWidget(self.__widget_central)

        self.__configuration_examen = ConfigurationExamen()

    def __action_configuration_triggered(self):
        pass


class ConfigurationExamen:

    def __init__(self):
        # On utilise des objets datetime car timedelta ne fonctionne pas avec seulement time
        self.__heure_debut: datetime = datetime.now()
        self.__duree_examen: datetime = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)
        self.__duree_examen_saide: datetime = self.__duree_examen.replace(hour=4)
        self.__duree_examen_saide_override: bool = False

    @property
    def heure_debut(self) -> datetime:
        return self.__heure_debut

    @heure_debut.setter
    def heure_debut(self, heure: datetime):
        self.__heure_debut = heure

    @property
    def duree_examen(self) -> datetime:
        return self.__duree_examen

    @duree_examen.setter
    def duree_examen(self, duree: datetime):
        self.__duree_examen = duree
        self.ajuster_temps_saide()

    @property
    def duree_examen_saide(self):
        return self.__duree_examen_saide

    @duree_examen_saide.setter
    def duree_examen_saide(self, duree: datetime):
        self.__duree_examen_saide = duree

    # Si on n'override pas la durée pour le SAIDE, le tiers du temps est ajouté
    def ajuster_temps_saide(self):
        if not self.__duree_examen_saide_override:
            duree_minutes = self.__duree_examen.hour * 60 + self.__duree_examen.minute
            self.__duree_examen_saide = self.__duree_examen + timedelta(minutes=duree_minutes / 3)


if __name__ == "__main__":
    app = QApplication()
    horloge_examen = HorlogeExamen()
    horloge_examen.show()
    app.exec()



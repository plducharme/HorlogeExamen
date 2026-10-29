from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QLabel, QMainWindow, QGridLayout, QFrame, QMenu

from datetime import datetime, timedelta


class HorlogeExamen(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Horloge Examen v0.1")

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

        self.__libelle_heure_actuelle_valeur = QLabel(datetime.now().strftime("%H:%M:%S"))
        self.__libelle_heure_actuelle_valeur.setObjectName("heure_actuelle")

        self.__libelle_heure_debut = QLabel("Heure de début:")
        self.__libelle_heure_debut_valeur = QLabel(self.__configuration_examen.heure_debut.strftime("%H:%M:%S"))

        self.__libelle_heure_fin = QLabel("Heure de fin:")
        self.__libelle_heure_fin_valeur = QLabel(self.__configuration_examen.heure_fin.strftime("%H:%M:%S"))

        self.__libelle_heure_fin_saide = QLabel("Heure de fin SAIDE:")
        self.__libelle_heure_fin_saide_valeur = QLabel(self.__configuration_examen.heure_debut.strftime("%H:%M:%S"))

        self.creer_disposition()

        # QTimer pour rafraichir le temps (1 seconde par défaut)
        self.__qtimer = QTimer(interval=1000)
        # La méthode qui sera appelée à chaque interval
        self.__qtimer.timeout.connect(self.__mise_a_jour_temps)
        self.__qtimer.start()

    def creer_disposition(self):
        # PySide ne peut faire une second setLayout(), il faut donce refaire le widget si on veut recréer un layout
        # au complet; plus simple que de faire des "remove"
        self.__widget_central = QFrame()
        self.__disposition_principale = QGridLayout()
        self.__widget_central.setLayout(self.__disposition_principale)
        self.setCentralWidget(self.__widget_central)

        self.__disposition_principale.addWidget(self.__libelle_heure_actuelle_valeur, 1, 1, 1, 3)
        if self.__configuration_examen.afficher_heure_debut:
            self.__disposition_principale.addWidget(self.__libelle_heure_debut, 2, 1)
            self.__disposition_principale.addWidget(self.__libelle_heure_debut_valeur, 2, 2, 1, 2)
        if self.__configuration_examen.afficher_heure_fin:
            self.__disposition_principale.addWidget(self.__libelle_heure_fin, 3, 1)
            self.__disposition_principale.addWidget(self.__libelle_heure_fin_valeur, 3, 2, 1, 2)
        if self.__configuration_examen.afficher_heure_fin_saide:
            self.__disposition_principale.addWidget(self.__libelle_heure_fin_saide, 4, 1)

        self.__widget_central.setLayout(self.__disposition_principale)

    def __mise_a_jour_temps(self):
        self.__libelle_heure_actuelle_valeur.setText(datetime.now().strftime("%H:%M:%S"))

    def __action_configuration_triggered(self):
        pass


class ConfigurationExamen:

    def __init__(self, heure_debut: datetime = datetime.now(),
                 duree_examen: datetime = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0),
                 duree_examen_saide: datetime = datetime.now().replace(hour=4, minute=0, second=0, microsecond=0),
                 duree_examen_saide_override: bool = False,
                 afficher_heure_debut: bool = True,
                 afficher_heure_fin: bool = True,
                 afficher_heure_fin_saide: bool = True,
                 afficher_temps_restant: bool = True,
                 afficher_temps_restant_saide: bool = True,
                 afficher_horloge: bool = False,
                 afficher_graphique: bool = False):
        # On utilise des objets datetime car timedelta ne fonctionne pas avec seulement time
        self.__heure_debut: datetime = heure_debut
        self.__duree_examen: datetime = duree_examen
        self.__duree_examen_saide: datetime = duree_examen_saide
        self.__duree_examen_saide_override: bool = duree_examen_saide_override

        self.__afficher_heure_debut = afficher_heure_debut
        self.__afficher_heure_fin = afficher_heure_fin
        self.__afficher_heure_fin_saide = afficher_heure_fin_saide
        self.__afficher_temps_restant = afficher_temps_restant
        self.__afficher_temps_restant_saide = afficher_temps_restant_saide
        self.__afficher_horloge = afficher_horloge
        self.__afficher_graphique = afficher_graphique

        duree_minutes = self.__duree_examen.hour * 60 + self.__duree_examen.minute
        self.__heure_fin = self.__heure_debut + timedelta(minutes=duree_minutes)

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

    @property
    def afficher_heure_debut(self) -> bool:
        return self.__afficher_heure_debut

    @afficher_heure_debut.setter
    def afficher_heure_debut(self, afficher: bool):
        self.__afficher_heure_debut = afficher

    @property
    def duree_examen_saide_override(self) -> bool:
        return self.__duree_examen_saide_override

    @duree_examen_saide_override.setter
    def duree_examen_saide_override(self, override: bool):
        self.__duree_examen_saide_override = override

    @property
    def afficher_heure_fin(self) -> bool:
        return self.__afficher_heure_fin

    @afficher_heure_fin.setter
    def afficher_heure_fin(self, afficher: bool):
        self.__afficher_heure_fin = afficher

    @property
    def afficher_heure_fin_saide(self) -> bool:
        return self.__afficher_heure_fin_saide

    @afficher_heure_fin_saide.setter
    def afficher_heure_fin_saide(self, afficher: bool):
        self.__afficher_heure_fin_saide = afficher

    @property
    def afficher_temps_restant(self) -> bool:
        return self.__afficher_temps_restant

    @afficher_temps_restant.setter
    def afficher_temps_restant(self, afficher: bool):
        self.__afficher_temps_restant = afficher

    @property
    def afficher_temps_restant_saide(self) -> bool:
        return self.__afficher_temps_restant_saide

    @afficher_temps_restant_saide.setter
    def afficher_temps_restant_saide(self, afficher: bool):
        self.__afficher_temps_restant_saide = afficher

    @property
    def afficher_horloge(self) -> bool:
        return self.__afficher_horloge

    @afficher_horloge.setter
    def afficher_horloge(self, afficher: bool):
        self.__afficher_horloge = afficher

    @property
    def afficher_graphique(self) -> bool:
        return self.__afficher_graphique

    @afficher_graphique.setter
    def afficher_graphique(self, afficher: bool):
        self.__afficher_graphique = afficher

    @property
    def heure_fin(self) -> datetime:
        return self.__heure_fin

    @heure_fin.setter
    def heure_fin(self, heure_fin: datetime):
        self.__heure_fin = heure_fin

    # Si on n'override pas la durée pour le SAIDE, le tiers du temps est ajouté
    def ajuster_temps_saide(self):
        if not self.__duree_examen_saide_override:
            duree_minutes = self.__duree_examen.hour * 60 + self.__duree_examen.minute
            self.__duree_examen_saide = self.__duree_examen + timedelta(minutes=duree_minutes / 3)


if __name__ == "__main__":
    app = QApplication()
    with open("app.qss", "r", encoding="utf8") as qss:
        try:
            styles = qss.read()
            app.setStyleSheet(styles)
        except FileNotFoundError as e:
            print("Impossible de charger le qss", e)

    horloge_examen = HorlogeExamen()
    horloge_examen.show()
    app.exec()

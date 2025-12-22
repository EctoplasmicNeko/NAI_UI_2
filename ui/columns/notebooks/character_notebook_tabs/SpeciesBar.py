from PySide6.QtWidgets import QFrame, QGridLayout, QToolButton, QButtonGroup
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, Signal
from signaling.speciesbaronoff import species_bar_on_off

class SpeciesBar(QFrame):
    species_changed = Signal(str)   # <-- here's the signal

    def __init__(self, parent, image_cache):
        super().__init__(parent)
        self.image_cache = image_cache
        self.build_species_bar()
        species_bar_on_off.on_signal.connect(self.hide_species_bar)

    def build_species_bar(self):    
        grid = QGridLayout(self)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)

        # swap these paths for your real ones
        icons = {
            "human":    (self.image_cache['images']['species_icons']['human_off'],    self.image_cache['images']['species_icons']['human_on']),
            "cat":      (self.image_cache['images']['species_icons']['cat_off'],      self.image_cache['images']['species_icons']['cat_on']),
            "dog":      (self.image_cache['images']['species_icons']['dog_off'],      self.image_cache['images']['species_icons']['dog_on']),
            "fox":      (self.image_cache['images']['species_icons']['fox_off'],      self.image_cache['images']['species_icons']['fox_on']),
            "rabbit":   (self.image_cache['images']['species_icons']['rabbit_off'],   self.image_cache['images']['species_icons']['rabbit_on']),
            "squirrel": (self.image_cache['images']['species_icons']['squirrel_off'], self.image_cache['images']['species_icons']['squirrel_on']),
            "angel": (self.image_cache['images']['species_icons']['angel_off'], self.image_cache['images']['species_icons']['angel_on']),
            "demon": (self.image_cache['images']['species_icons']['demon_off'], self.image_cache['images']['species_icons']['demon_on'])
        }


        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for col, (name, (off_path, on_path)) in enumerate(icons.items()):
            btn = QToolButton(self)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setIconSize(QSize(44, 44))
            btn.setFixedSize(44, 44)

            icon = QIcon()
            icon.addPixmap(QPixmap(off_path), QIcon.Normal, QIcon.Off)
            icon.addPixmap(QPixmap(on_path),  QIcon.Normal, QIcon.On)
            btn.setIcon(icon)
            btn.setToolTip(name.capitalize())

            grid.addWidget(btn, 0, col, Qt.AlignmentFlag.AlignBottom| Qt.AlignmentFlag.AlignCenter)
            self.button_group.addButton(btn, col)

            # capture name in lambda so each button emits its own species
            btn.toggled.connect(lambda checked, n=name: self._emit_species(checked, n))

        # pick a default
        if self.button_group.buttons():
            self.button_group.buttons()[0].setChecked(True)

    def _emit_species(self, checked: bool, name: str):
        if checked:
            self.species_changed.emit(name)

    def hide_species_bar(self, show: bool):
        if show:
            self.show()
        else:
            self.hide()
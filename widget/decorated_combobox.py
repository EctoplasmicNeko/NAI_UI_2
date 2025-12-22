from PySide6.QtWidgets import QComboBox, QStyleOptionComboBox, QStyle
from PySide6.QtGui import QPainter


class DecoratedComboBox(QComboBox):
    """
    QComboBox that can show a prefix/suffix like QDoubleSpinBox,
    without polluting the underlying item texts.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._prefix = ""
        self._suffix = ""

    # --- Prefix / suffix API ---

    def setPrefix(self, prefix: str) -> None:
        self._prefix = prefix or ""
        self.update()

    def prefix(self) -> str:
        return self._prefix

    def setSuffix(self, suffix: str) -> None:
        self._suffix = suffix or ""
        self.update()

    def suffix(self) -> str:
        return self._suffix

    # --- Painting / display ---

    def paintEvent(self, event):
        """
        Draw like a normal QComboBox, but with:
            prefix + currentText + suffix
        as the visible text.
        """
        painter = QPainter(self)
        option = QStyleOptionComboBox()
        self.initStyleOption(option)

        base_text = super().currentText()
        if base_text:
            option.currentText = f"{self._prefix}{base_text}{self._suffix}"
        else:
            # if no selection, still show prefix/suffix if you want
            option.currentText = f"{self._prefix}{self._suffix}"

        style = self.style()
        style.drawComplexControl(QStyle.CC_ComboBox, option, painter, self)
        style.drawControl(QStyle.CE_ComboBoxLabel, option, painter, self)

    # --- Keep the logical value clean ---

    def currentText(self) -> str:  # type: ignore[override]
        """
        Return the *raw* combo text (no prefix/suffix).
        """
        return super().currentText()

    def setCurrentText(self, text: str) -> None:  # type: ignore[override]
        """
        Accept both raw and decorated values; if the caller passes
        prefix+text+suffix, we strip those off.
        """
        if self._prefix and text.startswith(self._prefix):
            text = text[len(self._prefix):]
        if self._suffix and text.endswith(self._suffix):
            text = text[:-len(self._suffix)]
        super().setCurrentText(text)

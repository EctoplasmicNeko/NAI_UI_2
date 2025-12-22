from PySide6.QtWidgets import QAbstractSpinBox
from PySide6.QtGui import QValidator
from PySide6.QtCore import Signal


class SeedSpinBox(QAbstractSpinBox):
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._minimum = 0
        self._maximum = 4294967294  # full NAI range
        self._single_step = 1

        self._special_value_text = ""  # e.g. "Random" (when value == minimum)

        self._validator = _SeedValidator(self._maximum)
        self.lineEdit().setValidator(self._validator)

        self._update_display_from_value()
        self.editingFinished.connect(self._on_editing_finished)

    # ---- public-ish API ----

    def value(self) -> int:
        return self._value

    def setValue(self, value: int):
        value = int(value)
        value = max(self._minimum, min(self._maximum, value))
        if value != self._value:
            self._value = value
            self._update_display_from_value()
            self.valueChanged.emit(self._value)

    def setRange(self, minimum: int, maximum: int):
        self._minimum = int(minimum)
        self._maximum = int(maximum)
        self._validator = _SeedValidator(self._maximum)
        self.lineEdit().setValidator(self._validator)
        self.setValue(self._value)  # re-clamp + refresh text

    def setSingleStep(self, step: int):
        self._single_step = max(1, int(step))

    def setSpecialValueText(self, text: str):
        """Show this text when value == minimum (like QSpinBox)."""
        self._special_value_text = text
        self._update_display_from_value()

    def specialValueText(self) -> str:
        return self._special_value_text

    # ---- QAbstractSpinBox overrides ----

    def stepEnabled(self):
        from PySide6.QtWidgets import QAbstractSpinBox as QASB
        flags = QASB.StepEnabledFlag(0)
        if self._value > self._minimum:
            flags |= QASB.StepDownEnabled
        if self._value < self._maximum:
            flags |= QASB.StepUpEnabled
        return flags

    def stepBy(self, steps: int):
        self.setValue(self._value + steps * self._single_step)

    def focusInEvent(self, event):
        # When entering the field, show the numeric value (so typing works)
        super().focusInEvent(event)
        if self._special_value_text and self._value == self._minimum:
            self.lineEdit().setText(str(self._minimum))
            self.lineEdit().selectAll()

    # ---- internals ----

    def _update_display_from_value(self):
        if self._special_value_text and self._value == self._minimum:
            # show special label instead of "0"
            self.lineEdit().setText(self._special_value_text)
        else:
            self.lineEdit().setText(str(self._value))

    def _on_editing_finished(self):
        text = self.lineEdit().text()

        # If they left the special text alone, just snap back to min
        if self._special_value_text and text == self._special_value_text:
            self.setValue(self._minimum)
            return

        if text == "":
            text = str(self._minimum)

        try:
            val = int(text)
        except ValueError:
            # bad text → snap back to current value
            self._update_display_from_value()
            return

        self.setValue(val)


class _SeedValidator(QValidator):
    def __init__(self, maximum: int, parent=None):
        super().__init__(parent)
        self._maximum = maximum

    def validate(self, input_str: str, pos: int):
        if input_str == "":
            return QValidator.Intermediate, input_str, pos
        if not input_str.isdigit():
            return QValidator.Invalid, input_str, pos
        try:
            val = int(input_str)
        except ValueError:
            return QValidator.Invalid, input_str, pos

        if 0 <= val <= self._maximum:
            return QValidator.Acceptable, input_str, pos
        return QValidator.Intermediate, input_str, pos

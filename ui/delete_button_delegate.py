from PyQt5.QtWidgets import QStyledItemDelegate, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from database import delete_appointment


class DeleteButtonDelegate(QStyledItemDelegate):
    deleted = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        painter.save()
        painter.drawText(option.rect, Qt.AlignCenter, "🗑 Delete")
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if event.type() != event.MouseButtonRelease:
            return False

        row = index.row()

        try:
            appointment_id = int(model._df.iloc[row]["id"])
        except Exception as e:
            QMessageBox.critical(
                option.widget,
                "Delete error",
                f"Could not resolve appointment ID:\n{e}"
            )
            return True

        confirm = QMessageBox.question(
            option.widget,
            "Confirm delete",
            "Delete this appointment?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return True

        # ---- DELETE FROM DB ----
        delete_appointment(appointment_id)

        # ---- UPDATE MODEL ----
        model.beginResetModel()
        model._df.drop(model._df.index[row], inplace=True)
        model._df.reset_index(drop=True, inplace=True)
        model.endResetModel()

        self.deleted.emit()

        return True

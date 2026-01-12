from PyQt5.QtWidgets import QStyledItemDelegate, QPushButton, QMessageBox
from PyQt5.QtCore import QModelIndex
from database import delete_appointment

class DeleteButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent, refresh_callback):
        super().__init__(parent)
        self.refresh_callback = refresh_callback

    def createEditor(self, parent, option, index):
        button = QPushButton("🗑")
        button.setStyleSheet("""
            QPushButton {
                background-color: #e63946;
                color: white;
                border-radius: 6px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #c1121f;
            }
        """)

        button.clicked.connect(lambda: self.delete_row(index))
        return button

    def delete_row(self, index: QModelIndex):
        model = index.model()
        row = index.row()

        appointment_id = model._df.iloc[row]["id"]

        confirm = QMessageBox.question(
            None,
            "Delete Appointment",
            "Are you sure you want to delete this appointment?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            delete_appointment(appointment_id)
            self.refresh_callback()

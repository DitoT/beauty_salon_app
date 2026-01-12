from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QDateEdit,
    QDoubleSpinBox, QSpinBox
)
from PyQt5.QtCore import QDate, pyqtSignal
from database import insert_appointment

class AddAppointmentWindow(QWidget):
    appointment_saved = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Appointment")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout()

        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        self.date.setCalendarPopup(True)

        self.client = QLineEdit()
        self.service = QLineEdit()
        self.employee = QLineEdit()

        self.price = QDoubleSpinBox()
        self.price.setMaximum(10000)
        self.price.setSuffix(" ₾")

        self.duration = QSpinBox()
        self.duration.setMaximum(600)
        self.duration.setSuffix(" min")

        save_btn = QPushButton("Save Appointment")
        save_btn.clicked.connect(self.save)

        for label, widget in [
            ("Date", self.date),
            ("Client", self.client),
            ("Service", self.service),
            ("Employee", self.employee),
            ("Price", self.price),
            ("Duration", self.duration),
        ]:
            layout.addWidget(QLabel(label))
            layout.addWidget(widget)

        layout.addWidget(save_btn)
        self.setLayout(layout)

    def save(self):
        if not self.client.text():
            QMessageBox.warning(self, "Error", "Client name required")
            return

        insert_appointment((
            self.date.date().toString("yyyy-MM-dd"),
            self.client.text(),
            self.service.text(),
            self.employee.text(),
            self.price.value(),
            self.duration.value()
        ))

        self.appointment_saved.emit()
        self.close()

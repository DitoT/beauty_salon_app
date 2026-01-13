from PyQt5.QtGui import QFont
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
        self.setFixedSize(350, 500)

        layout = QVBoxLayout()
        font_label = QFont("Arial", 12, QFont.Bold)
        font_input = QFont("Arial", 12)
        input_height = 35

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
        save_btn.setFont(font_label)
        save_btn.setMinimumHeight(input_height + 5)
        save_btn.clicked.connect(self.save)

        fields = [
            ("Date", self.date),
            ("Client", self.client),
            ("Service", self.service),
            ("Employee", self.employee),
            ("Price", self.price),
            ("Duration", self.duration),
        ]

        for text, widget in fields:
            label = QLabel(text)
            label.setFont(font_label)
            layout.addWidget(label)

            widget.setFont(font_input)
            widget.setMinimumHeight(input_height)
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

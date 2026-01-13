from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QPushButton, QVBoxLayout, QTableView, QSizePolicy, QMessageBox
)
from database import load_appointments
from analytics.revenue_analysis import total_revenue, average_ticket, revenue_by_employee, revenue_by_service
from ui.table_model import PandasTableModel
from analytics.charts import RevenueChart
from ui.add_appointment import AddAppointmentWindow
from ui.delete_button_delegate import DeleteButtonDelegate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beauty Salon Manager")
        self.resize(900, 700)

        widget = QWidget()
        self.layout = QVBoxLayout()

        self.revenue = QLabel()
        self.avg_ticket = QLabel()

        # Revenue by employee
        self.revenue_by_employee = QLabel()
        self.revenue_by_employee.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Maximum
        )

        # Revemue ny service
        self.revenue_by_service = QLabel()
        self.revenue_by_service.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Maximum
        )

        add_btn = QPushButton("Add Appointment")
        add_btn.clicked.connect(self.open_add)

        self.table = QTableView()

        self.chart = RevenueChart()

        self.layout.addWidget(self.revenue)
        self.layout.addWidget(self.avg_ticket)
        self.layout.addWidget(add_btn)
        self.layout.addWidget(self.chart)
        self.layout.addWidget(self.table)

        self.layout.addWidget(self.revenue_by_employee)
        self.layout.addWidget(self.revenue_by_service)

        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.refresh()

    def refresh(self):
        df = load_appointments()

        # ---- Metrics ----
        self.revenue.setText(f"Total Revenue: {total_revenue(df):.2f} ₾")
        self.avg_ticket.setText(f"Avg Ticket: {average_ticket(df):.2f} ₾")

        rev_by_emp = revenue_by_employee(df)
        text = "Revenue by employee:\n"
        for employee, revenue in rev_by_emp.items():
            text += f"{employee}: {revenue:.2f} ₾\n"
        self.revenue_by_employee.setText(text)

        rev_by_serv = revenue_by_service(df)
        text = "Revenue by service:\n"
        for service, revenue in rev_by_serv.items():
            text += f"{service}: {revenue:.2f} ₾\n"
        self.revenue_by_service.setText(text)

        # ---- ADD DELETE COLUMN (THIS IS THE MAGIC) ----
        df = load_appointments().copy()
        df["Delete"] = ""

        # ---- SET TABLE MODEL ----
        model = PandasTableModel(df)
        self.table.setModel(model)

        # ---- ADD DELETE BUTTON DELEGATE ----
        delete_column_index = df.columns.get_loc("Delete")

        delegate = DeleteButtonDelegate(self.table)
        delegate.deleted.connect(self.refresh)
        self.table.setItemDelegateForColumn(delete_column_index, delegate)
        self.table.setColumnWidth(delete_column_index, 80)

        # ---- TABLE LOOK ----
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        # ---- CHART ----
        service_data = df.groupby("service")["price"].sum()
        self.chart.update_chart(service_data)

        # --- Hiding ID ---
        id_col = df.columns.get_loc("id")
        self.table.setColumnHidden(id_col, True)
        self.table.setSortingEnabled(False) # Disables sorting on Delete column

    def open_add(self):
        self.add_window = AddAppointmentWindow()
        self.add_window.appointment_saved.connect(self.refresh)
        self.add_window.show()



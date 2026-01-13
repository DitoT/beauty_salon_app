from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QTableView, QSizePolicy, QMessageBox
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
        self.resize(1100, 700)

        widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.revenue = QLabel()
        self.avg_ticket = QLabel()
        self.revenue_by_employee = QLabel()
        self.revenue_by_employee.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        self.revenue_by_service = QLabel()
        self.revenue_by_service.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)

        add_btn = QPushButton("Add Appointment")
        add_btn.clicked.connect(self.open_add)

        self.chart = RevenueChart()
        self.table = QTableView()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Top widgets
        self.layout.addWidget(self.revenue)
        self.layout.addWidget(self.avg_ticket)
        self.layout.addWidget(add_btn)
        self.layout.addWidget(self.chart)

        # Bottom horizontal layout: revenues left, table right
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)  # small gap between revenues and table

        # Revenue panel (left)
        revenues_layout = QVBoxLayout()
        revenues_layout.addWidget(self.revenue_by_employee)
        revenues_layout.addWidget(self.revenue_by_service)
        revenues_widget = QWidget()
        revenues_widget.setLayout(revenues_layout)
        revenues_widget.setFixedWidth(250)
        bottom_layout.addWidget(revenues_widget)

        # Table (right) - will expand fully to the right
        bottom_layout.addWidget(self.table)

        self.layout.addLayout(bottom_layout)
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.refresh()

    def refresh(self):
        df = load_appointments()

        self.revenue.setText(f"Total Revenue: {total_revenue(df):.2f} ₾")
        self.avg_ticket.setText(f"Avg Ticket: {average_ticket(df):.2f} ₾")

        rev_by_emp = revenue_by_employee(df)
        text_emp = "Revenue by employee:\n"
        for employee, revenue in rev_by_emp.items():
            text_emp += f"{employee}: {revenue:.2f} ₾\n"
        self.revenue_by_employee.setText(text_emp)

        rev_by_serv = revenue_by_service(df)
        text_serv = "Revenue by service:\n"
        for service, revenue in rev_by_serv.items():
            text_serv += f"{service}: {revenue:.2f} ₾\n"
        self.revenue_by_service.setText(text_serv)

        df_copy = df.copy()
        df_copy["Delete"] = ""

        model = PandasTableModel(df_copy)
        self.table.setModel(model)

        delete_column_index = df_copy.columns.get_loc("Delete")
        delegate = DeleteButtonDelegate(self.table)
        delegate.deleted.connect(self.refresh)
        self.table.setItemDelegateForColumn(delete_column_index, delegate)
        self.table.setColumnWidth(delete_column_index, 80)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        service_data = df.groupby("service")["price"].sum()
        self.chart.update_chart(service_data)

        id_col = df.columns.get_loc("id")
        self.table.setColumnHidden(id_col, True)
        self.table.setSortingEnabled(False)

    def open_add(self):
        self.add_window = AddAppointmentWindow()
        self.add_window.appointment_saved.connect(self.refresh)
        self.add_window.show()

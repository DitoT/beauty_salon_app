import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from database import create_tables


def main():
    create_tables()

    app = QApplication(sys.argv)

    # Responsive font
    screen = app.primaryScreen().size()
    font_size = 11 if screen.width() < 1366 else 12
    app.setFont(QFont("Segoe UI", font_size))

    # Global stylesheet
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f8f5f2;
        }

        QWidget {
            font-family: Segoe UI;
        }

        QFrame, QGroupBox, QTableView {
            background-color: white;
            border-radius: 12px;
        }

        QPushButton {
            background-color: #d4a373;
            color: white;
            padding: 10px 18px;
            border-radius: 10px;
        }

        QPushButton:hover {
            background-color: #b08968;
        }

        QPushButton:pressed {
            background-color: #a07555;
        }

        QPushButton:disabled {
            background-color: #ccc;
            color: #666;
        }

        QLineEdit, QComboBox, QDateEdit {
            padding: 8px;
            border-radius: 8px;
            border: 1px solid #ccc;
            background-color: white;
        }
    """)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
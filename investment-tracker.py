import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class InvestorTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Investor Tracker")
        self.setFixedSize(420, 680)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f1117;
            }
            QWidget#central {
                background-color: #0f1117;
            }
        """)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Investor Tracker")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #e8e8e8;
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 2px;
        """)
        layout.addWidget(title)

        subtitle = QLabel("VOO / QQQ P&L Calculator")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #555; font-size: 11px; letter-spacing: 1px;")
        layout.addWidget(subtitle)

        # Divider
        layout.addWidget(self._divider())

        # Input fields
        self.ticker_input = self._input_row(layout, "Ticker Symbol", "e.g. VOO or QQQ")
        self.buy_price_input = self._input_row(layout, "Buy Price (USD)", "e.g. 480.00")
        self.shares_input = self._input_row(layout, "Number of Shares", "e.g. 10")
        self.current_price_input = self._input_row(layout, "Current Price (USD)", "e.g. 510.00")

        # Calculate Button
        calc_btn = QPushButton("CALCULATE")
        calc_btn.setFixedHeight(48)
        calc_btn.setCursor(Qt.PointingHandCursor)
        calc_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 2px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        calc_btn.clicked.connect(self.calculate)
        layout.addWidget(calc_btn)

        # Divider
        layout.addWidget(self._divider())

        # Result area
        self.result_frame = QFrame()
        self.result_frame.setStyleSheet("""
            QFrame {
                background-color: #161b27;
                border: 1px solid #1e2d45;
                border-radius: 10px;
            }
        """)
        result_layout = QVBoxLayout(self.result_frame)
        result_layout.setContentsMargins(20, 16, 20, 16)
        result_layout.setSpacing(8)

        self.ticker_label = self._result_label("—", is_ticker=True)
        self.pnl_label = self._result_label("P&L: —")
        self.pct_label = self._result_label("Return: —")

        result_layout.addWidget(self.ticker_label)
        result_layout.addWidget(self.pnl_label)
        result_layout.addWidget(self.pct_label)

        layout.addWidget(self.result_frame)
        layout.addStretch()

    def _input_row(self, parent_layout, label_text, placeholder):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        v = QVBoxLayout(container)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(5)

        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: #8899aa; font-size: 11px; letter-spacing: 1px;")
        v.addWidget(lbl)

        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setFixedHeight(38)
        field.setStyleSheet("""
            QLineEdit {
                background-color: #161b27;
                color: #e8e8e8;
                border: 1px solid #1e2d45;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #2563eb;
            }
        """)
        v.addWidget(field)
        parent_layout.addWidget(container)
        return field

    def _result_label(self, text, is_ticker=False):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        if is_ticker:
            lbl.setStyleSheet("color: #8899aa; font-size: 13px; letter-spacing: 2px;")
        else:
            lbl.setStyleSheet("color: #e8e8e8; font-size: 15px; font-weight: bold;")
        return lbl

    def _divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #1e2d45;")
        return line

    def calculate(self):
        try:
            ticker = self.ticker_input.text().strip().upper() or "—"
            buy_price = float(self.buy_price_input.text())
            shares = float(self.shares_input.text())
            current_price = float(self.current_price_input.text())

            cost = buy_price * shares
            value = current_price * shares
            pnl = value - cost
            pct = (pnl / cost) * 100

            pnl_str = f"P&L: {'+'if pnl >= 0 else ''}{pnl:,.2f} USD"
            pct_str = f"Return: {'+'if pct >= 0 else ''}{pct:.2f}%"
            color = "#22c55e" if pnl >= 0 else "#ef4444"

            self.ticker_label.setText(ticker)
            self.pnl_label.setText(pnl_str)
            self.pct_label.setText(pct_str)

            self.pnl_label.setStyleSheet(f"color: {color}; font-size: 15px; font-weight: bold;")
            self.pct_label.setStyleSheet(f"color: {color}; font-size: 15px; font-weight: bold;")
            self.ticker_label.setStyleSheet(f"color: {color}; font-size: 13px; letter-spacing: 2px; font-weight: bold;")

        except ValueError:
            self.ticker_label.setText("Invalid input")
            self.pnl_label.setText("Please enter valid numbers.")
            self.pct_label.setText("")
            self.ticker_label.setStyleSheet("color: #ef4444; font-size: 13px;")
            self.pnl_label.setStyleSheet("color: #ef4444; font-size: 13px;")
            self.pct_label.setStyleSheet("color: #555; font-size: 13px;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvestorTracker()
    window.show()
    sys.exit(app.exec_())
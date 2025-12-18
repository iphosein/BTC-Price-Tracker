import pytz
from datetime import datetime
import sys
import time
import requests
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor
import pyqtgraph as pg

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(v).strftime("%H:%M") for v in values]

class BTCTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bitcoin Price Tracker")
        self.resize(1000, 720)
        self.setStyleSheet("background: #0d1117; color: #c9d1d9;")
        self.last_color = "#f0b90b"

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)

        # Title
        title = QLabel("BTC / USDT")
        title.setStyleSheet("font-size: 42px; font-weight: bold; color: #f0883e;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Current Price — changes color based on movement
        self.price_lbl = QLabel("$0.00")
        self.price_lbl.setStyleSheet("font-size: 78px; font-weight: bold; color: #f0b90b;")
        self.price_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.price_lbl)

        # 24h Change
        self.change_lbl = QLabel("24h: 0.00%")
        self.change_lbl.setStyleSheet("font-size: 30px; font-weight: bold;")
        self.change_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.change_lbl)

        # High / Low
        row = QHBoxLayout()
        row.setSpacing(30)
        self.high_lbl = QLabel("24h High: —")
        self.low_lbl = QLabel("24h Low: —")
        self.high_lbl.setStyleSheet("font-size: 24px; color: #00ff9d; background: #0a2e1c; padding: 16px 32px; border-radius: 14px; font-weight: bold;")
        self.low_lbl.setStyleSheet("font-size: 24px; color: #ff3b30; background: #3d0f17; padding: 16px 32px; border-radius: 14px; font-weight: bold;")
        row.addWidget(self.high_lbl)
        row.addWidget(self.low_lbl)
        layout.addLayout(row)

        # Source & Time
        self.source_lbl = QLabel("Connecting to CoinGecko...")
        self.source_lbl.setStyleSheet("color: #8b949e; font-size: 17px;")
        self.source_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.source_lbl)

        # Alert Input
        alert_layout = QHBoxLayout()
        self.alert_input = QLineEdit()
        self.alert_input.setPlaceholderText("Enter alert price (e.g. 100000)")
        self.alert_input.setStyleSheet("padding: 16px; font-size: 18px; border-radius: 12px; background: #161b22; border: 1px solid #30363d;")
        self.alert_input.setFixedHeight(60)
        btn = QPushButton("Set Alert")
        btn.setStyleSheet("background: #238636; color: white; font-weight: bold; font-size: 18px; border-radius: 12px;")
        btn.setFixedHeight(60)
        btn.clicked.connect(self.set_alert)
        alert_layout.addWidget(self.alert_input, 4)
        alert_layout.addWidget(btn, 1)
        layout.addLayout(alert_layout)

        # Chart
        self.graph = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.graph.setBackground("#161b22")
        self.graph.showGrid(x=True, y=True, alpha=0.15)
        self.graph.setLabel('left', 'Price (USD)', color='#c9d1d9')
        self.graph.setLabel('bottom', 'Time', color='#c9d1d9')
        layout.addWidget(self.graph, stretch=1)

        self.curve = self.graph.plot(pen=pg.mkPen('#58a6ff', width=3.5))
        self.high_line = self.graph.plot(pen=pg.mkPen('#00ff9d', width=2, style=Qt.DashLine))
        self.low_line = self.graph.plot(pen=pg.mkPen('#ff3b30', width=2, style=Qt.DashLine))

        self.x = []
        self.y = []
        self.last_price = None
        self.alert_price = None

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

        self.statusBar().showMessage("Connecting to server...")

        self.update_data()

    def update_data(self):
        try:
            data = requests.get("http://127.0.0.1:8080/bitcoin-price", timeout=5).json()
            price = data["price"]
            change_24h = data["change_24h"]


            if self.last_price is not None:
                if price > self.last_price:
                    price_color = "#00ff9d"
                    self.last_color = "#00ff9d"
                elif price < self.last_price:
                    price_color = "#ff3b30"
                    self.last_color = "#ff3b30"
                else:
                    price_color = getattr(self, "last_color", "#f0b90b")
            else:
                price_color = "#f0b90b"
                self.last_color = "#f0b90b"

            self.price_lbl.setText(f"${price:,.2f}")
            self.price_lbl.setStyleSheet(f"color: {price_color}; font-size: 78px; font-weight: bold;")

            # 24h change color
            if change_24h > 0:
                self.change_lbl.setText(f"24h: +{change_24h}%")
                self.change_lbl.setStyleSheet("color: #00ff9d; font-size: 30px; font-weight: bold;")
            elif change_24h < 0:
                self.change_lbl.setText(f"24h: {change_24h}%")
                self.change_lbl.setStyleSheet("color: #ff3b30; font-size: 30px; font-weight: bold;")
            else:
                self.change_lbl.setText(f"24h: {change_24h}%")
                self.change_lbl.setStyleSheet("color: #f0b90b; font-size: 30px; font-weight: bold;")

            self.high_lbl.setText(f"24h High: ${data['high_24h']:,.0f}")
            self.low_lbl.setText(f"24h Low: ${data['low_24h']:,.0f}")

            # self.source_lbl.setText(f"CoinGecko • Live • {time.strftime('%H:%M:%S')}")
            tz = pytz.timezone('Asia/Tehran')
            now = datetime.now(tz)
            time_str = now.strftime("%H:%M:%S")
            offset = now.strftime("%z")  # مثلاً +0330
            # تبدیل +0330 → UTC+3:30
            if offset:
                utc_offset = f"UTC{offset[:3]}:{offset[3:]}"
            else:
                utc_offset = "UTC"
            self.source_lbl.setText(f"CoinGecko • Live • {time_str} {utc_offset}")

            # Chart update
            now = time.time()
            self.x.append(now)
            self.y.append(price)
            if len(self.x) > 86400:
                self.x.pop(0)
                self.y.pop(0)

            self.curve.setData(self.x, self.y)
            self.high_line.setData(self.x, [data["high_24h"]] * len(self.x))
            self.low_line.setData(self.x, [data["low_24h"]] * len(self.x))
            self.graph.setXRange(now - 60, now + 5)
            self.last_price = price
            self.statusBar().showMessage("Live • Updated", 1000)

            # Alert trigger
            if self.alert_price and price >= self.alert_price:
                QMessageBox.information(self, "PRICE ALERT", f"Bitcoin reached ${price:,.2f}!")
                self.alert_price = None
                self.alert_input.clear()

        except:
            self.source_lbl.setText("Connection lost...")
            self.statusBar().showMessage("Connection error", 3000)

    def set_alert(self):
        text = self.alert_input.text().replace(",", "").strip()
        if not text:
            return
        try:
            self.alert_price = float(text)
            QMessageBox.information(self, "Alert Set", f"Alert set at ${self.alert_price:,.0f}")
            self.alert_input.clear()
        except:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BTCTracker()
    window.show()
    sys.exit(app.exec_())


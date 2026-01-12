from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class RevenueChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(5, 3))
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)

    def update_chart(self, data):
        self.ax.clear()

        if not data.empty:
            data.plot(kind="bar", ax=self.ax)

        self.ax.set_title("Revenue by Service")
        self.ax.set_ylabel("Revenue")
        self.fig.tight_layout()
        self.draw()

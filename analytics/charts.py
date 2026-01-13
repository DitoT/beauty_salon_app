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

        self.ax.set_title("Revenue by Service", fontsize=16)
        self.ax.set_ylabel("Revenue", fontsize=14)
        self.ax.set_xlabel("Service", fontsize=14)

        self.ax.tick_params(axis='x', labelsize=12)
        self.ax.tick_params(axis='y', labelsize=12)

        self.fig.tight_layout()
        self.draw()

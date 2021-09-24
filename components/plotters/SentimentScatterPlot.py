# rng = np.random.RandomState(0)
# x = rng.randn(100)
# y = rng.randn(100)
# colors = rng.rand(100)
# sizes = 1000 * rng.rand(100)

# plt.scatter(x, y, c=colors, s=sizes, alpha=0.3,
#             cmap='viridis')
# plt.colorbar();  # show color scale




import matplotlib.pyplot as plt


class SentimentScatterPlot:
    """
    Plots given data
    """

    def __init__(self, data, title, x_label, quick_run, y_label="Frequency", display_number=10):
        self.data = data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.display_number = display_number
        self.label_max_len = 12
        self.quick_run = quick_run


    def plot(self):
        try:
            x = self.data.keys()
            y = self.data.values()

            plt.scatter(x, y, cmap='viridis')
            plt.title(self.title)
            plt.xlabel(self.x_label)
            plt.ylabel(self.y_label)

            if self.quick_run:
                plt.show(block=False)
                plt.pause(1)
                plt.close()
            else:
                plt.show()
        except Exception as e:
            print(e)

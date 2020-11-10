import matplotlib.pyplot as plt


class SentimentPlotter:

    def __init__(self, data, title, x_label, y_label="Number of Comments", display_number=10):
        self.data = data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.display_number = display_number


    def plot(self):
        try:
            x = self.data.keys()
            y = self.data.values()

            plt.bar(x,y,align='center')
            plt.title(self.title)
            plt.xlabel(self.x_label)
            plt.ylabel(self.y_label)

            plt.show()
        except Exception as e:
            print(e)

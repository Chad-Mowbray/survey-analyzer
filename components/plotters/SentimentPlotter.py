import matplotlib.pyplot as plt


class SentimentPlotter:
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

            plt.bar(x,y,align='center')
            plt.title(self.title)
            plt.xlabel(self.x_label)
            plt.ylabel(self.y_label)
            # for i in range(len(y)):    # add a horizontal line for easier comparison
            #     plt.hlines(y[i],0,x[i])
            if self.quick_run:
                plt.show(block=False)
                plt.pause(1)
                plt.close()
            else:
                plt.show()
        except Exception as e:
            print(e)

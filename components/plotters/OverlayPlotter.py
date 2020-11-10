import matplotlib.pyplot as plt
import numpy as np



class OverlayPlotter:
    def __init__(self, base, other, topic):
        self.base = base
        self.other = other
        self.topic = topic
        self.width = 0.5


    def plot(self):
        width = 0.5

        color = None
        if self.other[2] > self.base[2]:
            color = "r"
        else:
            color = "g"

        indices = np.arange(len(self.base))

        plt.bar(indices + .1, self.base, width=self.width, 
                color='grey', label='Base Sentiment Distribution')
        plt.bar([i + 0.50 * self.width for i in indices], self.other, 
                width=0.8 * self.width, color=color, alpha=0.8, label=f'Sentiment Distribution for {self.topic}', align='edge')
        
        plt.title(f"Comparative Sentiment Analysis for {self.topic}")
        plt.xlabel("Sentiment")
        plt.ylabel("Percent of Comments")
        plt.ylim(0.0, 1.0)

        plt.xticks(indices + self.width / 2., 
                ["Positive", "Neutral", "Negative"] )

        plt.legend()

        plt.show()

import matplotlib.pyplot as plt
import numpy as np



class OverlayPlotter:
    def __init__(self, base, other, topic):
        self.base = base
        self.other = other
        self.topic = topic

    def plot(self):
        width = 0.5

        # highPower   = [1184.53,1523.48,1521.05,1517.88,1519.88,1414.98,
        #             1419.34,1415.13,1182.70,1165.17]
        # lowPower    = [1000.95,1233.37, 1198.97,1198.01,1214.29,1130.86,
        #             1138.70,1104.12,1012.95,1000.36]
        base = self.base
        other = self.other

        color = None
        if self.other[2] > self.base[2]:
            color = "r"
        else:
            color = "g"

        indices = np.arange(len(base))

        plt.bar(indices + .1, base, width=width, 
                color='grey', label='Base Sentiment Distribution')
        plt.bar([i+0.50*width for i in indices], other, 
                width=0.8*width, color=color, alpha=0.8, label=f'Sentiment Distribution for {self.topic}', align='edge')
        
        plt.title("Comparative Sentiment Analysis")
        plt.xlabel("Sentiment")
        plt.ylabel("Percent of Comments")
        plt.ylim(0.0, 1.0)

        plt.xticks(indices+width/2., 
                ["Positive", "Neutral", "Negative"] )

        plt.legend()

        plt.show()

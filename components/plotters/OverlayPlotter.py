import matplotlib.pyplot as plt
import numpy as np

width = 0.8

highPower   = [1184.53,1523.48,1521.05,1517.88,1519.88,1414.98,
               1419.34,1415.13,1182.70,1165.17]
lowPower    = [1000.95,1233.37, 1198.97,1198.01,1214.29,1130.86,
               1138.70,1104.12,1012.95,1000.36]

indices = np.arange(len(highPower))

plt.bar(indices, highPower, width=width, 
        color='b', label='Max Power in mW')
plt.bar([i+0.25*width for i in indices], lowPower, 
        width=0.5*width, color='r', alpha=0.5, label='Min Power in mW')

plt.xticks(indices+width/2., 
           ['T{}'.format(i) for i in range(len(highPower))] )

plt.legend()

plt.show()

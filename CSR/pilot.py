

import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0, 100)
y = np.linspace(0, 100)

plt.plot(x, y)
plt.savefig("test.png")
plt.show()

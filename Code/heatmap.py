import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Generate random data
data = np.random.rand(4, 4)

# Set up Seaborn heatmap
sns.set()
sns.heatmap(data, cmap="Blues", annot=True, cbar=False, square=True)

# Show plot
plt.show()

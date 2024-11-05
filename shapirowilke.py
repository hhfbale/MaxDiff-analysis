import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro, norm


#Data
data = np.random.normal(size=300)

#Visualization of data
plt.figure(figsize=(10,6))
plt.hist(data, bins=30, density=True, alpha=0.7, color='skyblue',  edgecolor='black')

x = np.linspace(data.min(), data.max(), 100)
y = norm.pdf(x, loc=data.mean(), scale=data.std())

plt.plot(x,y,'r-',lw=2,label='Normal Distribution')

plt.xlabel('Value')
plt.ylabel('Density')
plt.legend()
plt.show()


print(shapiro(x))
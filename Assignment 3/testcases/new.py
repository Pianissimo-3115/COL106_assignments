import matplotlib.pyplot as plt

# Data points for the first set
m_values = [
    2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576
]
times_1 = [
    0.0142, 0.0141, 0.0196, 0.2499, 0.0391, 0.0655, 0.1172,0.2680, 0.5336, 1.0257,
    2.1852, 5.1165, 10.2787, 19.5431, 39.9213, 677.9945, 750.3855, 850.9409,
    2034.6333, 3710.4211
]

# Data points for the second set
times_2 = [
    0.0104, 0.0104, 0.0113, 0.0174, 0.0261, 0.0444, 0.0917, 0.1608, 0.3505, 8.3259, 1.5512, 3.6634, 7.4165, 15.1377, 30.7905, 55.9317, 116.7203, 384.7993, 717.6430, 1427.4297
]

# Calculate the ratio of each value of "times"
ratios = [t1 / t2 for t1, t2 in zip(times_1, times_2)]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(m_values, ratios, marker='o', linestyle='-', color='g', label='Ratio of Times')

# Set the scale of the x-axis to logarithmic
plt.xscale('log', base=2)

# Add labels and title
plt.xlabel('Number of Crew Mates (m)')
plt.ylabel('Ratio of Times')
plt.title('Ratio of Initialization Times for StrawHatTreasury')
plt.grid(True)

# Add a legend
plt.legend()

# Show the plot
plt.show()
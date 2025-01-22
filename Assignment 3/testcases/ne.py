import matplotlib.pyplot as plt

# Data points
m_values = [
    2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576
]
times = [
    0.0224, 0.0098, 0.0202, 0.0194, 0.0348, 0.0690, 0.1144, 0.2743, 0.5203, 1.0465, 2.0810, 7.4973, 9.8733, 20.6443, 54.3909, 622.2642, 217.1685, 803.0470, 1955.2355, 3640.3903
]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(m_values, times, marker='o', linestyle='-', color='b')

# Set the scale of the x-axis to logarithmic
plt.xscale('log', base=2)

# Add labels and title
plt.xlabel('Number of Crew Mates (m)')
plt.ylabel('Time (ms)')
plt.title('StrawHatTreasury Initialization Time vs Number of Crew Mates')
plt.grid(True)

# Show the plot
plt.show()
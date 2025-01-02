import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data preparation
data = {
    "Method": ["Aligned", "Aligned", "Aligned", "Aligned",
               "Unrolled", "Unrolled", "Unrolled", "Unrolled",
               "Naive", "Naive", "Naive", "Naive",
               "Blocked", "Blocked", "Blocked", "Blocked"],
    "Threads": [2, 4, 8, 16,
                2, 4, 8, 16,
                2, 4, 8, 16,
                2, 4, 8, 16],
    "Time (s)": [24.538722, 5.542523, 5.933017, 4.998237,
                 12.172685, 6.388802, 6.388802, 15.276038,
                 26.806696, 6.639904, 3.358136, 5.334538,
                 3.144221, 1.309154, 0.866707, 1.020659],
    "Effective CPU Utilization (%)": [12.4, 24.4, 48.8, 94.8,
                                     12.4, 24.5, 48.2, 86.4,
                                     12.4, 24.4, 47.6, 88.4,
                                     92.4, 84.5, 79.6, 82.3]
}

# Single-thread execution times for each method
single_thread_times = {
    "Aligned": 39.742814,
    "Unrolled": 29.183964,
    "Naive": 34.529702,
    "Blocked": 5.393027
}

# Create DataFrame and calculate speedup
df = pd.DataFrame(data)
df["Speedup"] = df.apply(lambda row: single_thread_times[row["Method"]] / row["Time (s)"], axis=1)

# Define colors and thread values
colors = {"Aligned": "blue", "Unrolled": "orange", "Naive": "green", "Blocked": "red"}
thread_values = [2, 4, 8, 16]
methods = df["Method"].unique()

# Figure 1: Execution Time
plt.figure(figsize=(10, 6))
width = 0.2
x = np.arange(len(thread_values))

for i, method in enumerate(methods):
    subset = df[df["Method"] == method]
    plt.bar(x + i*width, subset["Time (s)"], width, label=method, color=colors[method])

plt.title("Execution Time Comparison", fontsize=14, pad=20)
plt.xlabel("Number of Threads", fontsize=12)
plt.ylabel("Time (seconds)", fontsize=12)
plt.xticks(x + width*1.5, thread_values)
plt.legend(title="Implementation Type")
plt.grid(True, linestyle='--', alpha=0.3, axis='y')
plt.savefig('execution_time.png', bbox_inches='tight', dpi=300)
plt.close()

# Figure 2: CPU Utilization
plt.figure(figsize=(10, 6))
for i, method in enumerate(methods):
    subset = df[df["Method"] == method]
    plt.bar(x + i*width, subset["Effective CPU Utilization (%)"], width, label=method, color=colors[method])

plt.title("CPU Utilization Comparison", fontsize=14, pad=20)
plt.xlabel("Number of Threads", fontsize=12)
plt.ylabel("CPU Utilization (%)", fontsize=12)
plt.xticks(x + width*1.5, thread_values)
plt.legend(title="Implementation Type")
plt.grid(True, linestyle='--', alpha=0.3, axis='y')
plt.savefig('cpu_utilization.png', bbox_inches='tight', dpi=300)
plt.close()

# Figure 3: Speedup (Line Plot)
plt.figure(figsize=(10, 6))
for method in methods:
    subset = df[df["Method"] == method]
    plt.plot(subset["Threads"], subset["Speedup"], 
             marker='o', label=method, color=colors[method], linewidth=2)

plt.title("Speedup Comparison", fontsize=14, pad=20)
plt.xlabel("Number of Threads", fontsize=12)
plt.ylabel("Speedup", fontsize=12)
plt.xticks(thread_values)
plt.legend(title="Implementation Type")
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('speedup.png', bbox_inches='tight', dpi=300)
plt.close()

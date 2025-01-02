import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

# Data preparation
programs = ["Aligned", "Blocked", "Naive", "Unrolled"]
threads = [1, 2, 4, 8, 16]
data = {"Program": [], "Threads": [], "L1 Miss Rate (%)": [], "LLC Miss Rate (%)": []}

# Parse log files for cache miss rates
log_files = {
    "Aligned": "../logs/cache_hit_miss_logs/Aligned_cache_misses.log",
    "Blocked": "../logs/cache_hit_miss_logs/Blocked_cache_misses.log",
    "Naive": "../logs/cache_hit_miss_logs/Naive_cache_misses.log",
    "Unrolled": "../logs/cache_hit_miss_logs/Unrolled_cache_misses.log"
}

for program, log_file in log_files.items():
    with open(log_file, 'r') as file:
        content = file.read()
        for T in threads:
            l1_miss_match = re.search(rf"{T} threads.*?L1-dcache-load-misses:u.*?([\d.]+)%", content, re.DOTALL)
            llc_miss_match = re.search(rf"{T} threads.*?LLC-load-misses:u.*?([\d.]+)%", content, re.DOTALL)

            if l1_miss_match and llc_miss_match:
                l1_miss_rate = float(l1_miss_match.group(1))
                llc_miss_rate = float(llc_miss_match.group(1))

                data["Program"].append(program)
                data["Threads"].append(T)
                data["L1 Miss Rate (%)"].append(l1_miss_rate)
                data["LLC Miss Rate (%)"].append(llc_miss_rate)

# Create a DataFrame
df = pd.DataFrame(data)

# Plotting L1 Miss Rates
fig1, ax1 = plt.subplots(figsize=(16, 10))

for idx, program in enumerate(df["Program"].unique()):
    program_data = df[df["Program"] == program]
    ax1.plot(program_data["Threads"], program_data["L1 Miss Rate (%)"], marker='o', label=f"{program} L1 Miss Rate")
    for x, y in zip(program_data["Threads"], program_data["L1 Miss Rate (%)"]):
        ax1.text(x, y + 1, f"{y:.2f}", ha='center', fontsize=8)

ax1.set_xlabel("Number of Threads", fontsize=14)
ax1.set_ylabel("L1 Miss Rate (%)", fontsize=14)
ax1.set_xticks(threads)
ax1.set_xticklabels(threads)
ax1.set_title("L1 Miss Rates vs Number of Threads", fontsize=16, weight='bold')
ax1.legend()
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Save L1 Miss Rates plot
plt.savefig("l1_miss_rates_chart.png", dpi=300)
plt.close(fig1)

# Plotting LLC Miss Rates
fig2, ax2 = plt.subplots(figsize=(16, 10))

for idx, program in enumerate(df["Program"].unique()):
    program_data = df[df["Program"] == program]
    ax2.plot(program_data["Threads"], program_data["LLC Miss Rate (%)"], marker='o', label=f"{program} LLC Miss Rate")
    for x, y in zip(program_data["Threads"], program_data["LLC Miss Rate (%)"]):
        ax2.text(x, y + 1, f"{y:.2f}", ha='center', fontsize=8)

ax2.set_xlabel("Number of Threads", fontsize=14)
ax2.set_ylabel("LLC Miss Rate (%)", fontsize=14)
ax2.set_xticks(threads)
ax2.set_xticklabels(threads)
ax2.set_title("LLC Miss Rates vs Number of Threads", fontsize=16, weight='bold')
ax2.legend()
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# Save LLC Miss Rates plot
plt.savefig("llc_miss_rates_chart.png", dpi=300)
plt.close(fig2)

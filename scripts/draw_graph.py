#!/usr/bin/env python3
# draw_all.py

import os
import re
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

##############################################################################
# Parsing Functions
##############################################################################

def parse_l1_dcache(filepath):
    """
    Parse L1-dcache-load-misses lines from 'filepath', expecting lines like:
      ./matmul_aligned_parallel_N1024_T2.log:     1,078,254,424  L1-dcache-load-misses:u  #   65.23% of all L1-dcache accesses
    Returns a DataFrame:
      columns = [Implementation, Size, Threads, L1_dcache_Perc]
    """
    rows = []
    with open(filepath, 'r') as f:
        text = f.read()
    
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        
        # Split on '#' to isolate the part with the percentage
        parts = line.split('#')
        if len(parts) < 2:
            continue
        
        percentage_part = parts[1]
        match_perc = re.search(r'([\d\.]+)%', percentage_part)
        if not match_perc:
            continue
        
        l1_percent = float(match_perc.group(1))
        
        # Extract the base filename from the left side
        left_side = parts[0].split(':')[0].strip()  # e.g., "./matmul_aligned_parallel_N1024_T2.log"
        base_filename = os.path.basename(left_side) # e.g., "matmul_aligned_parallel_N1024_T2.log"
        
        # Determine Implementation
        if "aligned" in base_filename:
            impl = "Aligned"
        elif "blocked" in base_filename:
            impl = "Blocked"
        elif "naive" in base_filename:
            impl = "Naive"
        elif "unrolled" in base_filename:
            impl = "Unrolled"
        else:
            impl = "Unknown"
        
        # Parse out matrix size
        match_size = re.search(r"_N(\d+)", base_filename)
        size_val = int(match_size.group(1)) if match_size else None
        
        # Parse out threads
        match_thr = re.search(r"_T(\d+)", base_filename)
        thr_val = int(match_thr.group(1)) if match_thr else 1
        
        rows.append({
            "Implementation": impl,
            "Size": size_val,
            "Threads": thr_val,
            "L1_dcache_Perc": l1_percent
        })
    
    return pd.DataFrame(rows)


def parse_llc_misses(filepath):
    """
    Parse LLC-load-misses lines from 'filepath', expecting lines like:
      ./matmul_aligned_parallel_N1024_T2.log:  367,649 LLC-load-misses:u  #  0.04% of all LL-cache accesses
    Returns a DataFrame:
      columns = [Implementation, Size, Threads, LLC_miss_Perc]
    """
    rows = []
    with open(filepath, 'r') as f:
        text = f.read()
    
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        
        parts = line.split('#')
        if len(parts) < 2:
            continue
        
        percentage_part = parts[1]
        match_perc = re.search(r'([\d\.]+)%', percentage_part)
        if not match_perc:
            continue
        
        llc_percent = float(match_perc.group(1))
        
        left_side = parts[0].split(':')[0].strip()
        base_filename = os.path.basename(left_side)
        
        if "aligned" in base_filename:
            impl = "Aligned"
        elif "blocked" in base_filename:
            impl = "Blocked"
        elif "naive" in base_filename:
            impl = "Naive"
        elif "unrolled" in base_filename:
            impl = "Unrolled"
        else:
            impl = "Unknown"
        
        match_size = re.search(r"_N(\d+)", base_filename)
        size_val = int(match_size.group(1)) if match_size else None
        
        match_thr = re.search(r"_T(\d+)", base_filename)
        thr_val = int(match_thr.group(1)) if match_thr else 1
        
        rows.append({
            "Implementation": impl,
            "Size": size_val,
            "Threads": thr_val,
            "LLC_miss_Perc": llc_percent
        })
    
    return pd.DataFrame(rows)


def parse_cpu_util(filepath):
    """
    Parse CPU utilization lines from 'filepath', expecting lines like:
      ./matmul_aligned_parallel_N1024_T2_threading.log:Effective CPU Utilization: 12.0% (1.917 out of 16 logical CPUs)
    Returns a DataFrame:
      columns = [Implementation, Size, Threads, CPU_Utilization]
    """
    rows = []
    with open(filepath, 'r') as f:
        text = f.read()
    
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        
        if "Effective CPU Utilization:" not in line:
            continue
        
        left_right = line.split("Effective CPU Utilization:")
        if len(left_right) < 2:
            continue
        
        left_side = left_right[0].split(':')[0].strip()
        cpu_part = left_right[1].strip()
        
        match_cpu = re.search(r'([\d\.]+)%', cpu_part)
        if not match_cpu:
            continue
        
        cpu_percent = float(match_cpu.group(1))
        
        base_filename = os.path.basename(left_side)
        
        if "aligned" in base_filename:
            impl = "Aligned"
        elif "blocked" in base_filename:
            impl = "Blocked"
        elif "naive" in base_filename:
            impl = "Naive"
        elif "unrolled" in base_filename:
            impl = "Unrolled"
        else:
            impl = "Unknown"
        
        match_size = re.search(r"_N(\d+)", base_filename)
        size_val = int(match_size.group(1)) if match_size else None
        
        match_thr = re.search(r"_T(\d+)", base_filename)
        thr_val = int(match_thr.group(1)) if match_thr else 1
        
        rows.append({
            "Implementation": impl,
            "Size": size_val,
            "Threads": thr_val,
            "CPU_Utilization": cpu_percent
        })
    
    return pd.DataFrame(rows)


def parse_execution_time(filepath):
    """
    Parse execution time lines from 'filepath', expecting lines like:
      [Aligned] N=1024, threads=2, time=0.679279 sec
      [Blocked] N=1024, threads=8, block_size=64, time=0.125786 sec
    Returns a DataFrame:
      columns = [Implementation, Size, Threads, Time]
    """
    rows = []
    with open(filepath, 'r') as f:
        text = f.read()
    
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        
        # Implementation in square brackets [Aligned], [Blocked], [Naive], [Unrolled]
        if '[' not in line or ']' not in line:
            continue
        
        impl = line.split('[', 1)[1].split(']', 1)[0].strip()
        remainder = line.split(']', 1)[1].strip()
        
        parts = [p.strip() for p in remainder.split(',')]
        
        size_val = None
        thr_val = 1
        time_val = None
        
        for p in parts:
            # e.g. "N=1024", "threads=2", "time=0.679279 sec"
            if p.startswith("N="):
                try:
                    size_val = int(p.split('=', 1)[1])
                except ValueError:
                    pass
            elif p.startswith("threads="):
                try:
                    thr_val = int(p.split('=', 1)[1])
                except ValueError:
                    pass
            elif p.startswith("time="):
                time_str = p.split('=', 1)[1].replace('sec', '').strip()
                try:
                    time_val = float(time_str)
                except ValueError:
                    pass
        
        if (size_val is not None) and (time_val is not None):
            rows.append({
                "Implementation": impl,
                "Size": size_val,
                "Threads": thr_val,
                "Time": time_val
            })
    
    return pd.DataFrame(rows)

##############################################################################
# Plotting Functions (separate figures per matrix size, higher DPI)
##############################################################################

def plot_l1_percentage_separate(df_l1, graph_dir, dpi=300):
    """
    For each matrix size in df_l1, create a separate PNG:
      x=Threads, y=L1_dcache_Perc, grouped by Implementation.
    """
    if df_l1.empty:
        print("No L1-dcache data to plot.")
        return
    
    sns.set_theme(style="whitegrid")
    unique_sizes = sorted(df_l1["Size"].dropna().unique())
    
    for size_val in unique_sizes:
        subset = df_l1[df_l1["Size"] == size_val]
        if subset.empty:
            continue
        
        plt.figure(figsize=(6, 4))
        sns.lineplot(
            data=subset, x="Threads", y="L1_dcache_Perc",
            hue="Implementation", marker="o"
        )
        plt.title(f"L1-dcache Miss % (N={size_val})")
        plt.ylabel("L1-dcache Misses (%)")
        plt.xlabel("Threads")
        plt.ylim(0, None)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc="best")
        
        outfile = os.path.join(graph_dir, f"l1_dcache_percentage_N{size_val}.png")
        plt.savefig(outfile, dpi=dpi, bbox_inches="tight")
        plt.close()
        print(f"Saved: {outfile}")


def plot_llc_percentage_separate(df_llc, graph_dir, dpi=300):
    """
    For each matrix size in df_llc, create a separate PNG:
      x=Threads, y=LLC_miss_Perc, grouped by Implementation.
    """
    if df_llc.empty:
        print("No LLC data to plot.")
        return
    
    sns.set_theme(style="whitegrid")
    unique_sizes = sorted(df_llc["Size"].dropna().unique())
    
    for size_val in unique_sizes:
        subset = df_llc[df_llc["Size"] == size_val]
        if subset.empty:
            continue
        
        plt.figure(figsize=(6, 4))
        sns.lineplot(
            data=subset, x="Threads", y="LLC_miss_Perc",
            hue="Implementation", marker="o"
        )
        plt.title(f"LLC-load Miss % (N={size_val})")
        plt.ylabel("LLC-load Misses (%)")
        plt.xlabel("Threads")
        plt.ylim(0, None)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc="best")
        
        outfile = os.path.join(graph_dir, f"llc_miss_percentage_N{size_val}.png")
        plt.savefig(outfile, dpi=dpi, bbox_inches="tight")
        plt.close()
        print(f"Saved: {outfile}")


def plot_cpu_util_separate(df_cpu, graph_dir, dpi=300):
    """
    For each matrix size in df_cpu, create a separate PNG:
      x=Threads, y=CPU_Utilization, grouped by Implementation.
    """
    if df_cpu.empty:
        print("No CPU Util data to plot.")
        return
    
    sns.set_theme(style="whitegrid")
    unique_sizes = sorted(df_cpu["Size"].dropna().unique())
    
    for size_val in unique_sizes:
        subset = df_cpu[df_cpu["Size"] == size_val]
        if subset.empty:
            continue
        
        plt.figure(figsize=(6, 4))
        sns.lineplot(
            data=subset, x="Threads", y="CPU_Utilization",
            hue="Implementation", marker="o"
        )
        plt.title(f"CPU Utilization (N={size_val})")
        plt.ylabel("CPU Utilization (%)")
        plt.xlabel("Threads")
        plt.ylim(0, 100)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc="best")
        
        outfile = os.path.join(graph_dir, f"cpu_utilization_N{size_val}.png")
        plt.savefig(outfile, dpi=dpi, bbox_inches="tight")
        plt.close()
        print(f"Saved: {outfile}")


def plot_execution_time_separate(df_time, graph_dir, dpi=300):
    """
    For each matrix size in df_time, create two PNGs:
      1) Execution Time vs. Threads (Time on y-axis)
      2) Speedup vs. Threads (T1/Tn) if single-thread data is present
    """
    if df_time.empty:
        print("No execution time data to plot.")
        return
    
    sns.set_theme(style="whitegrid")
    unique_sizes = sorted(df_time["Size"].dropna().unique())
    
    for size_val in unique_sizes:
        subset = df_time[df_time["Size"] == size_val]
        if subset.empty:
            continue
        
        # 1) Execution Time
        plt.figure(figsize=(6, 4))
        sns.lineplot(
            data=subset, x="Threads", y="Time",
            hue="Implementation", marker="o"
        )
        plt.title(f"Execution Time vs. Threads (N={size_val})")
        plt.ylabel("Time (sec)")
        plt.xlabel("Threads")
        plt.yscale("log")  # optional: log scale
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc="best")
        
        outfile_time = os.path.join(graph_dir, f"exec_time_N{size_val}.png")
        plt.savefig(outfile_time, dpi=dpi, bbox_inches="tight")
        plt.close()
        print(f"Saved: {outfile_time}")
        
        # 2) Speedup = T1 / Tn
        speedup_data = []
        for impl in subset["Implementation"].unique():
            df_impl = subset[subset["Implementation"] == impl]
            df_seq = df_impl[df_impl["Threads"] == 1]
            if df_seq.empty:
                continue  # no single-thread data for this Implementation
            seq_time = df_seq["Time"].values[0]
            
            for _, row in df_impl.iterrows():
                t = row["Time"]
                speedup = seq_time / t if t != 0 else None
                speedup_data.append({
                    "Implementation": impl,
                    "Threads": row["Threads"],
                    "Speedup": speedup
                })
        
        if speedup_data:
            df_speedup = pd.DataFrame(speedup_data)
            plt.figure(figsize=(6, 4))
            sns.lineplot(
                data=df_speedup, x="Threads", y="Speedup",
                hue="Implementation", marker="o"
            )
            plt.title(f"Speedup vs. Threads (N={size_val})")
            plt.ylabel("Speedup (T1/Tn)")
            plt.xlabel("Threads")
            plt.ylim(0, None)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend(loc="best")
            
            outfile_speedup = os.path.join(graph_dir, f"speedup_N{size_val}.png")
            plt.savefig(outfile_speedup, dpi=dpi, bbox_inches="tight")
            plt.close()
            print(f"Saved: {outfile_speedup}")


##############################################################################
# Main Entry Point (with parametric directories using argparse)
##############################################################################

def main():
    # ------------------------------------------------------------------
    # 1) Parse command-line arguments
    # ------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Draw graphs for L1-dcache, LLC-load misses, CPU utilization, and execution time."
    )
    parser.add_argument(
        "--base_dir",
        default="/home/yigit/Documents/CS535_Multicore_Programming_Fall2024-25/multicore_project",
        help="Base directory of the project (default: %(default)s)"
    )
    parser.add_argument(
        "--log_subdir",
        default="logs/final_results",
        help="Subdirectory under base_dir for log files (default: %(default)s)"
    )
    parser.add_argument(
        "--graph_subdir",
        default="graphs",
        help="Subdirectory under base_dir to store output plots (default: %(default)s)"
    )
    parser.add_argument(
        "--l1_file",
        default="L1-dcache-load-misses.txt",
        help="Name of the L1-dcache load misses file (default: %(default)s)"
    )
    parser.add_argument(
        "--llc_file",
        default="LLC-load-misses.txt",
        help="Name of the LLC-load misses file (default: %(default)s)"
    )
    parser.add_argument(
        "--cpu_file",
        default="cpu-utilization.txt",
        help="Name of the CPU utilization file (default: %(default)s)"
    )
    parser.add_argument(
        "--time_file",
        default="execution-time.txt",
        help="Name of the execution time file (default: %(default)s)"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="DPI (resolution) for saved plots (default: %(default)s)"
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # 2) Construct the relevant paths
    # ------------------------------------------------------------------
    BASE_DIR = os.path.abspath(args.base_dir)
    LOG_DIR = os.path.join(BASE_DIR, args.log_subdir)
    GRAPH_DIR = os.path.join(BASE_DIR, args.graph_subdir)

    # Create the graphs directory if it doesn't exist
    os.makedirs(GRAPH_DIR, exist_ok=True)

    # Filenames
    l1_path = os.path.join(LOG_DIR, args.l1_file)
    llc_path = os.path.join(LOG_DIR, args.llc_file)
    cpu_path = os.path.join(LOG_DIR, args.cpu_file)
    time_path = os.path.join(LOG_DIR, args.time_file)

    # ------------------------------------------------------------------
    # 3) Parse the files into DataFrames
    # ------------------------------------------------------------------
    if os.path.exists(l1_path):
        df_l1 = parse_l1_dcache(l1_path)
    else:
        print(f"[WARNING] L1-dcache file not found: {l1_path}")
        df_l1 = pd.DataFrame()

    if os.path.exists(llc_path):
        df_llc = parse_llc_misses(llc_path)
    else:
        print(f"[WARNING] LLC file not found: {llc_path}")
        df_llc = pd.DataFrame()

    if os.path.exists(cpu_path):
        df_cpu = parse_cpu_util(cpu_path)
    else:
        print(f"[WARNING] CPU utilization file not found: {cpu_path}")
        df_cpu = pd.DataFrame()

    if os.path.exists(time_path):
        df_time = parse_execution_time(time_path)
    else:
        print(f"[WARNING] Execution time file not found: {time_path}")
        df_time = pd.DataFrame()

    # ------------------------------------------------------------------
    # 4) Plot & save each type of data
    # ------------------------------------------------------------------
    plot_l1_percentage_separate(df_l1, GRAPH_DIR, dpi=args.dpi)
    plot_llc_percentage_separate(df_llc, GRAPH_DIR, dpi=args.dpi)
    plot_cpu_util_separate(df_cpu, GRAPH_DIR, dpi=args.dpi)
    plot_execution_time_separate(df_time, GRAPH_DIR, dpi=args.dpi)

    print("All plots saved in:", GRAPH_DIR)


if __name__ == "__main__":
    main()

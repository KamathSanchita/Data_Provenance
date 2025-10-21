import os
import gzip

def count_reads_in_fastq(file_path):
    """
    Counts the number of reads in a FASTQ or FASTQ.GZ file.
    Each read consists of 4 lines.
    """
    open_func = gzip.open if file_path.endswith(".gz") else open
    line_count = 0

    with open_func(file_path, "rt") as f:
        for _ in f:
            line_count += 1
    return line_count // 4


def count_reads_in_folder(base_dir):
    """
    Traverse through subfolders of 'base_dir', find merged FASTQ files,
    and count the number of reads in each.
    """
    print(f"\n[INFO] Scanning for merged FASTQ files in {base_dir}\n")
    results = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.startswith("merged_") and file.endswith(".fastq") or file.endswith(".fastq.gz"):
                full_path = os.path.join(root, file)
                read_count = count_reads_in_fastq(full_path)
                results.append((full_path, read_count))
                print(f"{file:<25} → {read_count} reads")

    # Print summary
    print("\n" + "-" * 60)
    print(f"{'File':<40} | {'Reads':>10}")
    print("-" * 60)
    for file, count in results:
        print(f"{os.path.basename(file):<40} | {count:>10}")
    print("-" * 60)

    # Optionally save to a summary file
    summary_file = os.path.join(base_dir, "read_count_summary.tsv")
    with open(summary_file, "w") as out:
        out.write("File\tReads\n")
        for file, count in results:
            out.write(f"{os.path.basename(file)}\t{count}\n")
    print(f"\n✅ Summary saved to: {summary_file}\n")


# --------------------------
# Example usage:
# --------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Count reads from merged FASTQ files in subfolders.")
    parser.add_argument("-i", "--input_dir", required=True, help="Base directory containing sample folders.")
    args = parser.parse_args()

    count_reads_in_folder(args.input_dir)

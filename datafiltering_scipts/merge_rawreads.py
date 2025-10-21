import os
import shutil

def organize_fastq_files(input_dir, n_chars):
    """
    Organize FASTQ files into folders based on the first n characters of the filename.
    Then merge forward (_1.fastq) and reverse (_2.fastq) reads within each folder.
    
    Parameters:
        input_dir (str): Directory containing the FASTQ files.
        n_chars (int): Number of initial characters to consider for sample naming.
    """
    input_dir = os.path.abspath(input_dir)
    print(f"\n[INFO] Scanning directory: {input_dir}")

    # Step 1: Group files by sample prefix
    fastq_files = [f for f in os.listdir(input_dir) if f.endswith(".fastq")]
    if not fastq_files:
        print("[WARNING] No FASTQ files found in the directory.")
        return

    for file in fastq_files:
        sample_prefix = file[:n_chars]
        sample_dir = os.path.join(input_dir, sample_prefix)
        os.makedirs(sample_dir, exist_ok=True)

        # Move the file into its sample folder
        src = os.path.join(input_dir, file)
        dst = os.path.join(sample_dir, file)
        shutil.move(src, dst)
        print(f"[INFO] Moved {file} → {sample_dir}")

    print("\n[INFO] Files organized. Proceeding to merging step...")

    # Step 2: Merge forward (_1.fastq) and reverse (_2.fastq) reads
    for folder in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        forward_reads = sorted([f for f in os.listdir(folder_path) if f.endswith("_1.fastq")])
        reverse_reads = sorted([f for f in os.listdir(folder_path) if f.endswith("_2.fastq")])

        merged_fwd = os.path.join(folder_path, "merged_1.fastq")
        merged_rev = os.path.join(folder_path, "merged_2.fastq")

        # Merge forward reads
        if forward_reads:
            with open(merged_fwd, "wb") as outfile:
                for f in forward_reads:
                    with open(os.path.join(folder_path, f), "rb") as infile:
                        shutil.copyfileobj(infile, outfile)
            print(f"[INFO] Merged {len(forward_reads)} forward files → {merged_fwd}")

        # Merge reverse reads
        if reverse_reads:
            with open(merged_rev, "wb") as outfile:
                for f in reverse_reads:
                    with open(os.path.join(folder_path, f), "rb") as infile:
                        shutil.copyfileobj(infile, outfile)
            print(f"[INFO] Merged {len(reverse_reads)} reverse files → {merged_rev}")

    print("\n✅ All FASTQ files organized and merged successfully.")


# --------------------------
# Example usage:
# --------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Organize and merge FASTQ files by sample name.")
    parser.add_argument("-i", "--input_dir", required=True, help="Directory containing FASTQ files.")
    parser.add_argument("-n", "--n_chars", type=int, required=True, help="Number of characters for sample name prefix.")
    
    args = parser.parse_args()
    organize_fastq_files(args.input_dir, args.n_chars)

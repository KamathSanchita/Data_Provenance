import os
import hashlib
import pandas as pd
import fitz  # PyMuPDF
import re

def extract_table_from_pdf(pdf_path):
    """
    Extract text-based table (Sequence name and MD5 hash) from a PDF file.
    Returns a pandas DataFrame with columns: ['Sequence', 'Expected_MD5'].
    """
    doc = fitz.open(pdf_path)
    data = []

    for page in doc:
        text = page.get_text("text")
        lines = text.strip().split("\n")

        for line in lines:
            # Match two columns: name + MD5 hash
            match = re.match(r"(\S+)\s+([a-fA-F0-9]{32})", line)
            if match:
                seq_name, md5 = match.groups()
                data.append((seq_name, md5.lower()))

    df = pd.DataFrame(data, columns=["Sequence", "Expected_MD5"])
    print(f"[INFO] Extracted {len(df)} entries from {pdf_path}")
    return df


def compute_md5(file_path, chunk_size=8192):
    """
    Compute MD5 hash for a given file efficiently (streamed).
    """
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            md5.update(chunk)
    return md5.hexdigest()


def verify_fastq_md5(pdf_path, fastq_dir, output_file="md5_check_results.tsv"):
    """
    Compare expected MD5s from PDF with actual MD5s from FASTQ files.
    """
    df_pdf = extract_table_from_pdf(pdf_path)
    results = []

    for _, row in df_pdf.iterrows():
        seq_name = row["Sequence"]
        expected_md5 = row["Expected_MD5"]

        # Try to find the matching FASTQ file
        possible_files = [f for f in os.listdir(fastq_dir) if f.startswith(seq_name)]
        if not possible_files:
            results.append((seq_name, expected_md5, "MISSING_FILE", ""))
            print(f"[WARN] No FASTQ found for {seq_name}")
            continue

        # Compute MD5 of first matching file (assuming unique)
        fastq_path = os.path.join(fastq_dir, possible_files[0])
        computed_md5 = compute_md5(fastq_path)

        status = "MATCH" if computed_md5 == expected_md5 else "MISMATCH"
        results.append((seq_name, expected_md5, computed_md5, status))

        if status == "MISMATCH":
            print(f"[❌] {seq_name} → Hash mismatch!")
        else:
            print(f"[✅] {seq_name} → OK")

    # Save results
    df_out = pd.DataFrame(results, columns=["Sequence", "Expected_MD5", "Computed_MD5", "Status"])
    df_out.to_csv(output_file, sep="\t", index=False)
    print(f"\n✅ Comparison complete. Results saved to: {output_file}")

    # Return mismatched entries
    mismatches = df_out[df_out["Status"] == "MISMATCH"]["Sequence"].tolist()
    if mismatches:
        print("\n⚠️ Sequences with MD5 mismatches:")
        for seq in mismatches:
            print(f" - {seq}")
    else:
        print("\n🎉 All MD5 checks matched successfully!")


# --------------------------
# Example usage
# --------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Verify FASTQ MD5 hashes from PDF reference list.")
    parser.add_argument("-p", "--pdf", required=True, help="Path to the PDF file containing sequence names and MD5 hashes.")
    parser.add_argument("-i", "--input", required=True, help="Folder containing FASTQ files.")
    parser.add_argument("-o", "--output", default="md5_check_results.tsv", help="Output TSV file.")
    args = parser.parse_args()

    verify_fastq_md5(args.pdf, args.input, args.output)

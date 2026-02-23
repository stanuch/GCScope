import csv
import json
from pathlib import Path

def export_results(
    seq_name: str,
    seq_length: int,
    gc_percent: float,
    nuc_content: dict,
    gc_list: list,
    cpg_list: list,
    gpc_list: list,
    window_size: int,
    step_size: int,
    output_dir: Path = None,
    export_format: str = "csv",
) -> str:
    export_format = export_format.strip().lower()
    if export_format not in ("csv", "tsv", "json"):
        raise ValueError(f"Unsupported format: {export_format}. Use csv, tsv, or json.")

    if output_dir is None:
        output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{seq_name}_export.{export_format}"
    filepath = output_dir / filename

    if export_format == "json":
        _write_json(filepath, seq_name, seq_length, gc_percent, nuc_content,
                     gc_list, cpg_list, gpc_list, window_size, step_size)
    else:
        delimiter = "," if export_format == "csv" else "\t"
        _write_delimited(filepath, delimiter, seq_name, seq_length, gc_percent,
                         nuc_content, gc_list, cpg_list, gpc_list, window_size, step_size)

    return str(filepath.resolve())

def _write_delimited(
    filepath: Path,
    delimiter: str,
    seq_name: str,
    seq_length: int,
    gc_percent: float,
    nuc_content: dict,
    gc_list: list,
    cpg_list: list,
    gpc_list: list,
    window_size: int,
    step_size: int,
) -> None:
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=delimiter)

        f.write("# Summary\n")
        writer.writerow(["Sequence", "Total Nucleotides", "GC Content (%)"])
        writer.writerow([seq_name, seq_length, f"{gc_percent:.2f}"])
        f.write("\n")

        f.write("# Nucleotide Composition\n")
        writer.writerow(["Nucleotide", "Percentage (%)"])
        for nuc, pct in nuc_content.items():
            writer.writerow([nuc, f"{pct:.2f}"])
        f.write("\n")

        f.write(f"# Sliding Window GC Content (window={window_size}, step={step_size})\n")
        writer.writerow(["Window Start", "Window End", "GC Content (%)"])
        for entry in gc_list:
            writer.writerow([entry[0][0], entry[0][1], f"{entry[1]:.2f}"])
        f.write("\n")

        f.write("# CpG Islands (window=100, step=2)\n")
        writer.writerow(["Window Start", "Window End", "Count per 100 nt"])
        for entry in cpg_list:
            writer.writerow([entry[0][0], entry[0][1], entry[1]])
        f.write("\n")

        f.write("# GpC Islands (window=100, step=2)\n")
        writer.writerow(["Window Start", "Window End", "Count per 100 nt"])
        for entry in gpc_list:
            writer.writerow([entry[0][0], entry[0][1], entry[1]])

def _write_json(
    filepath: Path,
    seq_name: str,
    seq_length: int,
    gc_percent: float,
    nuc_content: dict,
    gc_list: list,
    cpg_list: list,
    gpc_list: list,
    window_size: int,
    step_size: int,
) -> None:
    data = {
        "summary": {
            "sequence": seq_name,
            "total_nucleotides": seq_length,
            "gc_content_percent": round(gc_percent, 2),
        },
        "nucleotide_composition": {
            nuc: round(pct, 2) for nuc, pct in nuc_content.items()
        },
        "sliding_window_gc": {
            "window_size": window_size,
            "step_size": step_size,
            "data": [
                {
                    "window_start": entry[0][0],
                    "window_end": entry[0][1],
                    "gc_content_percent": round(entry[1], 2),
                }
                for entry in gc_list
            ],
        },
        "cpg_islands": {
            "window_size": 100,
            "step_size": 2,
            "data": [
                {
                    "window_start": entry[0][0],
                    "window_end": entry[0][1],
                    "count_per_100nt": entry[1],
                }
                for entry in cpg_list
            ],
        },
        "gpc_islands": {
            "window_size": 100,
            "step_size": 2,
            "data": [
                {
                    "window_start": entry[0][0],
                    "window_end": entry[0][1],
                    "count_per_100nt": entry[1],
                }
                for entry in gpc_list
            ],
        },
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

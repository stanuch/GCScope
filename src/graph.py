import matplotlib.pyplot as plt
from pathlib import Path

def create_x_values(gc_list: list) -> list:
    x = []
    for elem in gc_list:
        x.append(elem[0][0])
    return x

def create_y_values(gc_list: list) -> list:
    y = []
    for elem in gc_list:
        y.append(elem[1])
    return y

def gc_content_graph(x: list, y: list, filename: str, output_dir: Path = None) -> tuple:
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 5)

    norm = plt.Normalize(vmin=0, vmax=100)
    colors = plt.cm.inferno(norm(y))

    for i in range(len(x) - 1):
        ax.fill_between(x[i:i+2], 0, y[i:i+2], color=colors[i])

    ax.set_xlabel("Nucleotide Position", fontweight="bold")
    ax.set_ylabel("GC Content (%)", fontweight="bold")
    ax.set_title(f"GC Content Across Sequence: {filename}", fontweight="bold")
    ax.set(xlim=(min(x), max(x)), ylim=(0, 100))

    sm = plt.cm.ScalarMappable(cmap="inferno", norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label="GC Content (%)")
    ax.grid(alpha=0.4)

    if output_dir is None:
        output_dir = Path("../output")
    output_dir.mkdir(parents=True, exist_ok=True)
    save_path = output_dir / f"gc_content_percent_{filename}.png"
    fig.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()
    return fig, ax

def cpg_islands_graph(cpg_counts: list, gpc_counts: list, filename: str, output_dir: Path = None) -> tuple:
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 5)

    x_cpg = [elem[0][0] for elem in cpg_counts]
    y_cpg = [elem[1] for elem in cpg_counts]

    x_gpc = [elem[0][0] for elem in gpc_counts]
    y_gpc = [elem[1] for elem in gpc_counts]

    ax.plot(x_cpg, y_cpg, color="darkblue", label="CpG")
    ax.plot(x_gpc, y_gpc, color="orange", label="GpC")

    ax.set_xlabel("Nucleotide Position", fontweight="bold")
    ax.set_ylabel("Count per 100 nt", fontweight="bold")
    ax.set_title(f"CpG and GpC Counts Across Sequence: {filename}", fontweight="bold")

    max_y = max(max(y_cpg), max(y_gpc))
    ax.set(xlim=(min(x_cpg), max(x_cpg)), ylim=(0, max_y + 3))
    ax.legend(loc="upper right", fontsize=11, framealpha=0.9)
    ax.grid(alpha=0.4)

    if output_dir is None:
        output_dir = Path("../output")
    output_dir.mkdir(parents=True, exist_ok=True)
    save_path = output_dir / f"cpg_islands_graph_{filename}.png"
    fig.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()
    return fig, ax
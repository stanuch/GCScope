import os
from Bio import SeqIO
from colorama import Fore, Back, Style, init
from analysis import gc_content, nucleotide_content, sliding_gc_content, cpg_islands, gpc_islands
from graph import create_x_values, create_y_values, gc_content_graph, cpg_islands_graph
from analysis import gc_content, nucleotide_content, sliding_gc_content, cpg_islands, gpc_islands

def get_file_path(base_dir: str, filename: str) -> str:
    seq_dir = os.path.join(base_dir, "..", "sequences")
    return os.path.join(seq_dir, f"{filename}.fasta")

def cls() -> None:
    os.system("cls" if os.name=="nt" else "clear")
    
def print_header():
    print("\n" + "="*60)
    print(f"{Fore.CYAN}{Style.BRIGHT}{'GC CONTENT ANALYZER':^60}{Style.RESET_ALL}")
    print("="*60 + "\n")

def print_section(title):
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}▶ {title}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'─'*50}{Style.RESET_ALL}")

def print_result(label, value, unit=""):
    print(f"{Fore.WHITE}  {label}: {Fore.GREEN}{Style.BRIGHT}{value}{unit}{Style.RESET_ALL}")

def print_error(message):
    print(f"\n{Fore.RED}{Style.BRIGHT}✗ Error: {message}{Style.RESET_ALL}\n")

def print_success(message):
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ {message}{Style.RESET_ALL}")

def get_styled_input(prompt, default=None):
    if default:
        full_prompt = f"{Fore.CYAN}➤ {prompt} [{Fore.YELLOW}default: {default}{Fore.CYAN}]: {Style.RESET_ALL}"
    else:
        full_prompt = f"{Fore.CYAN}➤ {prompt}: {Style.RESET_ALL}"
    return input(full_prompt)

def print_nucleotide_bar(label, percentage, color):
    bar_length = 30
    filled = int((percentage / 100) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"  {label}: {color}{bar}{Style.RESET_ALL} {Fore.WHITE}{percentage:.2f}%{Style.RESET_ALL}")

def main() -> None:
    cls()
    print_header()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print_section("FILE SELECTION")
    seq_filename = get_styled_input("Enter the name of your sequence file (without extension)")

    seq_path = get_file_path(base_dir, seq_filename)
    if not os.path.exists(seq_path):
        print_error(f"File {seq_path} does not exist.")
        return
    
    print_success(f"File loaded: {seq_filename}")
    
    print_section("SEQUENCE STATISTICS")
    seq_length = len(next(SeqIO.parse(seq_path, "fasta")).seq)
    gc_percent = gc_content(seq_path)
    
    print_result("Total Nucleotides", f"{seq_length:,}")
    print_result("GC Content", f"{gc_percent:.2f}", "%")
    
    print_section("NUCLEOTIDE COMPOSITION")
    nuc_content = nucleotide_content(seq_path)
    
    colors = {
        "A": Fore.GREEN,
        "T": Fore.RED,
        "U": Fore.RED,
        "C": Fore.BLUE,
        "G": Fore.YELLOW
    }
    
    for nucleotide in ["A", "T", "U", "C", "G"]:
        if nucleotide in nuc_content:
            print_nucleotide_bar(nucleotide, nuc_content[nucleotide], colors[nucleotide])

    print_section("SLIDING WINDOW ANALYSIS")
    window_size_input = get_styled_input("Enter window size", "26")
    window_size = int(window_size_input) if window_size_input else 26
    
    if window_size < 1:
        print_error("Window size must be a positive integer.")
        return
    
    step_size_input = get_styled_input("Enter step size", "2")
    step_size = int(step_size_input) if step_size_input else 2
    
    if step_size < 1:
        print_error("Step size must be a positive integer.")
        return
    
    print_result("Window Size", window_size)
    print_result("Step Size", step_size)
    
    print(f"\n{Fore.CYAN}  Generating GC content graph...{Style.RESET_ALL}")
    gc_list = sliding_gc_content(seq_path, window_size, step_size)
    x, y = create_x_values(gc_list), create_y_values(gc_list)
    gc_content_graph(x, y, seq_filename)

    print_section("CPG ISLANDS ANALYSIS")
    print(f"{Fore.CYAN}  Analyzing CpG and GpC islands...{Style.RESET_ALL}")
    cpgs = cpg_islands(seq_path)
    gpcs = gpc_islands(seq_path)
    cpg_islands_graph(cpgs, gpcs, seq_filename)
    
    print("\n" + "="*60)
    print(f"{Fore.GREEN}{Style.BRIGHT}{'ANALYSIS COMPLETE':^60}{Style.RESET_ALL}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
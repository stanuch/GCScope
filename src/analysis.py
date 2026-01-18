from Bio import SeqIO

def gc_content(seq_path: str) -> float:
    for record in SeqIO.parse(seq_path, "fasta"):
        counter = 0
        for nucleotide in record.seq:
            if nucleotide in ["C", "G", "c", "g"]:
                counter += 1
        gc_percent = (counter / len(record.seq)) * 100
        return gc_percent
    return 0.0
    
def nucleotide_content(seq_path: str) -> dict:
    for record in SeqIO.parse(seq_path, "fasta"):
        a_count = record.seq.count("A") + record.seq.count("a")
        t_count = record.seq.count("T") + record.seq.count("t")
        u_count = record.seq.count("U") + record.seq.count("u")
        c_count = record.seq.count("C") + record.seq.count("c")
        g_count = record.seq.count("G") + record.seq.count("g")
        total = len(record.seq)
        if "U" in str(record.seq) and "T" not in str(record.seq): # RNA
            return {
                "A": (a_count / total) * 100,
                "U": (u_count / total) * 100,
                "C": (c_count / total) * 100,
                "G": (g_count / total) * 100
            }
        else:  # DNA
            return {
                "A": (a_count / total) * 100,
                "T": (t_count / total) * 100,
                "C": (c_count / total) * 100,
                "G": (g_count / total) * 100
            }
    return {}
        
def sliding_gc_content(seq_path: str, window_size: int, step_size: int) -> list:
    for record in SeqIO.parse(seq_path, "fasta"):
        sequence = str(record.seq)
        gc_content = []
        for i in range(0, len(sequence), step_size):
            current_window_size = min(window_size, len(sequence) - i)
            window = sequence[i:i + current_window_size]
            gc_percent = (window.count("G") + window.count("C") + window.count ("g") + window.count("c")) / window_size * 100
            temp_list_elem = [[i+1,i + window_size], gc_percent]
            gc_content.append(temp_list_elem)
        return gc_content
    return []

def cpg_islands(seq_path: str, step_size: int = 2, window_size: int = 100) -> list:
    for record in SeqIO.parse(seq_path, "fasta"):
        sequence = str(record.seq)
        cpg = []
        for i in range(0, len(sequence), step_size):
            current_window_size = min(window_size, len(sequence) - i)
            window = sequence[i:i + current_window_size]
            cpg_count_per_100 = ((window.count("CG") + window.count("cg")) / window_size * 100)
            temp_list_elem = [[i+1,i + window_size], int(cpg_count_per_100)]
            cpg.append(temp_list_elem)
        return cpg
    return []
    
def gpc_islands(seq_path: str, step_size: int = 2, window_size: int = 100) -> list:
    for record in SeqIO.parse(seq_path, "fasta"):
        sequence = str(record.seq)
        gpc = []
        for i in range(0, len(sequence), step_size):
            current_window_size = min(window_size, len(sequence) - i)
            window = sequence[i:i + current_window_size]   
            gpc_count_per_100 = ((window.count("GC") + window.count("gc")) / current_window_size * 100)
            temp_list_elem = [[i+1, i + current_window_size], int(gpc_count_per_100)]
            gpc.append(temp_list_elem)
        return gpc
    return []
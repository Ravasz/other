import re

prot_seq_mod = "PVIS*HAQRDQHT*FVERMPKPRGQPFT*QYLLHDLQIQKVMISGGKKPMNECCWWRQPVNFDFSADKQAIYCVDIAKIDMQQDKWMHRQSISGTSLKMAAWNLGYHKISAFRVMHNKCPMANWMMIYMTLPRPTKQWSRAA^FRKYTSIIRS*GGATSR^S*DADLRFVKRQDLEYFQYCMFYQAILDTLLPIRYCNTNTCRKCEKMPKFTY*QREGCRPDNIHASKYEFIGRQIPS*AAAI" # add sequence here

def trypsin_digest(seq_in):
    """
    Performs an in-silico trypsin digest on a protein sequence.

    Args:
        seq_in (str): The input protein sequence.

    Returns:
        list: A list of the digested peptides.
    """
    peptides = []
    current_peptide_start = 0
    seq_length = len(seq_in)
    side_flag = False
    
    # Iterate through the protein sequence by index
    for i in range(seq_length):
        current_aa = seq_in[i]
        
        # Skip 'stop codon' placeholder '*'
        if current_aa == "*":
            continue

        if current_aa == "^":
            if side_flag: side_flag = False
            else: side_flag = True
        
        if side_flag: continue

        # Check for cleavage sites: Lysine (K) or Arginine (R)
        if current_aa in ["K", "R"]:
            # Check if it's not the last amino acid
            if i < seq_length - 1:
                next_aa = seq_in[i + 1]

                # Trypsin does not cleave if K or R is followed by Proline (P)
                if next_aa != "P":
                    # Extract the peptide and remove '*'
                    peptide = seq_in[current_peptide_start:i+1]
                    peptide_nostar = re.sub("\\*", "", peptide)
                    
                    # Filter peptides by length (5 < length < 17)
                    if 5 < len(peptide_nostar) < 17:
                        if "*" in peptide:
                            peptides.append(peptide)
                    
                    # Update the start of the next peptide
                    current_peptide_start = i + 1
            else:
                # K or R at the end of the sequence is a cleavage site
                peptide = seq_in[current_peptide_start:i+1]
                peptide_nostar = re.sub("\\*", "", peptide)
                if 5 < len(peptide_nostar) < 17:
                    if "*" in peptide:
                        peptides.append(peptide)
                
                # Update start for the next (non-existent) peptide
                current_peptide_start = i + 1
    
    # Add the last peptide if there is any remaining sequence
    if current_peptide_start < seq_length:
        last_peptide = seq_in[current_peptide_start:]
        if "*" in last_peptide:
            peptides.append(last_peptide)
    

    min_len = len(min(peptides, key = len))
    
    peptides_out = []
    for pep_elem in peptides:
        if len(pep_elem) == min_len: 
            peptides_out.append(pep_elem)

    return peptides_out[-1]

# Example usage
pep_out = trypsin_digest(prot_seq_mod)
print(pep_out)
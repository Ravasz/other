library(tidyverse)


##### kinase test ##############################################################
find_kinase_target <- function(amino_acid_sequence, consensus_site) {
  # Convert inputs to uppercase for case-insensitive matching
  amino_acid_sequence <- toupper(amino_acid_sequence)
  consensus_site <- toupper(consensus_site)

  # Get the length of the consensus site
  pattern_length <- nchar(consensus_site)

  # Iterate through the amino acid sequence to find potential matches
  for (i in 1:(nchar(amino_acid_sequence) - pattern_length + 1)) {
    # Extract a subsequence of the same length as the consensus site
    subsequence <- substr(amino_acid_sequence, i, i + pattern_length - 1)

    # Check if the subsequence matches the consensus site
    match <- TRUE
    for (j in 1:pattern_length) {
      consensus_char <- substr(consensus_site, j, j)
      subsequence_char <- substr(subsequence, j, j)

      # If the consensus character is not 'X' and the characters don't match
      if (consensus_char != "X" && consensus_char != subsequence_char) {
        match <- FALSE
        break
      }
    }

    # If a match is found, return the starting position (1-based index)
    if (match) {
      return(i)
    }
  }

  # If no match is found, return NULL
  return(NULL)
}


find_kinase_target(
    "STEYIQSPLEIKDIAHTQTARTGKTHTAHIWKPEYFSRWKALROTSVDQDSGTTVSSNQLKMYGAEVGLIRHQTMRMPSNGFSIPKSSTSAKHGFEWIAPRGNYRLGDKFDHFDSCD",
    "XLROXSVDXDXX"
)

set.seed(1000)
measurement_a <- rnorm(5, mean = 30000, sd = 500) |> round()
measurement_b <- rnorm(5, mean = 30400, sd = 500) |> round()

t.test(measurement_a, measurement_b, paired = TRUE)$p.value

generate_values <- function() {
    trt <- rnorm(5, mean = 30000, sd = 500) |> round()
    ctrl <- rnorm(5, mean = 30400, sd = 500) |> round()
    return(list("trt" = trt, "ctrl" = ctrl))
}

cur_vals <- generate_values()
print(paste0(
    paste(cur_vals[["trt"]], collapse = " "), 
    " ", 
    paste(cur_vals[["ctrl"]], collapse = " "),
    " ",
    t.test(cur_vals[["trt"]], cur_vals[["ctrl"]], paired = TRUE)$statistic
))

### phosphopeptide test ########################################################

prot_seq <- "PVMHQRDQHFVERMPKPRGQPFTQYLLHDLQIQKVMISGGKKPMNECCWWRQPVNFDFSADKQAIYCVDIAKIDMQQDKWMHRQSISGTSLKMAAWNLGYHKISAFRVMHNKCPMANWMMIYMTLPRPTKQWSRFVKRQDLEYFQYCMFYQAILDTLLPIRYCNTNTCRKCEKMPKFTYQREGCRPDNIHASKYEFIG"

tryptic_cut <- function(seq_in) {

  peptides <- c()
  current_peptide_start <- 1
  seq_length <- nchar(seq_in)

  # Iterate through the protein sequence character by character
  for (i in 1:seq_length) {
    # Get the current amino acid
    current_aa <- substr(seq_in, i, i)

    # Check for Lysine (K) or Arginine (R)
    if (current_aa == "K" || current_aa == "R") {
      # Check if it's not the last amino acid in the sequence
      if (i < seq_length) {
        # Trypsin does not cut if K or R is followed by Proline (P)
        if (substr(seq_in, i + 1, i + 1) != "P") {
          # If it's a cleavage site, extract the peptide
          peptide <- substr(seq_in, current_peptide_start, i)
          if(nchar(peptide) > 5 & nchar(peptide) < 13) {
            peptides <- c(peptides, peptide)
          }
          
          # Update the start of the next peptide
          current_peptide_start <- i + 1
        }
      } else {
        # If K or R is the last amino acid, it's a cleavage site (no P to follow)
        peptide <- substr(seq_in, current_peptide_start, i)
        peptides <- c(peptides, peptide)
        
        # Update the start for the next (non-existent) peptide
        current_peptide_start <- i + 1
      }
    }
  }

  # Add the last peptide if there's any remaining sequence after the last cut
  if (current_peptide_start <= seq_length) {
    last_peptide <- substr(seq_in, current_peptide_start, seq_length)
    peptides <- c(peptides, last_peptide)
  }

  return(peptides)
}

tryptic_cut(prot_seq)

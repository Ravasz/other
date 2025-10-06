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
    "STEYIQSPLEIKDIAHTQTARTGKTHTAHIWKPEYFSRWKALRQTSVDQDSGTTVSSNQLKMYGAEVGLIRHQTMRMPSNGFSIPKSSTSAKHGFEWIAPRGNYRLGDKFDHFDSCD",
    "XLRQXSVDXDXX"
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
prot_seq_mod <- "PVS*HQRDQHT*FVERMPKPRGQPFT*QYLLHDLQIQKVMISGGKKPMNECCWWRQPVNFDFSADKQAIYCVDIAKIDMQQDKWMHRQSISGTSLKMAAWNLGYHKISAFRVMHNKCPMANWMMIYMTLPRPTKQWSRFVKRQDLEYFQYCMFYQAILDTLLPIRYCNTNTCRKCEKMPKFTY*QREGCRPDNIHASKYEFIG"

trypsin_digest <- function(seq_in) {

    peptides <- c()
    current_peptide_start <- 1
    seq_length <- nchar(seq_in)

    # Iterate through the protein sequence character by character
    for (i in 1:seq_length) {
        current_aa <- substr(seq_in, i, i)
        if (current_aa == "*") next
        if (current_aa == "K" || current_aa == "R") {
            # Check if it's not the last amino acid in the sequence
            if (i < seq_length) {
                next_aa <- substr(seq_in, i + 1, i + 1)

                # Trypsin does not cut if K or R is followed by Proline (P)
                if (next_aa != "P") {
                    # If it's a cleavage site, extract the peptide
                    peptide <- substr(seq_in, current_peptide_start, i)
                    peptide_nostar <- str_replace_all(peptide, "\\*", "")
                    print(peptide)
                    print(nchar(peptide_nostar))
                    if(nchar(peptide_nostar) > 5 & nchar(peptide_nostar) < 17) {
                        peptides <- c(peptides, peptide)
                    }
                    
                    # Update the start of the next peptide
                    current_peptide_start <- i + 1
                }
            } else {
                # If K or R is the last amino acid, it's a cleavage site (no P to follow)
                peptide <- substr(seq_in, current_peptide_start, i)
                peptide_nostar <- str_replace_all(peptide, "\\*", "")
                print(peptide)
                print(nchar(peptide_nostar))
                if(nchar(peptide_nostar) > 5 & nchar(peptide_nostar) < 17) {
                    peptides <- c(peptides, peptide)
                }
                
                # Update the start for the next (non-existent) peptide
                current_peptide_start <- i + 1
            }
        }
    }

    # Add the last peptide if there's any remaining sequence after the last cut
    if (current_peptide_start <= seq_length) {
        last_peptide <- substr(seq_in, current_peptide_start, seq_length)
        peptide_nostar <- str_replace_all(last_peptide, "\\*", "")
        print(last_peptide)
        print(nchar(peptide_nostar))
        if(nchar(peptide_nostar) > 5 & nchar(peptide_nostar) < 17) {
            peptides <- c(peptides, last_peptide)
        }
    }

    return(peptides)
}

pep_out <- trypsin_digest(prot_seq_mod)


mouse_matrix = matrix(
    c(253, 207, 291, 169), 
    nrow = 2, 
    byrow = TRUE, 
    dimnames = list(
        "Mouse" = c("OT1", "OT2"),
        "autoimmunity" = c("Yes", "No")
    )
)

print(fisher.test(mouse_matrix))




# ORC1 30585 30124 29821 30692 30206 30338 30367 29239 29877 31429 0.9262724
# ORC2 30375 29855 29886 29935 30907 30153 30544 29652 31211 30518 0.53
# ORC3 30285 29839 30229 30534 30162 30064 29983 29733 30512 30062 0.264176
# ORC4 29745 30397 30520 30090 29996 30143 30960 29658 29705 30448 0.9112587
# ORC5 30129 30246 29593 30449 29409 30223 31012 31251 30417 30756 0.08292843
# ORC6 29251 30330 30143 30694 29920 30170 30484 31098 30764 30568 0.0423089
# MCM2 29524 30399 30051 30668 29986 29489 29901 30555 30466 29861 0.6856001
# MCM3 30093 30462 30998 29851 29785 30247 30604 30632 30087 30402 0.3743958
# MCM4 30181 29617 29911 29592 29350 29801 31352 31012 30516 30307 0.06554106
# MCM5 30842 30514 30748 30556 30251 30424 30140 30811 30951 30204 0.6373761
# MCM6 29819 29419 29644 30174 30214 31230 30691 30472 30572 29934 0.07796511
# MCM7 30459 30365 29159 29883 29670 30362 30478 30353 30880 30083 0.1030876


# The above is a simulated experiment. I used the following R code to generate these results:

set.seed(990)
generate_values <- function() {
    trt <- rnorm(5, mean = 30000, sd = 500) |> round()
    ctrl <- rnorm(5, mean = 30400, sd = 500) |> round()
    return(list("trt" = trt, "ctrl" = ctrl))
}

# cur_vals <- generate_values()
# print(paste0(
#     paste(cur_vals[["trt"]], collapse = " "), 
#     " ", 
#     paste(cur_vals[["ctrl"]], collapse = " "),
#     " ",
#     t.test(cur_vals[["trt"]], cur_vals[["ctrl"]], paired = TRUE)$p.value
# ))


# print(paste0(
#     paste(cur_vals[["trt"]], collapse = " "), 
#     " ", 
#     paste(cur_vals[["ctrl"]], collapse = " ")
# ))


test_mat <- matrix(unlist(generate_values()), nrow = 1, byrow = TRUE)

for (i in seq(1:11)) {
    test_mat <- rbind(
        test_mat, 
        matrix(unlist(generate_values()), nrow = 1, byrow = TRUE)
    )
}

# set row and colnames
rownames(test_mat) <- c(
    "ORC1", 
    "ORC2", 
    "ORC3", 
    "ORC4", 
    "ORC5", 
    "ORC6", 
    "MCM2", 
    "MCM3", 
    "MCM4", 
    "MCM5", 
    "MCM6", 
    "MCM7" 
)

colnames(test_mat) <- c(paste0("trt", 1:5), paste0("ctrl", 1:5))

# check which are down in the treatment
trt_means <- apply(test_mat[,1:5], 1, mean) |>
    as.data.frame() |> 
    magrittr::set_colnames("trt_means") |> 
    rownames_to_column("ID")

ctrl_means <- apply(test_mat[,6:10], 1, mean) |> 
    as.data.frame() |> 
    magrittr::set_colnames("ctrl_means") |> 
    rownames_to_column("ID")

means_df <- trt_means |> left_join(ctrl_means, by = "ID") |>
    mutate("diff" = trt_means - ctrl_means)

pos_means_to_remove <- means_df |> filter(diff > 0) |> pull(ID)

# scale df
scaled_df <- t(scale(t(test_mat))) |> 
    as.data.frame() 

# filter for low sd
deviations <- apply(as.matrix(scaled_df), 2, sd) |> 
    as.data.frame() |>
    set_names("SD") |>
    rownames_to_column("ID") |>
    filter(SD < 1)

filt_df <- scaled_df |> dplyr::select(all_of(deviations[["ID"]])) |>
    rownames_to_column("ID")

trt_cols <- intersect(paste0("trt", 1:5), colnames(filt_df))
ctrl_cols <- intersect(paste0("ctrl", 1:5), colnames(filt_df))

proc_df <- filt_df |>
    rowwise() |> 
    mutate(
        trt_cols = list(c_across(starts_with("trt"))),
        ctrl_cols = list(c_across(starts_with("ctrl"))),
        ttest_result = list(t.test(trt_cols, ctrl_cols)),
        p_value = ttest_result$p.value
    ) |>
    ungroup() |>
    dplyr::select(-c("trt_cols", "ctrl_cols", "ttest_result")) 
    
res_text <- proc_df |>
    filter(p_value < 0.05) |>
    filter(!ID %in% pos_means_to_remove) |>
    pull(p_value, ID) |>
    round(3)


# reformat output
out_str <- ""
for (i in seq_along(res_text)) {
    if (i == 1) {out_str <- paste0(
        out_str, 
        names(res_text)[i],
        "=", 
        unname(res_text[i])
    )}
    else {out_str <- paste0(
        out_str, 
        ", ", 
        names(res_text)[i], 
        "=", 
        unname(res_text[i])
    )}
}

out_filt_str = ""
for (i in seq_along(pos_means_to_remove)) {
    out_filt_str <- paste0(out_filt_str, pos_means_to_remove[i], "X, ")
}

print(paste0(out_filt_str, out_str))

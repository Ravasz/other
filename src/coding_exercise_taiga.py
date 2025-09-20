import pandas as pd
import numpy as np
from scipy import stats

# Define the matrix
Test_mat = pd.DataFrame(
    [
        [29863, 29693, 30539, 30073, 30067, 30678, 30626, 31254, 30447, 30582],
        [30534, 30286, 30601, 29539, 30507, 30988, 30162, 30378, 31438, 29839],
        [30412, 28996, 30129, 29997, 30622, 31536, 31218, 30466, 30412, 31472],
        [28983, 29928, 30168, 30140, 29981, 30794, 30438, 30304, 30543, 30006],
        [29325, 30705, 30125, 30108, 29149, 30212, 30615, 30709, 31144, 30473],
        [30399, 30508, 30416, 29604, 30340, 30625, 30213, 30389, 30221, 29068],
        [30540, 30788, 30087, 29429, 30256, 30156, 30230, 30827, 31073, 31268],
        [30054, 29851, 29944, 30048, 30192, 30879, 31038, 30569, 30779, 30721],
        [30916, 29642, 30405, 30755, 30570, 30637, 30649, 30535, 30580, 30775],
        [29446, 29379, 30231, 30668, 30637, 30584, 30843, 31106, 30316, 30350],
        [30060, 29180, 30248, 29959, 29497, 30571, 30319, 31356, 31043, 29099],
        [31182, 29445, 29861, 29934, 30429, 31381, 30207, 30310, 30256, 31035],
    ],
    index=[
        "ORC1", "ORC2", "ORC3", "ORC4", "ORC5", "ORC6", "MCM2", "MCM3", "MCM4", "MCM5", "MCM6", "MCM7"
    ],
    columns=[
        "trt1", "trt2", "trt3", "trt4", "trt5", "ctrl1", "ctrl2", "ctrl3", "ctrl4", "ctrl5"
    ]
)

# Calculate treatment and control means
trt_means = Test_mat.iloc[:, :5].mean(axis=1)
ctrl_means = Test_mat.iloc[:, 5:].mean(axis=1)

# Create means DataFrame and filter for positive differences
means_df = pd.DataFrame({'trt_means': trt_means, 'ctrl_means': ctrl_means})
means_df['diff'] = means_df['trt_means'] - means_df['ctrl_means']
pos_means_to_remove = means_df[means_df['diff'] > 0].index.tolist()

# Scale the DataFrame
scaled_df = pd.DataFrame(
    stats.zscore(Test_mat.T, axis=0),
    index=Test_mat.columns,
    columns=Test_mat.index
).T

# Filter for low standard deviation
deviations = scaled_df.std()
filt_df = scaled_df.loc[:, deviations < 1]

# Perform t-test for each row
trt_cols = [col for col in filt_df.columns if 'trt' in col]
ctrl_cols = [col for col in filt_df.columns if 'ctrl' in col]

p_values = {}
for index, row in filt_df.iterrows():
    trt_data = row[trt_cols].dropna()
    ctrl_data = row[ctrl_cols].dropna()
    if not trt_data.empty and not ctrl_data.empty:
        t_stat, p_val = stats.ttest_ind(trt_data, ctrl_data, equal_var=False)
        p_values[index] = p_val

# Create the final result Series
proc_df = pd.Series(p_values)

# Filter based on p-value and 'pos_means_to_remove'
res_text = proc_df[(proc_df < 0.05) & (~proc_df.index.isin(pos_means_to_remove))]

# Format and print the output
out_str = ", ".join([f"{idx}={p_val:.3f}" for idx, p_val in res_text.items()])
out_filt_str = ", ".join([f"{idx}X" for idx in pos_means_to_remove])

print(f"{out_filt_str}, {out_str}")
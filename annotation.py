# Split documents into two batches: 'exploration' and 'evaluation'
# 250 exploration documents and 250 evaluation documents

# Import Libraries
import pandas as pd

# Read in the data
df = pd.read_csv('reviews_to_annotate.csv')

# Shuffle the data
df = df.sample(frac=1, random_state = 42).reset_index(drop=True)

# Split the data into two batches; exploration and evaluation
explore = df[:250]
evaluate = df[250:500]

# Save the data as csv files
explore.to_csv('explore.csv', index=False)
evaluate.to_csv('evaluate.csv', index=False)

import pandas as pd
from io import StringIO

data = {
    'Column1': [1, 2, [3, 4]],
    'Column2': [4, 5, 6],
    'Column3': [7, 8, [9, 0]]
}

df = pd.DataFrame(data)

print(df)

js = df.to_json()

print(js)

df2 = pd.read_json(StringIO(js))

print(df2)

import json
# Load the list of JSON strings from the file
#with open('dataframes.json', 'r') as f:
#    json_dfs = json.load(f)

# Convert each JSON string back into a DataFrame and store it in a list
# dfs = [pd.read_json(StringIO(json_df)) for json_df in json_dfs]

#dfs = []
#with open('dataframes.json', 'r') as f:
#    for line in f:
#        # Convert the JSON string back into a DataFrame
#        df = pd.read_json(StringIO(line))
#        # Append the DataFrame to the list
#        dfs.append(df)

#for df in dfs:
#    print("\n", df)

# Initialize an empty dictionary to store the dataframes
dfs = {}

# Open the file and read each line
with open('dataframes2.json', 'r') as f:
    for line in f:
        # Remove any trailing newline characters
        line = line.rstrip('\n')

        # Convert the JSON string back into a dictionary
        group_dict = json.loads(line)

        # For each key-value pair in the dictionary
        for key, value in group_dict.items():
            # If the key is 'data', convert the JSON string back into a DataFrame
            if key == 'data':
                df = pd.read_json(StringIO(value))
                # Use the 'id' value as the key to store the DataFrame in the dictionary
                dfs[group_dict['id']] = df

print(dfs)
print(dfs['df7'])
#TODO: When saving as dict, make key 'nameofconfed_stage_groupletter' then can filter by what string contained in key
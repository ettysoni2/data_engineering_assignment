import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns


# Reading and transforming the raw data
root_dir = r"/Users/ettys/Library/CloudStorage/OneDrive-SpinMasterLtd/dev/data_engineering_assignment"
data_dir = r"/Users/ettys/Library/CloudStorage/OneDrive-SpinMasterLtd/dev/data_engineering_assignment/raw_data"

os.chdir(data_dir)

with open(os.path.join(root_dir, 'output_file.csv'), 'w+') as csv_file:
    for path in glob.glob('./*.TXT'):
        with open(path) as txt_file:
            txt = txt_file.read() + '\n'
            csv_file.write(txt)

os.chdir(root_dir)

data = pd.read_csv('output_file.csv', header=None)
data.columns = ["state", "gender", "year", "name", "count"]
data = data[data["year"] > 2000]


# Understanding the data
print(data.head())
print(data.info())

data["year"] = data["year"].astype(str)

print(data.describe())
print(data["name"].value_counts().shape)



# Data checks
def isnull(data):
    print(data.isnull().any())

isnull(data)

def check_state_length(data):
    state_length = data['state'].str.len()
    state_length = state_length.to_numpy()
    if((state_length[0] == state_length).all()) == True:
        print("Check pass")
    else:
        print("Data quality issue found")

check_state_length(data)

def check_year_length(data):
    year_length = data['state'].str.len()
    year_length = year_length.to_numpy()
    if((year_length[0] == year_length).all()) == True:
        print("Check pass")
    else:
        print("Data quality issue found")

check_year_length(data)



# Function to create gender neutral names
def gender_neutral_names(data):
    """
    Returns gender neutral names

    data: dataframe
    """

    df_m=data[data['gender']=='M'].groupby(['name','gender'])['count'].sum()
    df_f=data[data['gender']=='F'].groupby(['name','gender'])['count'].sum()
    df_unisex=pd.merge(df_f,df_m,how='inner',on='name').reset_index()
    df_unisex["total"] = df_unisex['count_y']+ df_unisex['count_x']
    df_unisex['prop_x']=df_unisex['count_x']/df_unisex['total']
    df_unisex['prop_y']=df_unisex['count_y']/df_unisex['total']
    df_unisex['diff']=abs(df_unisex['prop_x']-df_unisex['prop_y'])
    df_unisex[(df_unisex['total']>=500) & (df_unisex['diff']<0.3)]
    print(df_unisex['name'])

gender_neutral_names(data)



# Function to create labeled barplots
def labeled_barplot(data, feature, perc=False, n=None):
    """
    Barplot with percentage at the top

    data: dataframe
    feature: dataframe column
    perc: whether to display percentages instead of count (default is False)
    n: displays the top n category levels (default is None, i.e., display all levels)
    """

    total = len(data[feature])  # length of the column
    count = data[feature].nunique()
    if n is None:
        plt.figure(figsize=(count + 1, 5))
    else:
        plt.figure(figsize=(n + 1, 5))

    plt.xticks(rotation=90, fontsize=15)
    ax = sns.countplot(
        data=data,
        x=feature,
        palette="Paired",
        order=data[feature].value_counts().index[:n].sort_values(),
    )

    for p in ax.patches:
        if perc == True:
            label = "{:.3f}%".format(
                100 * p.get_height() / total
            )  # percentage of each class of the category
        else:
            label = p.get_height()  # count of each level of the category

        x = p.get_x() + p.get_width() / 2  # width of the plot
        y = p.get_height()  # height of the plot

        ax.annotate(
            label,
            (x, y),
            ha="center",
            va="center",
            size=12,
            xytext=(0, 5),
            textcoords="offset points",
        )  # annotate the percentage

    plt.show()  # show the plot

'''
What is the split of the gender in the data?
'''
labeled_barplot(data, "gender", perc=True)

'''
Top 10 states
'''
labeled_barplot(data, "state", perc=True)

'''
Top 10 names
'''
labeled_barplot(data, "name", perc=True, n = 10)


# Saving the transformed data to use it in the powerBI dashboard
data.to_csv(r"/Users/ettys/Library/CloudStorage/OneDrive-SpinMasterLtd/dev/data_engineering_assignment/pbi_input.csv", index=False)
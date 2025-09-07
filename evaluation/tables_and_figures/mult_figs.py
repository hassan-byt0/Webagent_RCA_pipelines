import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns   
import numpy as np

TSR_DIFF_1 = "./tables/single/tsr_difference_relative-1dp-coarse.csv"
TSR_DIFF_2 = "./tables/double/tsr_difference_benign_relative-2dp-coarse.csv"
TSR_DIFF_3 = "./tables/triple/tsr_difference_benign_relative-3dp-coarse.csv"
TSR_DIFF_4 = "./tables/quad/tsr_difference_benign_relative-4dp-coarse.csv"

DPSR_DIFF_2 = "./tables/double/dpsr_difference_relative-2dp-coarse.csv"
DPSR_DIFF_3 = "./tables/triple/dpsr_difference_relative-3dp-coarse.csv"
DPSR_DIFF_4 = "./tables/quad/dpsr_difference_relative-4dp-coarse.csv"

def custom_round(x):
    if x < 1:
        return round(x)
    elif x < 1000:
        return round(x / 100) * 100
    else:
        return round(x / 500) * 500

def generate_mult_graphs_tsr():
    df1 = pd.read_csv(TSR_DIFF_1)
    df2 = pd.read_csv(TSR_DIFF_2)
    df3 = pd.read_csv(TSR_DIFF_3)
    df4 = pd.read_csv(TSR_DIFF_4)

    df1['Source'] = '1 DP'
    df2['Source'] = '2 DP'
    df3['Source'] = '3 DP'
    df4['Source'] = '4 DP'

    # Merge dataframes on 'Agent' column
    merged_df = pd.merge(df1[['Agent', 'Overall']], df2[['agent', 'Overall']], left_on='Agent', right_on='agent', suffixes=('_dp1', '_dp2'))
    merged_df = pd.merge(merged_df, df3[['agent', 'Overall']], on='agent', suffixes=('', '_dp3'))
    merged_df = pd.merge(merged_df, df4[['agent', 'Overall']], on='agent', suffixes=('', '_dp4'))

    # Drop duplicate 'agent' column and rename columns
    merged_df = merged_df.drop(columns=['agent'])
    merged_df.columns = ['Agent', 'Overall_dp1', 'Overall_dp2', 'Overall_dp3', 'Overall_dp4']

    # Plot grouped bar graph
    plt.figure(figsize=(10, 6))
    merged_df.set_index('Agent').plot(
        kind='bar', 
        width=0.8,
        # color=['tomato', 'lightblue', 'lawngreen', 'thistle'],
        color=['#377eb8', '#e41a1c', '#4daf4a', '#984ea3'],
        edgecolor='black',
        zorder=3)

    # Add title and labels
    # plt.title('Overall Values by Agent for dp1, dp2, dp3, and dp4')
    plt.xlabel('')
    plt.ylabel('Relative Difference in Task Success Rate (%)')
    plt.xticks(rotation=0)
    plt.legend(title='Data Points', labels=['1 DP Enabled', '2 DP Enabled', '3 DP Enabled', '4 DP Enabled'])
    plt.grid(axis='y', linestyle='--', color='lightgray', linewidth=0.5)

    # Display the graph
    plt.tight_layout()
    plt.savefig("./graphs/mult/eval_mult_tsr_diff.pdf")

    # merged_df.to_csv("./test/mult_graphs/merged_tsr_diff.csv")

def generate_mult_graphs_dpsr():
    df2 = pd.read_csv(DPSR_DIFF_2)
    df3 = pd.read_csv(DPSR_DIFF_3)
    df4 = pd.read_csv(DPSR_DIFF_4)

    df2['Source'] = '2 DP'
    df3['Source'] = '3 DP'
    df4['Source'] = '4 DP'

    # Merge dataframes on 'Agent' column
    merged_df = pd.merge(df2[['Agent', 'overall']], df3[['Agent', 'overall']], left_on='Agent', right_on='Agent', suffixes=('_dp2', '_dp3'))
    merged_df = pd.merge(merged_df, df4[['Agent', 'overall']], on='Agent', suffixes=('', '_dp4'))

    # Drop duplicate 'agent' column and rename columns
    merged_df.columns = ['Agent', 'overall_dp2', 'overall_dp3', 'overall_dp4']
    
    # Get unique agents
    agents = merged_df['Agent'].unique()
    
    # Create a figure with subplots (one for each agent)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))  # 2 rows, 3 columns for 6 agents
    axes = axes.flatten()  # Flatten to make indexing easier
    plt.xticks(fontsize=16)
    
    # Colors for the bars
    colors = ['tomato', 'lightblue', 'lawngreen']
    colors=['#377eb8', '#e41a1c', '#4daf4a', '#984ea3']
    
    # For each agent, create a single subplot
    for i, agent in enumerate(agents):
        # Get data for this agent
        agent_data = merged_df[merged_df['Agent'] == agent]
        
        # Extract values for plotting
        values = [agent_data['overall_dp2'].values[0], 
                  agent_data['overall_dp3'].values[0], 
                  agent_data['overall_dp4'].values[0]]
        
        # Create the bar plot
        bars = axes[i].bar(['2 DP', '3 DP', '4 DP'], values, 
                           color=colors, 
                           edgecolor='black', width=0.6, zorder=3)
        
        # Set the title and labels
        axes[i].set_title(agent, fontsize=16)
        axes[i].set_ylabel('Relative Difference From Single DP(%)', fontsize = 14)
        axes[i].set_xticklabels(axes[i].get_xticklabels(), fontsize=16)
        axes[i].set_yticklabels(axes[i].get_yticklabels(), fontsize=16)
        axes[i].grid(axis='y', linestyle='--', color='lightgray', linewidth=0.5)
        
        # Add value labels on the bars
        for bar in bars:
            height = bar.get_height()
            axes[i].text(bar.get_x() + bar.get_width()/2., height,
                         f'{(height):.0f}',
                         ha='center', va='bottom', rotation=0, zorder=3, fontsize=14)
    
    # Add a common title
    # fig.suptitle('Relative Difference in Dark Pattern Success Rate by Agent', fontsize=16)
    
    # Adjust spacing
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)  # Make room for the suptitle
    
    # Save the figure
    plt.savefig("./graphs/mult/eval_mult_dpsr_diff.pdf")
    
    # Save the data
    # merged_df.to_csv("./test/mult_graphs/merged_dpsr_diff.csv")


def generate_mult_graphs_dpsr_new():
    df2 = pd.read_csv(DPSR_DIFF_2)
    df3 = pd.read_csv(DPSR_DIFF_3)
    df4 = pd.read_csv(DPSR_DIFF_4)

    df2['Source'] = '2 DP'
    df3['Source'] = '3 DP'
    df4['Source'] = '4 DP'

    # Merge dataframes on 'Agent' column
    merged_df = pd.merge(df2[['Agent', 'overall']], df3[['Agent', 'overall']], left_on='Agent', right_on='Agent', suffixes=('_dp2', '_dp3'))
    merged_df = pd.merge(merged_df, df4[['Agent', 'overall']], on='Agent', suffixes=('', '_dp4'))

    # Drop duplicate 'agent' column and rename columns
    merged_df.columns = ['Agent', 'overall_dp2', 'overall_dp3', 'overall_dp4']
    
    # Get unique agents
    agents = merged_df['Agent'].unique()
    
    # Create a figure with subplots (one for each agent)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))  # 2 rows, 3 columns for 6 agents
    axes = axes.flatten()  # Flatten to make indexing easier
    plt.xticks(fontsize=16)
    
    # Colors for the bars
    colors=['#377eb8', '#e41a1c', '#4daf4a', '#984ea3']
    
    # For each agent, create a single subplot
    for i, agent in enumerate(agents):
        # Get data for this agent
        agent_data = merged_df[merged_df['Agent'] == agent]
        
        # Extract values for plotting
        values = [agent_data['overall_dp2'].values[0], 
                  agent_data['overall_dp3'].values[0], 
                  agent_data['overall_dp4'].values[0]]
        
        x = [0,1.2,2.4]
        labels = ['2 DP', '3 DP', '4 DP']
        # Create the bar plot
        bars = axes[i].bar(x, values, 
                           color=colors, 
                           edgecolor='black', width=0.6, zorder=3)
        
        # Set the title and labels
        axes[i].set_title(agent, fontsize=16)
        axes[i].set_ylabel('Relative Difference From Single DP(%)', fontsize = 14)
        axes[i].set_xticks(x)
        axes[i].set_xticklabels(labels, fontsize=16)
        axes[i].set_yticklabels(axes[i].get_yticklabels(), fontsize=16)
        axes[i].grid(axis='y', linestyle='--', color='lightgray', linewidth=0.5)
        for bar in bars:
            height = bar.get_height()
            axes[i].text(bar.get_x() + bar.get_width()/2., height,
                        f'{(height):.0f}',
                        ha='center', va='bottom', rotation=0, zorder=3, fontsize=14)
    
    # Add a common title
    # fig.suptitle('Relative Difference in Dark Pattern Success Rate by Agent', fontsize=16)
    
    # Adjust spacing
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)  # Make room for the suptitle
    
    # Save the figure
    plt.savefig("./graphs/mult/eval_mult_dpsr_diff.pdf")
    
    # Save the data
    # merged_df.to_csv("./test/mult_graphs/merged_dpsr_diff.csv")

    


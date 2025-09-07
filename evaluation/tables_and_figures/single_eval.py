import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# fine = fine grained data --> shows rates for each dp under each prompt
# coarse = coarse grained data --> shows rate for each dp
# general = general-grained data --> shows rates for each agent

# tsr = task success rate
# dpsr = dark pattern susceptibility rate
# cm = confusion matrix of DC, EC, DF, EF

SINGLE_DP_DP_TASK_SUCCESS_FINE_GRAINED = "./tables/single/cm-1dp-fine.csv"
SINGLE_DP_DP_TASK_SUCCESS_COARSE_GRAINED = "./tables/single/cm-1dp-coarse.csv"
SINGLE_DP_DP_TASK_SUCCESS_GENERAL = "./tables/single/cm-1dp-general.csv"
SINGLE_DP_TASK_SUCCESS_FINE_GRAINED = "./tables/single/tsr-1dp-fine.csv"
SINGLE_DP_DP_SUCCESS_FINE_GRAINED = "./tables/single/dpsr-1dp-fine.csv"
SINGLE_DP_DP_SUCCESS_COARSE_GRAINED = "./tables/single/dpsr-1dp-coarse.csv"
SINGLE_DP_TASK_SUCCESS = "./tables/single/tsr-1dp-general.csv"
SINGLE_DP_DP_SUCCESS = "./tables/single/dpsr-1dp-general.csv"
SINGLE_DP_TC_DIFFERENCE = "./tables/single/tsr_difference-1dp-coarse.csv"
SINGLE_DP_TC_DIFFERENCE_RELATIVE = "./tables/single/tsr_difference_relative-1dp-coarse.csv"
SINGLE_DP_DP_ATTRIBUTE = "./tables/single/dp_attribute-1dp-general.csv"
SINGLE_DP_DP_ATTRIBUTE_TASK_COMPLETE_ONLY = "./tables/single/dp_attribute_task_complete_only-1dp-general.csv"

DP_ATTRIBUTE = {
    'shop_p1': ['obstruction', 'interface interference', 'forced action', 'social engineering'],
    'shop_p2': ['obstruction', 'interface interference', 'forced action'],
    'shop_w': ['sneaking'],
    'shop_s': ['interface interference'],
    'news_ob': ['obstruction', 'interface interference', 'forced action'],
    'news_bs': ['sneaking', 'interface interference', 'forced action'],
    'news_sa': ['interface interference'],
    'news_cf': ['interface interference', 'forced action', 'social engineering'],
    'spotify_du': ['obstruction', 'interface interference', 'forced action'],
    'spotify_ds': ['obstruction', 'interface interference', 'forced action', 'social engineering'],
    'spotify_am': ['interface interference', 'social engineering'],
    'health_cs': ['obstruction', 'interface interference', 'social engineering'],
    'health_tos': ['interface interference', 'forced action', 'social engineering'],
    'health_cf': ['interface interference', 'forced action', 'social engineering'],
}

######################################################################################################
########### SINGLE


# Single Dark Pattern Tables
# Tables we might want: 
# 1. Agent success rate on each website for each agent

def single_data_eval(full_agent_data, benign_dfs):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(full_agent_data)

    # Filter rows where dp1 is not empty, but dp2, dp3, and dp4 are empty
    filtered_df = df[df['dp1'].notnull() & (df['dp1'] != '') &
                 (df['dp2'].isna() | (df['dp2'] == '')) &
                 (df['dp3'].isna() | (df['dp3'] == '')) &
                 (df['dp4'].isna() | (df['dp4'] == ''))].copy()
    
    filtered_df['site_name'] = df['site'].apply(lambda x: x.split('/')[1].split('?')[0] if isinstance(x, str) and '/' in x else x)
    filtered_df['scenario'] = filtered_df['site_name'] + ":" + filtered_df['dp1'] + ":" + filtered_df['prompt']
    filtered_df['dp1_key'] = filtered_df['site_name'] + "_" + filtered_df['dp1']

    # Define conditions for the new column
    conditions = [
        (filtered_df['task_correct'] == True) & (filtered_df['dp1_susceptibility'] == True),
        (filtered_df['task_correct'] == True) & (filtered_df['dp1_susceptibility'] == False),
        (filtered_df['task_correct'] == False) & (filtered_df['dp1_susceptibility'] == True),
        (filtered_df['task_correct'] == False) & (filtered_df['dp1_susceptibility'] == False)
    ]

    # Define corresponding values for each condition
    choices = ['DC', 'EC', 'DF', 'EF']

    # Create the new column using np.select
    filtered_df['type'] = np.select(conditions, choices, default=None)

    # Define the list of categories to check
    categories = ['obstruction', 'sneaking', 'interface interference', 'forced action', 'social engineering']

    # Initialize new columns with False (default state)
    for category in categories:
        filtered_df[category] = False
    
    # Update values based on DP_ATTRIBUTE
    for idx, row in filtered_df.iterrows():
        dp_key = f"{row['site_name']}_{row['dp1']}"
        if dp_key in DP_ATTRIBUTE:
            for pattern in DP_ATTRIBUTE[dp_key]:
                filtered_df.at[idx, pattern] = True

    filtered_df = filtered_df[['agent', 'site_name', 'scenario', 'prompt', 'dp1', 'dp1_key', 'task_correct', 
                               'dp1_susceptibility', 'type', 'obstruction', 'sneaking', 'interface interference', 'forced action', 'social engineering']]

    agent_mapping = {
    'visualwebarena': 'VisualWebArena',
    'skyvern': 'Skyvern',
    'agente': 'Agent-E',
    'dobrowser': 'DoBrowser',
    'browseruse': 'BrowserUse',
    'webarena': 'WebArena',
    }

    filtered_df['agent'] = filtered_df['agent'].replace(agent_mapping)
    # Need to exclude the other experiments (attribute changes, and postscripts)
    # exclude postscripts experiments:
    with open('postscripts.txt', 'r') as file:
        exclude_prompts = [line.strip() for line in file]
    # Filter the dataframe to exclude rows where 'prompts' column value is in the exclude_prompts list
    filtered_df = filtered_df[~filtered_df['prompt'].isin(exclude_prompts)]

    # exclude attribute changes experiments:
    attribute_change_codes = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
    filtered_df = filtered_df[~filtered_df['dp1'].isin(attribute_change_codes)]

    # exclude vision ablation study experiments
    excluded_agents = ['browseruse_vis', 'dobrowser_novis']
    filtered_df = filtered_df[~filtered_df['agent'].isin(excluded_agents)]

    filtered_df.to_csv("./raw_df/single_dp.csv")

    ###### GET STATISTICS FOR HOW MANY DARK PATTERNS ALL AGENTS FELL FOR ######
    # Calculate the percentage of True values in the "dp_susceptibility" column
    true_count = filtered_df['dp1_susceptibility'].sum()  # Sum of True values (True is treated as 1)
    total_count = len(filtered_df['dp1_susceptibility'])  # Total number of rows
    true_percentage = (true_count / total_count) * 100
    print(f"DP1 Susceptibility Rate on Agents: {true_percentage:.2f}%")

    task_correct_df = filtered_df[filtered_df['task_correct'] == True]
    task_correct_true_count = task_correct_df['dp1_susceptibility'].sum()  # Sum of True values (True is treated as 1)
    task_correct_total_count = len(task_correct_df['dp1_susceptibility'])  # Total number of rows
    task_correct_true_percentage = (task_correct_true_count / task_correct_total_count) * 100
    print(f"DP1 Susceptibility Rate on Task Correct Agents: {task_correct_true_percentage:.2f}%")

    task_incorrect_df = filtered_df[filtered_df['task_correct'] == False]
    task_incorrect_true_count = task_incorrect_df['dp1_susceptibility'].sum()  # Sum of True values (True is treated as 1)
    task_incorrect_total_count = len(task_incorrect_df['dp1_susceptibility'])  # Total number of rows
    task_incorrect_true_percentage = (task_incorrect_true_count / task_incorrect_total_count) * 100
    print(f"DP1 Susceptibility Rate on Task Incorrect Agents: {task_incorrect_true_percentage:.2f}%")

    ###### TABLE GENERATION FOR AGENT DP/TASK SUCCESS RATE (FINE-GRAINED) ######
    fine_grained_dp_task_summary = filtered_df.groupby(['agent', 'scenario', 'type']).size().reset_index(name='count')

    ###### TABLE GENERATION FOR AGENT DP/TASK SUCCESS RATE (COARSE-GRAINED) ######
    coarse_grained_dp_task_summary = filtered_df.groupby(['agent', 'site_name', 'type']).size().reset_index(name='count')
    coarse_grained_dp_task_summary = coarse_grained_dp_task_summary.pivot(index=['agent', 'site_name'], columns='type', values='count').fillna(0)
    coarse_grained_dp_task_summary = coarse_grained_dp_task_summary.div(coarse_grained_dp_task_summary.sum(axis=1), axis=0) * 100
    coarse_grained_dp_task_summary = coarse_grained_dp_task_summary.round(1)
    coarse_grained_dp_task_summary.reset_index(inplace=True)

    ###### TABLE GENERATION FOR AGENT DP/TASK SUCCESS RATE (COARSE-GRAINED) ######
    general_dp_task_summary = filtered_df.groupby(['agent', 'type']).size().reset_index(name='count')
    general_dp_task_summary = general_dp_task_summary.pivot(index='agent', columns='type', values='count').fillna(0)
    general_dp_task_summary = general_dp_task_summary.div(general_dp_task_summary.sum(axis=1), axis=0) * 100
    general_dp_task_summary = general_dp_task_summary.round(1)
    # general_dp_task_summary.reset_index(inplace=True)

    ###### TABLE GENERATION FOR AGENT SUCCESS RATE (FINE-GRAINED) ######
    fine_grained_task_summary = filtered_df.groupby(['agent', 'scenario'])['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    fine_grained_task_summary = fine_grained_task_summary.pivot(index='agent', columns='scenario', values='task_correct')
    fine_grained_task_summary['Overall'] = filtered_df.groupby('agent')['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    fine_grained_task_summary.reset_index()
    fine_grained_task_summary = fine_grained_task_summary.rename(columns={'agent': 'Agent'})

    ###### TABLE GENERATION FOR AGENT SUSCEPTIBILITY RATE (FINE-GRAINED) ######
    fine_grained_dp_summary = filtered_df.groupby(['agent', 'scenario'])['dp1_susceptibility'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    fine_grained_dp_summary = fine_grained_dp_summary.pivot(index='agent', columns='scenario', values='dp1_susceptibility')
    fine_grained_dp_summary['Overall'] = filtered_df.groupby('agent')['dp1_susceptibility'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    fine_grained_dp_summary.reset_index()
    fine_grained_dp_summary = fine_grained_dp_summary.rename(columns={'agent': 'Agent'})

    ###### TABLE GENERATION FOR AGENT SUSCEPTIBILITY RATE (COARSE-GRAINED) ######
    coarse_grained_dp_summary = filtered_df.groupby(['agent', 'dp1_key'])['dp1_susceptibility'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    coarse_grained_dp_summary = coarse_grained_dp_summary.pivot(index='agent', columns='dp1_key', values='dp1_susceptibility')
    coarse_grained_dp_summary['Overall'] = filtered_df.groupby('agent')['dp1_susceptibility'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    coarse_grained_dp_summary = coarse_grained_dp_summary.reset_index()
    coarse_grained_dp_summary = coarse_grained_dp_summary.rename(columns={'agent': 'Agent'})

    ###### TABLE GENERATION FOR TASK SUCCESS RATE ######
    performance_summary = filtered_df.groupby(['agent', 'site_name'])['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    performance_summary = performance_summary.pivot(index='agent', columns='site_name', values='task_correct')
    performance_summary['Overall'] = filtered_df.groupby('agent')['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    performance_summary = performance_summary.reset_index()
    performance_summary = performance_summary.rename(columns={'agent': 'Agent'})    
    
    ###### TABLE GENERATION FOR DP SUSCEPTIBILITY RATE ######
    dp_summary = filtered_df.groupby(['agent', 'site_name'])['dp1_susceptibility'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    dp_summary = dp_summary.pivot(index='agent', columns='site_name', values='dp1_susceptibility')
    dp_summary['Overall'] = filtered_df.groupby('agent')['dp1_susceptibility'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    dp_summary = dp_summary.reset_index()
    dp_summary = dp_summary.rename(columns={'agent': 'Agent'})    

    ###### TABLE FOR TASK RATE COMPARISON WITH BENIGN ######
    tc_difference = performance_summary.copy() 
    columns_to_subtract = ['health', 'news', 'shop', 'spotify', 'Overall']
    tc_difference[columns_to_subtract] = performance_summary[columns_to_subtract] - benign_dfs['general_tc_summary'][columns_to_subtract]

    tc_relative_difference = tc_difference.copy()
    tc_relative_difference[columns_to_subtract] = ((tc_difference[columns_to_subtract] / benign_dfs['general_tc_summary'][columns_to_subtract]) * 100).round(1)

    ###### TABLE DP SUSCEPTIBILITY BY DP ATTRIBUTE ######
    results = []
    # Process each agent individually
    for agent in filtered_df['agent'].unique():
        agent_data = filtered_df[filtered_df['agent'] == agent]
        agent_result = {'agent': agent}
        # Calculate for each attribute
        for attr in categories:
            # Get all instances where this attribute was present
            attr_occurrences = agent_data[agent_data[attr]]
            # Calculate susceptibility rate for this attribute
            total_cases = len(attr_occurrences)
            susceptible_cases = attr_occurrences['dp1_susceptibility'].sum()
            # Calculate percentage (handle zero cases)
            percentage = (susceptible_cases / total_cases * 100) if total_cases > 0 else None
            agent_result[attr] = round(percentage, 1)
        results.append(agent_result)
    dps_by_category_summary = pd.DataFrame(results).set_index('agent')

    # Add an 'Overall' row to calculate the overall rates of all agents
    overall_result = {'agent': 'Overall'}

    for attr in categories:
        # Get all instances where this attribute was present across all agents
        attr_occurrences = filtered_df[filtered_df[attr]]
        # Calculate susceptibility rate for this attribute
        total_cases = len(attr_occurrences)
        susceptible_cases = attr_occurrences['dp1_susceptibility'].sum()
        # Calculate percentage (handle zero cases)
        percentage = (susceptible_cases / total_cases * 100) if total_cases > 0 else None
        overall_result[attr] = round(percentage, 1)
    
    dps_by_category_summary = dps_by_category_summary.reset_index()
    dps_by_category_summary = pd.concat([dps_by_category_summary, pd.DataFrame([overall_result])], ignore_index=True)
    dps_by_category_summary = dps_by_category_summary.set_index('agent')

    ###### TABLE DP SUSCEPTIBILITY BY DP ATTRIBUTE ONLY DC ######
    task_complete_df = filtered_df[filtered_df['task_correct'] == True]
    task_complete_results = []
    # Process each agent individually
    for agent in task_complete_df['agent'].unique():
        agent_data = task_complete_df[task_complete_df['agent'] == agent]
        agent_result = {'agent': agent}
        # Calculate for each attribute
        for attr in categories:
            # Get all instances where this attribute was present
            attr_occurrences = agent_data[agent_data[attr]]
            # Calculate susceptibility rate for this attribute
            total_cases = len(attr_occurrences)
            susceptible_cases = attr_occurrences['dp1_susceptibility'].sum()
            # Calculate percentage (handle zero cases)
            percentage = (susceptible_cases / total_cases * 100) if total_cases > 0 else None
            if total_cases > 0:
                agent_result[attr] = round(percentage, 2)
            else:
                agent_result[attr] = None
        task_complete_results.append(agent_result)
    dps_by_category_task_complete_only_summary = pd.DataFrame(task_complete_results).set_index('agent')
    

    #### Save the DataFrames to CSV files ####
    fine_grained_dp_task_summary.to_csv(SINGLE_DP_DP_TASK_SUCCESS_FINE_GRAINED)
    coarse_grained_dp_task_summary.to_csv(SINGLE_DP_DP_TASK_SUCCESS_COARSE_GRAINED)
    general_dp_task_summary.to_csv(SINGLE_DP_DP_TASK_SUCCESS_GENERAL)
    fine_grained_dp_task_summary.to_csv(SINGLE_DP_TASK_SUCCESS_FINE_GRAINED)
    fine_grained_task_summary.to_csv(SINGLE_DP_TASK_SUCCESS_FINE_GRAINED)
    fine_grained_dp_summary.to_csv(SINGLE_DP_DP_SUCCESS_FINE_GRAINED)
    performance_summary.to_csv(SINGLE_DP_TASK_SUCCESS)
    dp_summary.to_csv(SINGLE_DP_DP_SUCCESS)
    tc_difference.to_csv(SINGLE_DP_TC_DIFFERENCE)
    tc_relative_difference.to_csv(SINGLE_DP_TC_DIFFERENCE_RELATIVE)
    coarse_grained_dp_summary.to_csv(SINGLE_DP_DP_SUCCESS_COARSE_GRAINED)
    dps_by_category_summary.to_csv(SINGLE_DP_DP_ATTRIBUTE)
    dps_by_category_task_complete_only_summary.to_csv(SINGLE_DP_DP_ATTRIBUTE_TASK_COMPLETE_ONLY)
    filtered_df.to_csv("./raw_df/single_dp.csv")

    single_dp_dfs = {
        "all": filtered_df,
        "fine_grained_ts_summary": fine_grained_dp_task_summary,
        "coarse_grained_ts_summary": coarse_grained_dp_task_summary,
        "general_ts_summary": general_dp_task_summary,
        "fine_grained_tc_summary": fine_grained_task_summary,
        "fine_grained_dps_summary": fine_grained_dp_summary,
        "general_tc_summary": performance_summary,
        "general_dps_summary": dp_summary,
        "difference_in_tc_summary": tc_difference,
        "coarse_grained_dps_summary": coarse_grained_dp_summary,
        "dps_by_category_summary": dps_by_category_summary,
        "dps_by_category_task_complete_only_summary": dps_by_category_task_complete_only_summary
    }

    ####### GRAPHS AND VISUALIZATIONS #######
    plt.figure(figsize=(6,3))
    plt.bar(performance_summary['Agent'], performance_summary['Overall'], color = 'grey', edgecolor = 'black')
    plt.xlabel("Agent", fontsize=14)
    plt.ylabel("Success Rate (%)", fontsize=14)
    plt.title("Task Success Rate With One Dark Pattern Enabled", fontsize=16)
    plt.xticks(fontsize=12, rotation=45)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', color='lightgray', linewidth=0.5)
    plt.savefig('graphs/single/eval_tsr_1dp.pdf', dpi=300, bbox_inches='tight')

    plt.figure(figsize=(6,3))
    plt.bar(dp_summary['Agent'], dp_summary['Overall'], color = '#377eb8', edgecolor = 'black', zorder=3)
    # plt.xlabel("Agent")
    plt.ylabel("Susceptibility Rate (%)")
    # plt.title("Dark Pattern Susceptibility Rate With One Dark Pattern Enabled", fontsize=16)
    plt.xticks(rotation=0, fontsize=7)
    plt.yticks()
    plt.grid(axis='y', linestyle='--', color='lightgray', linewidth=0.5)
    plt.savefig('graphs/single/eval_dpsr_1dp.pdf', dpi=300, bbox_inches='tight')

    # plt.figure(figsize=(6,3))
    # plt.bar(dp_summary['Agent'], dp_summary['Overall'], color = '#377eb8', edgecolor = 'black', zorder=3)
    # # plt.xlabel("Agent")
    # plt.ylabel("Susceptibility Rate (%)")
    # # plt.title("Dark Pattern Susceptibility Rate With One Dark Pattern Enabled", fontsize=16)
    # # plt.xticks(rotation=45, fontsize=8)
    # plt.xticks(ticks=range(len(dp_summary['Agent'])), labels=['1', '2', '3', '4', '5', '6'], fontsize=8)
    # plt.yticks()
    # plt.grid(axis='y', linestyle='--', color='lightgray', linewidth=0.5)
    # plt.savefig('graphs/single/eval_dpsr_1dp.pdf', dpi=300, bbox_inches='tight')
    # # Add the legend at the bottom

    plt.figure(figsize=(6,3))
    plt.bar(tc_difference['Agent'], tc_difference['Overall'], color = 'grey', edgecolor = 'black')
    plt.xlabel("Agent", fontsize=14)
    plt.ylabel("Relative Change in Success Rate(%)", fontsize=14)
    plt.title("Change in Task Success Between No vs One Dark Pattern", fontsize=16)
    plt.xticks(fontsize=12, rotation=45)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', color='lightgray', linewidth=0.5)
    plt.savefig('graphs/single/eval_tsr_difference_1dp.pdf', dpi=300, bbox_inches='tight')

    ####### CHI SQUARE HEAT MAP #######
    chi2, p, dof, expected = chi2_contingency(general_dp_task_summary)
    # print(expected)
    # Calculate standardized residuals
    observed = general_dp_task_summary.values
    residuals = (observed - expected) / np.sqrt(expected)

    # Create combined annotation labels
    percentage_values = general_dp_task_summary.values
    annot_labels = pd.DataFrame(
        [[f"{resid:.2f}\n({perc:.1f}%)" for resid, perc in zip(res_row, perc_row)] 
        for res_row, perc_row in zip(residuals, percentage_values)],
        index=general_dp_task_summary.index,
        columns=general_dp_task_summary.columns
    )

    # Create DataFrame for residuals with labels
    residual_df = pd.DataFrame(residuals, 
                            index=general_dp_task_summary.index,
                            columns=general_dp_task_summary.columns)

    # Create heatmap
    plt.figure(figsize=(10, 6))
    ax = sns.heatmap(residual_df, 
                    annot=annot_labels, 
                    fmt="",
                    cmap='coolwarm',
                    center=0,
                    linewidths=.5,
                    annot_kws={"size": 10, "va": "center"})

    # ax.set_title('Standardized Chi-Square Residuals Heatmap', pad=20, fontsize=14)
    ax.set_xlabel('Task-Deception Outcome')
    ax.set_ylabel('')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.savefig('graphs/single/eval_cm_residuals_1dp.pdf', dpi=300, bbox_inches='tight')



    ###### TSR COMPARISON BAR GRAPH ######
    # Example: Two DataFrames with the same categories

    df1 = performance_summary.copy()
    df2 = benign_dfs['general_tc_summary'].copy()
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.grid(axis='y', linestyle='--', color='lightgray', linewidth=0.5)

    # Define width of bars and positions
    bar_width = 0.35
    x = np.arange(len(df1['Agent']))

    # Create short labels for x-axis
    short_labels = ['A', 'B', 'C', 'D', 'E', 'F']

    # Create the bars with different colors
    bars1 = ax.bar(x + bar_width/2, df1['Overall'], bar_width, 
                color='#377eb8', edgecolor='black', label='One Dark Pattern', zorder=3)
    bars2 = ax.bar(x - bar_width/2, df2['Overall'], bar_width,  
                color='#e41a1c', edgecolor='black', label='No Dark Pattern', zorder=3)  # Darker green

    # Add labels and title
    # ax.set_xlabel('Agents', fontsize=12)
    ax.set_ylabel('Task Success Rate (%)', fontsize=12)
    # ax.set_title('Task Success Rate One vs No Dark Pattern', fontsize=14)
    ax.set_title('')
    ax.set_xticks(x, labels=['1', '2', '3', '4', '5', '6'],)
    ax.set_xticklabels(df1['Agent'], fontsize=12)  # Use agent names for labels
    # ax.set_xticklabels(short_labels)

    # Add the metric type legend (for bar colors)
    metric_legend = ax.legend(loc='upper right', title="Metrics")

    # # Create a custom legend for category mapping (long names)
    # category_patches = []
    # for i, category in enumerate(df1['Agent']):
    #     category_patches.append(mpatches.Patch(color='gray', alpha=0.7, label=f"{short_labels[i]}: {category}"))

    # # Add the category legend at the bottom
    # category_legend = plt.legend(handles=category_patches, loc='upper center', 
    #                             bbox_to_anchor=(0.5, -0.15), ncol=3, title="")

    # Add the first legend back (metrics legend)
    ax.add_artist(metric_legend)

    # Adjust layout to fit both legends
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.3)  # Make room for the bottom legend

    plt.savefig('graphs/single/eval_tsr_comparison_1dp.pdf', dpi=300, bbox_inches='tight')
    
    ###### DPSR AND TSR COMPARISON BAR GRAPH ######
    # Example: Two DataFrames with the same categories

    df1 = performance_summary.copy()
    df2 = dp_summary.copy()

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.grid(axis='y', linestyle='--', color='lightgray', linewidth=0.5)
    
    # Define width of bars and positions
    bar_width = 0.35
    x = np.arange(len(df1['Agent']))

    # Create the bars with different colors
    bars1 = ax.bar(x + bar_width/2, df1['Overall'], bar_width, 
                color='#377eb8', edgecolor='black', label='Dark Pattern Susceptibility', zorder=3)
    bars2 = ax.bar(x - bar_width/2, df2['Overall'], bar_width,  
                color='#e41a1c', edgecolor='black', label='Task Success Rate', zorder=3)  # Darker green

    # Add labels and title
    # ax.set_xlabel('Agents', fontsize=12)
    ax.set_ylabel('Success/Susceptibility Rates', fontsize=12)
    # ax.set_title('Task Success Rate One vs No Dark Pattern', fontsize=14)
    ax.set_title('')
    ax.set_xticks(x)
    ax.set_xticklabels(df1['Agent'], rotation=45, ha='right', fontsize=12)  # Use agent names for labels
    # ax.set_xticklabels(short_labels)

    # Add the metric type legend (for bar colors)
    metric_legend = ax.legend(loc='upper right', title="Metrics")
    ax.add_artist(metric_legend)

    # Adjust layout to fit both legends
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.3)  # Make room for the bottom legend

    plt.savefig('graphs/single/eval_tsr_dpsr_1dp.png', dpi=300, bbox_inches='tight')

    return single_dp_dfs
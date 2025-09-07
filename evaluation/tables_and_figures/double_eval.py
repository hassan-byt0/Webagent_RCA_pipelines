import pandas as pd
import numpy as np

DOUBLE_DP_DP_SUCCESS_COARSE_GRAINED = "./tables/double/dpsr_individual-2dp-coarse.csv"
DOUBLE_DP_DP_SUCCESS_DIFFERENCE_COARSE_GRAINED = "./tables/double/dpsr_difference-2dp-coarse.csv"
DOUBLE_DP_TASK_SUCCESS_FINE_GRAINED = "./tables/double/tsr-2dp-fine.csv"
DOUBLE_DP_TASK_SUCCESS_COARSE_GRAINED = "./tables/double/tsr-2dp-coarse.csv"
DOUBLE_DP_TASK_SUCCESS_DIFFERENCE_BENIGN_COARSE_GRAINED = "./tables/double/tsr_difference_benign-2dp-coarse.csv"
DOUBLE_DP_TASK_SUCCESS_DIFFERENCE_SINGLE_COARSE_GRAINED = "./tables/double/tsr_difference_single-2dp-coarse.csv"
DOUBLE_DP_NUM_DPS_FELL_FOR_COARSE_GRAINED = "./tables/double/num_dps_fell_for-2dp-coarse.csv"
DOUBLE_DP_NUM_DPS_FELL_FOR_GENERAL = "./tables/double/num_dps_fell_for-2dp-general.csv"
DOUBLE_DP_DP_PAIR_NUM_SUSCEPTIBLE_COARSE = "./tables/double/dp_pair_num_susceptible-2dp-coarse.csv"
DOUBLE_DP_DP_PAIR_TASK_SUCCESS_COARSE = "./tables/double/dp_pair_task_success_rate-2dp-coarse.csv"
DOUBLE_DP_CM_FINE_GRAINED = "./tables/double/cm-2dp-fine.csv"
DOUBLE_DP_CM_COARSE_GRAINED = "./tables/double/cm-2dp-coarse.csv"
DOUBLE_DP_CM_GENERAL = "./tables/double/cm-2dp-general.csv"
DOUBLE_DP_CM_DIFFERENCE_FINE_GRAINED = "./tables/double/cm_difference-2dp-fine.csv"
DOUBLE_DP_CM_DIFFERENCE_COARSE_GRAINED = "./tables/double/cm_difference-2dp-coarse.csv"
DOUBLE_DP_CM_DIFFERENCE_GENERAL = "./tables/double/cm_difference-2dp-general.csv"
DOUBLE_DP_DPSR_DIFFERENCE_RELATIVE = "./tables/double/dpsr_difference_relative-2dp-coarse.csv"

######################################################################################################
###### DOUBLE

def double_data_eval(full_agent_data, epsilon):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(full_agent_data)

    # Filter rows where dp1 and dp2 is not empty, but dp3 and dp4 are empty
    filtered_df = df[df['dp1'].notnull() & (df['dp1'] != '') &
                 (df['dp2'].notnull() & (df['dp2'] != '')) &
                 (df['dp3'].isna() | (df['dp3'] == '')) &
                 (df['dp4'].isna() | (df['dp4'] == ''))].copy()
    
    filtered_df['site_name'] = df['site'].apply(lambda x: x.split('/')[1].split('?')[0] if isinstance(x, str) and '/' in x else x)
    filtered_df['scenario'] = filtered_df['site_name'] + ":" + filtered_df['dp1'] + ":" + filtered_df['dp2'] + ":" + filtered_df['prompt']
    filtered_df['dp1_key'] = filtered_df['site_name'] + "_" + filtered_df['dp1']
    filtered_df['dp2_key'] = filtered_df['site_name'] + "_" + filtered_df['dp2']

    # Define conditions for the new column
    dp1_conditions = [
        (filtered_df['task_correct'] == True) & (filtered_df['dp1_susceptibility'] == True),
        (filtered_df['task_correct'] == True) & (filtered_df['dp1_susceptibility'] == False),
        (filtered_df['task_correct'] == False) & (filtered_df['dp1_susceptibility'] == True),
        (filtered_df['task_correct'] == False) & (filtered_df['dp1_susceptibility'] == False)
    ]

    # Define corresponding values for each condition
    dp1_choices = ['DC', 'EC', 'DF', 'EF']

    # Create the new column using np.select
    filtered_df['dp1_type'] = np.select(dp1_conditions, dp1_choices, default=None)

        # Define conditions for the new column
    dp2_conditions = [
        (filtered_df['task_correct'] == True) & (filtered_df['dp2_susceptibility'] == True),
        (filtered_df['task_correct'] == True) & (filtered_df['dp2_susceptibility'] == False),
        (filtered_df['task_correct'] == False) & (filtered_df['dp2_susceptibility'] == True),
        (filtered_df['task_correct'] == False) & (filtered_df['dp2_susceptibility'] == False)
    ]

    # Define corresponding values for each condition
    dp2_choices = ['DC', 'EC', 'DF', 'EF']

    # Create the new column using np.select
    filtered_df['dp2_type'] = np.select(dp2_conditions, dp2_choices, default=None)

    # Define conditions for the new column
    num_susceptible_conditions = [
        (filtered_df['dp1_susceptibility'] == False) & (filtered_df['dp2_susceptibility'] == False),  # Both False → 0
        (filtered_df['dp1_susceptibility'] != filtered_df['dp2_susceptibility']),                     # One True → 1
        (filtered_df['dp1_susceptibility'] == True) & (filtered_df['dp2_susceptibility'] == True)     # Both True → 2
    ]

    # Assign corresponding numerical values
    choices = [0, 1, 2]

    # Create new column using vectorized operation
    filtered_df['num_susceptible'] = np.select(num_susceptible_conditions, choices, default=None)

    # Create a new column with alphabetically sorted values from dp1 and dp2
    filtered_df['dp_combined'] = filtered_df[['dp1', 'dp2']].apply(lambda x: '_'.join(sorted(x)), axis=1)
    
    filtered_df = filtered_df[['agent', 'site_name', 'scenario', 'prompt', 'dp1', 'dp2', 'dp1_key', 'dp2_key', 'task_correct', 
                               'dp1_susceptibility', 'dp2_susceptibility', 'dp1_type', 'dp2_type', 'num_susceptible', 'dp_combined']]

    # Need to exclude the other experiments (attribute changes, and postscripts)
    # exclude postscripts experiments:
    with open('postscripts.txt', 'r') as file:
        exclude_prompts = [line.strip() for line in file]
    # Filter the dataframe to exclude rows where 'prompts' column value is in the exclude_prompts list
    filtered_df = filtered_df[~filtered_df['prompt'].isin(exclude_prompts)]

    # exclude attribute changes experiments:
    attribute_change_codes = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
    filtered_df = filtered_df[~filtered_df['dp1'].isin(attribute_change_codes)]
    filtered_df = filtered_df[~filtered_df['dp2'].isin(attribute_change_codes)]

    agent_mapping = {
    'visualwebarena': 'VisualWebArena',
    'skyvern': 'Skyvern',
    'agente': 'Agent-E',
    'dobrowser': 'DoBrowser',
    'browseruse': 'BrowserUse',
    'webarena': 'WebArena',
    }

    filtered_df['agent'] = filtered_df['agent'].replace(agent_mapping)

    ###### TABLE GENERATION FOR SUSCEPTIBILITY RATE OF INDIVIDUAL DPS
    # Extract Unique dark patterns from the filtered DP
    dark_patterns = pd.concat([filtered_df['dp1_key'], filtered_df['dp2_key']]).unique()
    results = []
    for agent in filtered_df['agent'].unique():
        for dp in dark_patterns:
            encounters = ((filtered_df['agent'] == agent) & ((filtered_df['dp1_key'] == dp) | (filtered_df['dp2_key'] == dp))).sum()
            susceptible = ((filtered_df['agent'] == agent) & 
                        (((filtered_df['dp1_key'] == dp) & filtered_df['dp1_susceptibility']) | 
                            ((filtered_df['dp2_key'] == dp) & filtered_df['dp2_susceptibility']))).sum()
            rate = np.round((susceptible / encounters) * 100, 1) if encounters > 0 else None
            results.append({'Agent': agent, 'dp': dp, 'Susceptibility Rate': rate})

    susceptibility_df = pd.DataFrame(results)
    susceptibility_df = susceptibility_df.pivot(index = 'Agent', columns='dp', values="Susceptibility Rate")
    susceptibility_df = susceptibility_df.reset_index().rename_axis(None, axis=1)

    ###### TABLE GENERATION FOR SUSCEPTIBILITY DIFFERENCE

    # Brief explanation: We are trying to compare the susceptibility rates of the same dp between the single dp and double dp experiments.
    # You may notice that there are more single dp experiments in different prompts/scenarios than double dp experiments. 
    # To make the comparison fair, we are trying to find the rows in the single dp dataframe that match the dp1 or dp2 of the double dp dataframe under that same scenarios (agent, site, prompt).
    
    # single_susceptibility_df = single_dp_dfs['coarse_grained_dps_summary'].copy()
    # single_df = single_dp_dfs['all'].copy()
    single_df = pd.read_csv('./raw_df/single_dp.csv')
    single_df_matching = single_df[single_df.apply(
        lambda row: any(
            row['agent'] == double_row['agent'] and
            row['prompt'] == double_row['prompt'] and
            (
                row['dp1'] == double_row['dp1'] or
                row['dp1'] == double_row['dp2']
            )
            for _, double_row in filtered_df.iterrows()
        ), axis=1
    )]
    
    # Now just doing the same thing for the benign
    # benign = benign_dfs['all'].copy()
    benign = pd.read_csv('./raw_df/no_dp.csv')
    benign_matching = benign[benign.apply(
        lambda row: any(
            row['agent'] == double_row['agent'] and
            row['prompt'] == double_row['prompt']
            for _, double_row in filtered_df.iterrows()
        ), axis=1
    )]
    # benign_matching.to_csv('./test/benign_matching.csv')

    single_susceptibility_df = single_df_matching.groupby(['agent', 'dp1_key'])['dp1_susceptibility'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    single_susceptibility_df = single_susceptibility_df.pivot(index='agent', columns='dp1_key', values='dp1_susceptibility')
    single_susceptibility_df['Overall'] = single_df_matching.groupby('agent')['dp1_susceptibility'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    single_susceptibility_df = single_susceptibility_df.reset_index()
    single_susceptibility_df = single_susceptibility_df.rename(columns={'agent': 'Agent'})
    
    # single_df_matching.to_csv("./test/single_df_matching_to_double_df.csv")
    # single_susceptibility_df.to_csv("./test/single_susceptibility_df.csv")

    merged_susceptibility = pd.merge(
        single_susceptibility_df,
        susceptibility_df,
        on="Agent",
        suffixes=('_existing', '_new'),
        how='outer'
    )

    single_dps = set(single_susceptibility_df.columns) - {'Agent'}
    double_dps = set(susceptibility_df.columns) - {'Agent'}
    shared_dps = single_dps.intersection(double_dps)
    
    susceptibility_difference = []
    for agent in merged_susceptibility['Agent']:
        row = {'Agent': agent}
        for dp in shared_dps:
            single_dp_val = merged_susceptibility.loc[merged_susceptibility['Agent'] == agent, f'{dp}_existing'].values
            double_dp_val = merged_susceptibility.loc[merged_susceptibility['Agent'] == agent, f'{dp}_new'].values

            single = single_dp_val[0] if single_dp_val.size > 0 else None
            double = double_dp_val[0] if double_dp_val.size > 0 else None
            row[dp] = double - single if single is not None and double is not None else None
        susceptibility_difference.append(row)
    susceptibility_difference_df = pd.DataFrame(susceptibility_difference)

    susceptibility_difference_relative = []
    for agent in merged_susceptibility['Agent']:
        row = {'Agent': agent}
        for dp in shared_dps:
            single_dp_val = merged_susceptibility.loc[merged_susceptibility['Agent'] == agent, f'{dp}_existing'].values
            double_dp_val = merged_susceptibility.loc[merged_susceptibility['Agent'] == agent, f'{dp}_new'].values

            #LAPLACE SMOOTHING
            single = single_dp_val[0] + epsilon
            double = double_dp_val[0] + epsilon
            # single = single_dp_val[0] if single_dp_val.size > 0 else None
            # double = double_dp_val[0] if double_dp_val.size > 0 else None
            if single is not None and double is not None:
                if single != 0:
                    row[dp] = np.round(((double - single)/single) * 100, 2)
                else:
                    row[dp] = float('inf')
            else:
                row[dp] = None
            # row[dp] = (double - single)/single if single is not None and double is not None else None
        susceptibility_difference_relative.append(row)
    susceptibility_difference_relative_df = pd.DataFrame(susceptibility_difference_relative)
    # Add 'overall' column to calculate the average of all numeric values in each row
    susceptibility_difference_relative_df['overall'] = (
        susceptibility_difference_relative_df.loc[:, susceptibility_difference_relative_df.columns != 'Agent'].mean(axis=1).round(1)
    )
    susceptibility_difference_relative_df.to_csv(DOUBLE_DP_DPSR_DIFFERENCE_RELATIVE)


    ###### TASK SCUEESS RATE FOR EACH TASK AND AGENT 
    tsr_fine_grained = filtered_df.groupby(['agent', 'scenario'])['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    tsr_fine_grained = tsr_fine_grained.pivot(index='agent', columns='scenario', values='task_correct')
    tsr_fine_grained['Overall'] = filtered_df.groupby('agent')['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    tsr_fine_grained.reset_index()
    tsr_fine_grained = tsr_fine_grained.rename(columns={'agent': 'Agent'})

    tsr_coarse_grained = filtered_df.groupby(['agent', 'site_name'])['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    tsr_coarse_grained = tsr_coarse_grained.pivot(index='agent', columns='site_name', values='task_correct')
    tsr_coarse_grained['Overall'] = filtered_df.groupby('agent')['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    tsr_coarse_grained.reset_index()
    tsr_coarse_grained = tsr_coarse_grained.rename(columns={'agent': 'Agent'})

    ###### TASK SUCCESS RATE DIFFERENCE 
    benign_tsr_coarse_grained = benign_matching.groupby(['agent', 'site_name'])['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    benign_tsr_coarse_grained = benign_tsr_coarse_grained.pivot(index='agent', columns='site_name', values='task_correct')
    benign_tsr_coarse_grained['Overall'] = benign_matching.groupby('agent')['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    benign_tsr_coarse_grained.reset_index()
    benign_tsr_coarse_grained = benign_tsr_coarse_grained.rename(columns={'agent': 'Agent'})
    # benign_tsr_coarse_grained.to_csv("./test/double/benign_tsr_coarse_grained.csv")

    single_tsr_coarse_grained = single_df_matching.groupby(['agent', 'site_name'])['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    single_tsr_coarse_grained = single_tsr_coarse_grained.pivot(index='agent', columns='site_name', values='task_correct')
    single_tsr_coarse_grained['Overall'] = single_df_matching.groupby('agent')['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    single_tsr_coarse_grained.reset_index()
    single_tsr_coarse_grained = single_tsr_coarse_grained.rename(columns={'agent': 'Agent'})
    # single_tsr_coarse_grained.to_csv("./test/double/single_tsr_coarse_grained.csv")

    columns_to_subtract = ['health', 'news', 'shop', 'spotify', 'Overall']
    tsr_difference_from_benign_coarse_grained = benign_tsr_coarse_grained.copy() 
    # print(f"These are tsr_course_grained columns: {tsr_coarse_grained.columns}")
    # print(f"These are benign_tsr_coarse_grained columns: {benign_tsr_coarse_grained}")
    tsr_difference_from_benign_coarse_grained[columns_to_subtract] = tsr_coarse_grained[columns_to_subtract] - benign_tsr_coarse_grained[columns_to_subtract]
    tsr_difference_from_benign_relative_difference = tsr_difference_from_benign_coarse_grained.copy()
    tsr_difference_from_benign_relative_difference[columns_to_subtract] = ((tsr_difference_from_benign_coarse_grained[columns_to_subtract] / benign_tsr_coarse_grained[columns_to_subtract]) * 100).round(1)
    tsr_difference_from_benign_relative_difference.to_csv('./tables/double/tsr_difference_benign_relative-2dp-coarse.csv')

    tsr_difference_from_single_coarse_grained = single_tsr_coarse_grained.copy() 
    tsr_difference_from_single_coarse_grained[columns_to_subtract] = tsr_coarse_grained[columns_to_subtract] - single_tsr_coarse_grained[columns_to_subtract]
    tsr_difference_from_single_relative_difference = tsr_difference_from_single_coarse_grained.copy()
    tsr_difference_from_single_relative_difference[columns_to_subtract] = ((tsr_difference_from_single_coarse_grained[columns_to_subtract] / single_tsr_coarse_grained[columns_to_subtract]) * 100).round(1)

    ###### NUM DPS FELL FOR COARSE ######
    # Create pivot table with all combinations
    filtered_df['site_num'] = filtered_df['site_name'] + "_" + filtered_df['num_susceptible'].astype(str)
    pivoted_num_susceptible_table_coarse = filtered_df.pivot_table(
        index='agent',
        columns='site_num',
        values='num_susceptible',
        aggfunc='count',
        fill_value=0
    )   

    # Generate all possible column combinations
    sites = filtered_df['site_name'].unique()
    nums = [0, 1, 2]
    num_susceptible_columns_coarse = [f"{site}_{num}" for site in sites for num in nums]
    pivoted_num_susceptible_table_coarse = pivoted_num_susceptible_table_coarse.reindex(columns=num_susceptible_columns_coarse, fill_value=0)

    for col in num_susceptible_columns_coarse:
        if col not in pivoted_num_susceptible_table_coarse.columns:
            pivoted_num_susceptible_table_coarse[col] = 0
    
    num_dps_fell_for_coarse = pivoted_num_susceptible_table_coarse[num_susceptible_columns_coarse].reset_index().rename(columns={'agent': 'Agent'})


    ###### NUM DPS FELL FOR GENERAL######
    num_dps_fell_for_general = (
        filtered_df.groupby(['agent', 'num_susceptible'])
        .size()
        .unstack(fill_value=0)
        .add_prefix('num_susceptible_')
        .reset_index()
        .rename(columns={'agent': 'Agent'})
    )

    for n in [0, 1, 2]:
        col = f'num_susceptible_{n}'
        if col not in num_dps_fell_for_general.columns:
            num_dps_fell_for_general[col] = 0
    
    num_dps_fell_for_general = num_dps_fell_for_general[['Agent', 'num_susceptible_0', 'num_susceptible_1', 'num_susceptible_2']]

    ###### DP PAIR SUSCEPTIBILITY RATE ######
    dp_pair_susceptibility_coarse = filtered_df.groupby(['agent', 'dp_combined'])['num_susceptible'].apply(lambda x: np.round(x.mean(), 1)).reset_index()
    dp_pair_susceptibility_coarse = dp_pair_susceptibility_coarse.pivot(index='agent', columns='dp_combined', values='num_susceptible')
    dp_pair_susceptibility_coarse['Overall'] = filtered_df.groupby('agent')['num_susceptible'].apply(lambda x: np.round(x.mean(), 1))
    dp_pair_susceptibility_coarse.reset_index()
    dp_pair_susceptibility_coarse = dp_pair_susceptibility_coarse.rename(columns={'agent': 'Agent'})
    
    ###### DP PAIR TASK SUCCESS RATE ######
    dp_pair_task_success_coarse = filtered_df.groupby(['agent', 'dp_combined'])['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    dp_pair_task_success_coarse = dp_pair_task_success_coarse.pivot(index='agent', columns='dp_combined', values='task_correct')
    dp_pair_task_success_coarse['Overall'] = filtered_df.groupby('agent')['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    dp_pair_task_success_coarse.reset_index()
    dp_pair_task_success_coarse = dp_pair_task_success_coarse.rename(columns={'agent': 'Agent'})

    ###### CONFUSION MATRIX DC, EC, DF, EF ######
    # Create two versions of the DataFrame
    dp1_df = (
        filtered_df.drop(columns=['dp2', 'dp2_susceptibility'])
        .rename(columns={'dp1': 'dp', 'dp1_susceptibility': 'dp_susceptibility'})
    )

    dp2_df = (
        filtered_df.drop(columns=['dp1', 'dp1_susceptibility'])
        .rename(columns={'dp2': 'dp', 'dp2_susceptibility': 'dp_susceptibility'})
    )

    # Combine vertically and reset index
    cm_df = pd.concat([dp1_df, dp2_df], ignore_index=True)

    # Define conditions for the new column
    conditions = [
        (cm_df['task_correct'] == True) & (cm_df['dp_susceptibility'] == True),
        (cm_df['task_correct'] == True) & (cm_df['dp_susceptibility'] == False),
        (cm_df['task_correct'] == False) & (cm_df['dp_susceptibility'] == True),
        (cm_df['task_correct'] == False) & (cm_df['dp_susceptibility'] == False)
    ]

    # Define corresponding values for each condition
    choices = ['DC', 'EC', 'DF', 'EF']

    # Create the new column using np.select
    cm_df['type'] = np.select(conditions, choices, default=None)

    fine_grained_cm = cm_df.groupby(['agent', 'dp', 'type']).size().reset_index(name='count')
    fine_grained_cm = fine_grained_cm.pivot(index=['agent', 'dp'], columns='type', values='count').fillna(0)
    fine_grained_cm = fine_grained_cm.div(fine_grained_cm.sum(axis=1), axis=0) * 100
    fine_grained_cm = fine_grained_cm.round(1)
    fine_grained_cm.reset_index(inplace=True)

    coarse_grained_cm = cm_df.groupby(['agent', 'site_name', 'type']).size().reset_index(name='count')
    coarse_grained_cm = coarse_grained_cm.pivot(index=['agent', 'site_name'], columns='type', values='count').fillna(0)
    coarse_grained_cm = coarse_grained_cm.div(coarse_grained_cm.sum(axis=1), axis=0) * 100
    coarse_grained_cm = coarse_grained_cm.round(1)
    coarse_grained_cm.reset_index(inplace=True)
    
    general_cm = cm_df.groupby(['agent', 'type']).size().reset_index(name='count')
    general_cm = general_cm.pivot(index=['agent'], columns='type', values='count').fillna(0)
    general_cm = general_cm.div(general_cm.sum(axis=1), axis=0) * 100
    general_cm = general_cm.round(1)
    general_cm.reset_index(inplace=True)

    ###### CONFUSION MATRIX DIFFERENCES ######
    
    ## FIRST, WE HAVE TO GET THE CONFUSION MATRICES, BUT ONLY FROM THE MATCHING DF
    single_fine_grained_cm = single_df_matching.groupby(['agent', 'dp1', 'type']).size().reset_index(name='count')
    single_fine_grained_cm = single_fine_grained_cm.rename(columns={'dp1': 'dp'})
    single_fine_grained_cm = single_fine_grained_cm.pivot(index=['agent', 'dp'], columns='type', values='count').fillna(0)
    single_fine_grained_cm = single_fine_grained_cm.div(single_fine_grained_cm.sum(axis=1), axis=0) * 100
    single_fine_grained_cm = single_fine_grained_cm.round(1)
    single_fine_grained_cm.reset_index(inplace=True)
    # single_fine_grained_cm.to_csv("./test/double/single_fine_grained_cm.csv")

    single_coarse_grained_cm = single_df_matching.groupby(['agent', 'site_name', 'type']).size().reset_index(name='count')
    single_coarse_grained_cm = single_coarse_grained_cm.pivot(index=['agent', 'site_name'], columns='type', values='count').fillna(0)
    single_coarse_grained_cm = single_coarse_grained_cm.div(single_coarse_grained_cm.sum(axis=1), axis=0) * 100
    single_coarse_grained_cm = single_coarse_grained_cm.round(1)
    single_coarse_grained_cm.reset_index(inplace=True)
    # single_coarse_grained_cm.to_csv("./test/double/single_coarse_grained_cm.csv")
    
    single_general_cm = single_df_matching.groupby(['agent', 'type']).size().reset_index(name='count')
    single_general_cm = single_general_cm.pivot(index=['agent'], columns='type', values='count').fillna(0)
    single_general_cm = single_general_cm.div(single_general_cm.sum(axis=1), axis=0) * 100
    single_general_cm = single_general_cm.round(1)
    single_general_cm.reset_index(inplace=True)
    # single_general_cm.to_csv("./test/double/single_general_cm.csv")

    # Now we can calculate the differences
    cm_columns_to_subtract = ['DC', 'EC', 'DF', 'EF']

    fine_grained_cm.set_index(['agent', 'dp'], inplace=True)
    single_fine_grained_cm.set_index(['agent', 'dp'], inplace=True)
    aligned_fine_grained_cm, aligned_single_fine_grained_cm = fine_grained_cm.align(single_fine_grained_cm)
    fine_grained_cm_difference = aligned_fine_grained_cm[cm_columns_to_subtract] - aligned_single_fine_grained_cm[cm_columns_to_subtract]
    fine_grained_cm_difference.reset_index(inplace=True)
    
    coarse_grained_cm.set_index(['agent', 'site_name'], inplace=True)
    single_coarse_grained_cm.set_index(['agent', 'site_name'], inplace=True)
    aligned_coarse_grained_cm, aligned_single_coarse_grained_cm = coarse_grained_cm.align(single_coarse_grained_cm)
    coarse_grained_cm_difference = aligned_coarse_grained_cm[cm_columns_to_subtract] - aligned_single_coarse_grained_cm[cm_columns_to_subtract]
    coarse_grained_cm_difference.reset_index(inplace=True)
    
    general_cm.set_index(['agent'], inplace=True)
    single_general_cm.set_index(['agent'], inplace=True)
    aligned_general_cm, aligned_single_general_cm = general_cm.align(single_general_cm)
    general_cm_difference = aligned_general_cm[cm_columns_to_subtract] - aligned_single_general_cm[cm_columns_to_subtract]
    general_cm_difference.reset_index(inplace=True)

    ##### Save the DataFrames to CSV files ####
    susceptibility_df.to_csv(DOUBLE_DP_DP_SUCCESS_COARSE_GRAINED)
    susceptibility_difference_df.to_csv(DOUBLE_DP_DP_SUCCESS_DIFFERENCE_COARSE_GRAINED)
    tsr_fine_grained.to_csv(DOUBLE_DP_TASK_SUCCESS_FINE_GRAINED)
    tsr_coarse_grained.to_csv(DOUBLE_DP_TASK_SUCCESS_COARSE_GRAINED)
    tsr_difference_from_benign_coarse_grained.to_csv(DOUBLE_DP_TASK_SUCCESS_DIFFERENCE_BENIGN_COARSE_GRAINED)
    tsr_difference_from_single_coarse_grained.to_csv(DOUBLE_DP_TASK_SUCCESS_DIFFERENCE_SINGLE_COARSE_GRAINED)
    num_dps_fell_for_coarse.to_csv(DOUBLE_DP_NUM_DPS_FELL_FOR_COARSE_GRAINED)
    num_dps_fell_for_general.to_csv(DOUBLE_DP_NUM_DPS_FELL_FOR_GENERAL)
    dp_pair_susceptibility_coarse.to_csv(DOUBLE_DP_DP_PAIR_NUM_SUSCEPTIBLE_COARSE)
    dp_pair_task_success_coarse.to_csv(DOUBLE_DP_DP_PAIR_TASK_SUCCESS_COARSE)
    fine_grained_cm.to_csv(DOUBLE_DP_CM_FINE_GRAINED)
    coarse_grained_cm.to_csv(DOUBLE_DP_CM_COARSE_GRAINED)
    general_cm.to_csv(DOUBLE_DP_CM_GENERAL)
    fine_grained_cm_difference.to_csv(DOUBLE_DP_CM_DIFFERENCE_FINE_GRAINED)
    coarse_grained_cm_difference.to_csv(DOUBLE_DP_CM_DIFFERENCE_COARSE_GRAINED)
    general_cm_difference.to_csv(DOUBLE_DP_CM_DIFFERENCE_GENERAL)
    # merged_susceptibility.to_csv("./test/merged.csv")
    filtered_df.to_csv('./raw_df/double_dp.csv')

    double_dp_dfs = {
        "all": filtered_df,
        "coarse_grained_dpsr": susceptibility_df,
        "coarse_grained_dpsr_difference": susceptibility_difference_df,
        "fine_grained_tsr": tsr_fine_grained,
        "coarse_grained_tsr": tsr_coarse_grained,
        "benign_tsr_difference": tsr_difference_from_benign_coarse_grained,
        "single_tsr_difference": tsr_difference_from_single_coarse_grained,
        "coarse_grained_num_dps_fell": num_dps_fell_for_coarse,
        "general_num_dps_fell": num_dps_fell_for_general,
        "coarse_dp_pair_dpsr": dp_pair_susceptibility_coarse,
        "coarse_dp_pair_tsr": dp_pair_task_success_coarse,
        "fine_grained_cm": fine_grained_cm,
        "coarse_grained_cm": coarse_grained_cm,
        "general_cm": general_cm,
        "fine_grained_cm_difference": fine_grained_cm_difference,
        "coarse_grained_cm_difference": coarse_grained_cm_difference,
        "general_cm_difference": general_cm_difference,
    }

    return double_dp_dfs
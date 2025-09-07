import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BENIGN_SUCCESS_RATE = "./tables/benign/tsr-0dp-coarse.csv"
BENIGN_TASK_SUCCESS_FINE_GRAINED = "./tables/benign/tsr-0dp-fine.csv"

def benign_data_eval(full_agent_data):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(full_agent_data)

    # Filter rows where dp1, dp2, dp3, and dp4 are empty
    filtered_df = df[(df['dp1'].isna() | (df['dp1'] == '')) &
                     (df['dp2'].isna() | (df['dp2'] == '')) &
                     (df['dp3'].isna() | (df['dp3'] == '')) &
                     (df['dp4'].isna() | (df['dp4'] == ''))].copy()

    filtered_df['site_name'] = df['site'].apply(lambda x: x.split('/')[1] if isinstance(x, str) and '/' in x else x)
    filtered_df['scenario'] = filtered_df['site_name'] + ":" + filtered_df['prompt']
    filtered_df = filtered_df[['agent', 'site_name', 'scenario', 'prompt', 'task_correct']]
    
    # exclude vision ablation study experiments
    excluded_agents = ['browseruse_vis', 'dobrowser_novis']
    filtered_df = filtered_df[~filtered_df['agent'].isin(excluded_agents)]

    agent_mapping = {
    'visualwebarena': 'VisualWebArena',
    'skyvern': 'Skyvern',
    'agente': 'Agent-E',
    'dobrowser': 'DoBrowser',
    'browseruse': 'BrowserUse',
    'webarena': 'WebArena',
    }

    filtered_df['agent'] = filtered_df['agent'].replace(agent_mapping)

    performance_summary = filtered_df.groupby(['agent', 'site_name'])['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    performance_summary = performance_summary.pivot(index='agent', columns='site_name', values='task_correct')
    performance_summary['Overall'] = filtered_df.groupby('agent')['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    performance_summary = performance_summary.reset_index()
    performance_summary = performance_summary.rename(columns={'agent': 'Agent'})

    fine_grained_summary = filtered_df.groupby(['agent', 'scenario'])['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1)).reset_index()
    fine_grained_summary = fine_grained_summary.pivot(index='agent', columns='scenario', values='task_correct')
    fine_grained_summary['Overall'] = filtered_df.groupby('agent')['task_correct'].apply(lambda x: np.round((x == True).mean() * 100, 1))
    fine_grained_summary.reset_index()
    fine_grained_summary = fine_grained_summary.rename(columns={'agent': 'Agent'})
    
    performance_summary.to_csv(BENIGN_SUCCESS_RATE)
    fine_grained_summary.to_csv(BENIGN_TASK_SUCCESS_FINE_GRAINED)
    filtered_df.to_csv('./raw_df/no_dp.csv')

    benign_dfs = {
        "all": filtered_df,
        "fine_grained_tc_summary": fine_grained_summary,
        "general_tc_summary": performance_summary
    }

    plt.figure(figsize=(6,3))
    plt.bar(performance_summary['Agent'], performance_summary['Overall'], color = 'grey', edgecolor = 'black')
    plt.xlabel("Agent")
    plt.ylabel("Success Rate (%)")
    plt.title("Task Success Rate With One Dark Pattern Enabled")
    plt.xticks(rotation=45)
    plt.yticks()
    plt.savefig('graphs/benign/eval_tsr_0dp.pdf', dpi=300, bbox_inches='tight')
    return benign_dfs
from baseline_eval import benign_data_eval
from single_eval import single_data_eval
from double_eval import double_data_eval
from triple_eval import triple_data_eval
from quad_eval import quad_data_eval
from mult_figs import generate_mult_graphs_dpsr_new, generate_mult_graphs_tsr
import os

VALIDATION_RESULTS_CSV = "../../numbers/custom_comparison_results.csv"
EPSILON = 0.5

def create_folders():

    subfolders_1 = ['benign', 'single', 'double', 'triple', 'quad']
    subfolders_2 = ['benign', 'single', 'mult']
    

    if not os.path.exists('tables'):
        os.mkdir('tables')
    
    if not os.path.exists('graphs'):
        os.mkdir('graphs')
    
    if not os.path.exists('raw_df'):
        os.mkdir('raw_df')
    
    # Check and create subfolders
    for subfolder in subfolders_1:
        path = os.path.join('tables', subfolder)
        if not os.path.exists(path):
            os.mkdir(path)
    
    for subfolder in subfolders_2:
        path = os.path.join('graphs', subfolder)
        if not os.path.exists(path):
            os.mkdir(path)

def main():
    create_folders()
    benign_data = benign_data_eval(VALIDATION_RESULTS_CSV)
    single_data = single_data_eval(VALIDATION_RESULTS_CSV, benign_data)
    double_data = double_data_eval(VALIDATION_RESULTS_CSV, EPSILON)
    triple_data = triple_data_eval(VALIDATION_RESULTS_CSV, EPSILON, benign_data, single_data)
    quad_data = quad_data_eval(VALIDATION_RESULTS_CSV, EPSILON, benign_data, single_data)
    generate_mult_graphs_tsr()
    generate_mult_graphs_dpsr_new()
    

if __name__ == "__main__":
    main()
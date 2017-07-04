__author__ = 'jnejati'
import prepare_datasets
import learning_algos
import numpy as np

def main():

    comp_time_array, download_time_array = prepare_datasets.prepare_dataset('./data/orig', './data/modified')
    np.set_printoptions(suppress=True)
    #print(comp_time_array[:,:2], comp_time_array[:,2])
    #my_le = learning_algos.LearningAlgorithms(comp_time_array[:, :2], comp_time_array[:, 2])
    my_le = learning_algos.LearningAlgorithms(download_time_array[:, :2], download_time_array[:, 2])

    my_le.linear_regression()

if __name__ == '__main__':
    main()

from matplotlib.pyplot import plot, show

from algorithms.neuralnetwork.feedforward.PredictionNNFactory import \
    PredictionNNFactory
from datahandler.numerical.NumericalDataHandler import NumericalDataHandler
from datahandler.numerical.NumericalDataProcessor import NumericalDataProcessor
from engine.constants.run_type import HADOOP, LOCAL, INLINE
from engine.engine import Engine
import numpy as np
from validator.PredictionValidator import PredictionValidator


if __name__ == '__main__':
    
    
    print("=== Neural Network Prediction Example ===")
    
    nr_params = 11
    nr_label_dim = 1
    arr_layer_sizes = [ nr_params, 5, nr_label_dim ]
    iterations = 100
    run_type = LOCAL
    data_file = 'hdfs:///user/linda/ml/data/winequality-red.csv' if run_type == HADOOP else '../data/wine-quality/winequality-red.csv'
    input_scalling = NumericalDataProcessor.STANDARDIZE
    target_scalling = None
    
    print(  "\n             data: " + data_file
          + "\n           params: " + str(nr_params)
          + "\n        label dim: " + str(nr_label_dim)
          + "\n           layers: " + str(arr_layer_sizes)
          + "\n       iterations: " + str(iterations)
          + "\n         run type: " + run_type
          + "\n   input scalling: " + str(input_scalling)
          + "\n  target scalling: " + str(target_scalling)
          + "\n"
          )
    
    # 1. define algorithm
    pred_nn = PredictionNNFactory(arr_layer_sizes, iterations)
    
    # 2. set data handler (pre-processing, normalization, data set creation)
    data_handler = NumericalDataHandler(nr_params, nr_label_dim, input_scalling=input_scalling, target_scalling=target_scalling)
    
    # 3. run
    engine = Engine(pred_nn, data_file, data_handler=data_handler)
    trained_alg = engine.start(_run_type=run_type)
    
    # 4. validate result
    validation_stats = engine.validate(trained_alg, PredictionValidator(), _run_type=run_type)
    targets = np.array(validation_stats['targets'])
    pred = np.array(validation_stats['pred'])
    plot(targets, 'go')
    plot(pred, 'r+')
    show()
    
    data_processor = data_handler.get_data_processor()
    data_processor.set_data(np.array([[7.4, 0.7, 0 , 1.9, 0.076, 11, 34, 0.9978, 3.51, 0.56, 9.4, 5]]))
    data_processor.normalize_data(data_handler.get_statistics())
    test_set = data_processor.get_data_set()
    pred = trained_alg.predict(test_set)
    
    print(pred)
    print(test_set.targets)

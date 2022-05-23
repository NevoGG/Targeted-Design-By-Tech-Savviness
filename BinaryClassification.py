import numpy as np
import pandas as pd


# def load_data(csv_dir):
#     data = pd.read_csv(csv_dir, header=None)
#     print(data)
#
#     # # make the dataset linearly separable
#     # data = data[:100]
#     # data[4] = np.where(data.iloc[:, -1] == 'Iris-setosa', 0, 1)
#     data = np.asmatrix(data, dtype='float64')


class Perceptron(object):

    def __init__(self, no_of_inputs, epochs=1, learning_rate=0.01):
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.weights = np.zeros(no_of_inputs + 1)


        """
        :param vector: an array of nums, same length as weight array
        :return: classification of vector, 0 or 1.
        """
    def predict(self, vector):
        summation = np.dot(vector, self.weights[1:]) + self.weights[0]
        if summation > 0:
            activation = 1
        else:
            activation = 0
        return activation

    """
    :param df: a pd dataframe, same num of cols as weights vector. last col is classification mark.
    :updates weights vector according to trained data 
    """
    def train(self, df):
        num_of_rows = df.shape[0] # num of input rows? todo: verify
        print("num of rows: ", num_of_rows)
        for i in range(self.epochs): # num of times we run the whole db
            for j in range(0, num_of_rows):
                vector_data = df.iloc[j].to_numpy()
                vector = vector_data[:-1] # excluding label
                label = vector_data[-1]  # last col is the label.
                prediction = self.predict(vector)
                self.weights[1:] += self.learning_rate * (
                            label - prediction) * vector  # if label not prediction, update
                self.weights[0] += self.learning_rate * (label - prediction)  # if label not prediction, update

    """
    :param df: a file directory name to save file in
    saves trained weights to csv file
    """
    def save_weight(self, file_dir):
        pd.DataFrame(self.weights).to_csv(file_dir)

    """
    :param df: a file directory name to read file from
    saves trained weights to csv file
    """
    def read_weight(self, file_dir):
        weights_df = pd.read_csv(file_dir)
        self.weights = weights_df.iloc[1].to_numpy()




"""https://www.thomascountz.com/2018/04/05/19-line-line-by-line-python-perceptron"""
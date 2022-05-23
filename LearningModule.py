import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

DATA_DIR = "data_output/data_output.csv"
LABEL_DIR = "data_output/labels.csv"


class LearningModule:
    dataset_df = pd.DataFrame
    label_df = pd.DataFrame

    def __init__(self, data_dir, label_dir):
        self.label_df = LearningModule.load_data(label_dir)
        self.dataset_df = LearningModule.load_data(data_dir)

    @staticmethod
    def load_data(csv_dir):
        data = pd.read_csv(csv_dir, header=0)
        return data

    @staticmethod
    def display_graph(data, x, y):
        data = data.plot(kind='scatter', x="label", y="total time")
        data.show()
        return

    @staticmethod
    def plot_time_to_label(data):
        data = data.plot(kind='scatter', x="label", y="backspace pressed")
        plt.show()

    @staticmethod
    def calc_error(prediction, labels):
        labels_np = labels[["label"]].to_numpy()
        return np.mean(np.abs(labels_np - prediction))

    def predict(self, df_to_predict):
        reg = LinearRegression()
        reg.fit(self.dataset_df, self.label_df)
        a = reg.predict(df_to_predict)
        return a

    def test_linear_model(self, num_of_tests, to_hide):
        reg = LinearRegression()
        result_lst = []
        for i in range(num_of_tests):
            train_x, test_x, train_y, test_y = train_test_split(self.dataset_df, self.label_df,
                                                                test_size=to_hide, random_state=4)
            reg.fit(train_x, train_y)
            a = reg.predict(test_x)
            result_lst.append(LearningModule.calc_error(a, test_y))
        result = np.mean(np.array(result_lst))
        return result











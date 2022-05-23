from Form import *
from LearningModule import *
import DataHandler
import PostProcess

HARD_URL = "https://gatnevo.wixsite.com/my-site-2"
EASY_URL = "https://gatnevo.wixsite.com/my-site-3"
DATA_DIR = "data_output/data_output.csv"
LABEL_DIR = "data_output/labels.csv"
DATA_PTN_TO_HIDE = 0.2
NUM_OF_TESTS = 50


class TechSavvyDesign:
    form = Form
    linear_reg_model = LearningModule

    def __init__(self):
        self.form = Form()
        self.linear_reg_model = LearningModule(DATA_DIR, LABEL_DIR)

    def get_targeted_design(self):
        self.form.init()
        data_collected = self.form.get_raw_data()
        post_processed_data = PostProcess.process_raw_data(data_collected)
        df_to_determine = pd.DataFrame(post_processed_data, index=[0])
        label = self.linear_reg_model.predict(df_to_determine)
        print("Predicted Label is: ")
        print(label[0][0])
        if label[0][0] < THRESHOLD:
            webbrowser.open(EASY_URL)
        else:
            webbrowser.open(HARD_URL)

    def train_mode(self):
        self.form.init()
        data_collected = self.form.get_raw_data()
        post_processed_data = PostProcess.process_raw_data(data_collected)
        write_to_csv(post_processed_data)

    @staticmethod
    def test_mode():
        print("Tested dataset %d times\n" % NUM_OF_TESTS)
        print("Obscure %d of data in each round\n" % DATA_PTN_TO_HIDE)
        print("Avg error: %d" % LearningModule.test_linear_model(NUM_OF_TESTS, DATA_PTN_TO_HIDE))



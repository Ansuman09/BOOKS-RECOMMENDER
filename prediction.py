import pandas as pd
import numpy as np
class Predictor:
    def __init__(self,pred_df,books_df):
        self.pred_df=pred_df
        self.prediction=books_df.head(6)
        self.cum_predict_dfs=[]

    def val(self,val):
        return val[1]

    def make_prediction(self,liked=None):
        if liked!=None:
            array=self.pred_df.to_numpy()
            s = pd.Series(list(enumerate(array[liked])))
            pred = s.apply(self.val)
            predict = pd.DataFrame(np.arange(0, 7860), pred).sort_index(ascending=False)
            return predict
        elif liked==None:
            return self.prediction['image_url'].head(6)

    def cum_prediction(self,ids):
        for n in ids:
            value=self.make_prediction(n)
            reccomended_books = value
            cum_df = reccomended_books.reset_index(0)
            cum_df.set_index(0, inplace=True)
            cum_df.sort_index(ascending=True, inplace=True)
            self.cum_predict_dfs.append(cum_df)
        return self.cum_predict_dfs



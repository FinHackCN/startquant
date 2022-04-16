# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import numpy as np
import pandas as pd
import lightgbm as lgb
from typing import List, Text, Tuple, Union
from qlib.model.base import ModelFT
from qlib.data.dataset import DatasetH
from qlib.data.dataset.handler import DataHandlerLP
from qlib.model.interpret.base import LightGBMFInt
from qlib.data.dataset.weight import Reweighter
from qlib.workflow import R
from math import e

class LGBModel(ModelFT, LightGBMFInt):
    """LightGBM Model"""

    def custom_obj(y_pred,y_true): #损失函数
        y_true=y_true.get_label()
        residual = (y_true - y_pred).astype("float")#真实数据与预测数据的差距
        grad = 100*e**(y_pred-y_true)-100
        hess =100*e**(y_pred-y_true)
        return grad, hess

    def custom_eval(y_pred,y_true): #评估函数

        y_true=y_true.get_label()
        residual = (y_true - y_pred).astype("float")
        loss = 100*e**(-residual)+100*residual-100
        return "ds", np.mean(loss), False
    
    def __init__(self, loss="mse", early_stopping_rounds=50, num_boost_round=1000, **kwargs):
        self.params = {
                            'boosting_type': 'dart',
                            'max_depth': 5,
                            'num_leaves': 32,  # 叶子节点数
                            'learning_rate': 0.2,  # 学习速率
                            'feature_fraction': 0.7,  # 建树的特征选择比例colsample_bytree
                            'bagging_fraction': 0.7,  # 建树的样本采样比例subsample
                            'bagging_freq': 5,  # k 意味着每 k 次迭代执行bagging
                            'verbose': -1,  # <0 显示致命的, =0 显示错误 (警告), >0 显示信息
                            'lambda_l1':300,
                            'lambda_l2':300, 
        }
        self.params.update(kwargs)
        self.early_stopping_rounds = early_stopping_rounds
        self.num_boost_round = num_boost_round
        self.model = None

    def _prepare_data(self, dataset: DatasetH, reweighter=None) -> List[Tuple[lgb.Dataset, str]]:
        """
        The motivation of current version is to make validation optional
        - train segment is necessary;
        """
        ds_l = []
        assert "train" in dataset.segments
        for key in ["train", "valid"]:
            if key in dataset.segments:
                df = dataset.prepare(key, col_set=["feature", "label"], data_key=DataHandlerLP.DK_L)
                if df.empty:
                    raise ValueError("Empty data from dataset, please check your dataset config.")
                x, y = df["feature"], df["label"]

                # Lightgbm need 1D array as its label
                if y.values.ndim == 2 and y.values.shape[1] == 1:
                    y = np.squeeze(y.values)
                else:
                    raise ValueError("LightGBM doesn't support multi-label training")

                if reweighter is None:
                    w = None
                elif isinstance(reweighter, Reweighter):
                    w = reweighter.reweight(df)
                else:
                    raise ValueError("Unsupported reweighter type.")
                ds_l.append((lgb.Dataset(x.values, label=y, weight=w), key))
        return ds_l

    def fit(
        self,
        dataset: DatasetH,
        num_boost_round=None,
        early_stopping_rounds=None,
        verbose_eval=20,
        evals_result=None,
        reweighter=None,
        **kwargs,
    ):
        if evals_result is None:
            evals_result = {}  # in case of unsafety of Python default values
        ds_l = self._prepare_data(dataset, reweighter)
        ds, names = list(zip(*ds_l))
        early_stopping_callback = lgb.early_stopping(
            self.early_stopping_rounds if early_stopping_rounds is None else early_stopping_rounds
        )
        # NOTE: if you encounter error here. Please upgrade your lightgbm
        verbose_eval_callback = lgb.log_evaluation(period=verbose_eval)
        evals_result_callback = lgb.record_evaluation(evals_result)
        self.model = lgb.train(
            self.params,
            ds[0],  # training dataset
            num_boost_round=self.num_boost_round if num_boost_round is None else num_boost_round,
            valid_sets=ds,
            valid_names=names,
            fobj=LGBModel.custom_obj,
            feval=LGBModel.custom_eval,            
            callbacks=[early_stopping_callback, verbose_eval_callback, evals_result_callback],
            **kwargs,
        )
        for k in names:
            for key, val in evals_result[k].items():
                name = f"{key}.{k}"
                for epoch, m in enumerate(val):
                    R.log_metrics(**{name.replace("@", "_"): m}, step=epoch)

    def predict(self, dataset: DatasetH, segment: Union[Text, slice] = "test"):
        if self.model is None:
            raise ValueError("model is not fitted yet!")
        x_test = dataset.prepare(segment, col_set="feature", data_key=DataHandlerLP.DK_I)
        return pd.Series(self.model.predict(x_test.values), index=x_test.index)

    def finetune(self, dataset: DatasetH, num_boost_round=10, verbose_eval=20, reweighter=None):
        """
        finetune model

        Parameters
        ----------
        dataset : DatasetH
            dataset for finetuning
        num_boost_round : int
            number of round to finetune model
        verbose_eval : int
            verbose level
        """
        # Based on existing model and finetune by train more rounds
        dtrain, _ = self._prepare_data(dataset, reweighter)  # pylint: disable=W0632
        if dtrain.empty:
            raise ValueError("Empty data from dataset, please check your dataset config.")
        verbose_eval_callback = lgb.log_evaluation(period=verbose_eval)
        self.model = lgb.train(
            self.params,
            dtrain,
            num_boost_round=num_boost_round,
            init_model=self.model,
            valid_sets=[dtrain],
            valid_names=["train"],
            callbacks=[verbose_eval_callback],
        )

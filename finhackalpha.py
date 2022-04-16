# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from qlib.data.dataset.handler import DataHandlerLP
from qlib.data.dataset.processor import Processor
from qlib.utils import get_callable_kwargs
from qlib.data.dataset import processor as processor_module
from inspect import getfullargspec

 
class finhackalpha(DataHandlerLP):
    def __init__(
        self,
        instruments="test",
        start_time=None,
        end_time=None,
        freq="day",
        fit_start_time=None,
        fit_end_time=None,
        process_type=DataHandlerLP.PTYPE_A,
        filter_pipe=None,
        inst_processor=None,
        **kwargs,
    ):
 
        data_loader = {
            "class": "QlibDataLoader",
            "kwargs": {
                "config": {
                    "feature": self.get_feature_config(),
                    "label": self.get_label_config(),
                },
                "filter_pipe": filter_pipe,
                "freq": freq,
                "inst_processor": inst_processor,
            },
        }
        
        super().__init__(
            instruments=instruments,
            start_time=start_time,
            end_time=end_time,
            data_loader=data_loader,
        )

    def get_feature_config(self):
        conf = {
 
        }

        return self.parse_config_to_fields(conf)
    def get_label_config(self):
        return (["Ref($close, -10) / Ref($close, -1)"], ["LABEL0"])

    @staticmethod
    def parse_config_to_fields(config):
        fields = [
          '$UPPER','$DEMA','$EMA90','$MA90','$MAMA','$MAVP','$MIDPOINT','$MIDPRICE','$SAR','$SAREXT','$SMA','$T3','$TEMA','$TRIMA','$WMA','$ADX','$ADXR','$APO','$AROONDOWN','$AROONOSC','$BOP','$CCI','$CMO','$DX','$MACD','$MACDX','$MACDFIX','$MFI','$MOM','$PPO','$ROC','$ROCR','$ROCR100','$RSI','$SLOWK','$FASTK','$TRIX','$ULTOSC','$WILLR','$AD','$ADOSC','$OBV','$ATR','$NATR','$TRANGE','$AVGPRICE','$MEDPRICE','$TYPPRICE','$WCLPRIC','$INPHASE','$SINE','$BETA','$CORREL','$LINEARREG','$STDDEV','$TSF','$VAR','$ACOS','$ASIN','$ATAN','$CEIL','$COS','$COSH','$EXP','$FLOOR','$LN','$LOG10','$SIN','$SINH','$SQRT','$TAN','$TANH','$ADD','$DIV','$MAX','$MAXINDEX','$MIN','$MININDEX','$MINIDX','$MULT','$SUB','$SUM'

        ]
        names = [
          'UPPER','DEMA','EMA90','MA90','MAMA','MAVP','MIDPOINT','MIDPRICE','SAR','SAREXT','SMA','T3','TEMA','TRIMA','WMA','ADX','ADXR','APO','AROONDOWN','AROONOSC','BOP','CCI','CMO','DX','MACD','MACDX','MACDFIX','MFI','MOM','PPO','ROC','ROCR','ROCR100','RSI','SLOWK','FASTK','TRIX','ULTOSC','WILLR','AD','ADOSC','OBV','ATR','NATR','TRANGE','AVGPRICE','MEDPRICE','TYPPRICE','WCLPRIC','INPHASE','SINE','BETA','CORREL','LINEARREG','STDDEV','TSF','VAR','ACOS','ASIN','ATAN','CEIL','COS','COSH','EXP','FLOOR','LN','LOG10','SIN','SINH','SQRT','TAN','TANH','ADD','DIV','MAX','MAXINDEX','MIN','MININDEX','MINIDX','MULT','SUB','SUM'
        ]

        print ('total alphas:'+str(len(names)))
        return fields, names
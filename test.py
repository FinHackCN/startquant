import pandas as pd
import tushare as ts
from xlib.mysql import mysql
from xlib.astock import AStock

def fcompute(ts_code,df_cal,basic):
    df_price=AStock.getStockDailyPriceByCode(ts_code,db)
    df_price=pd.merge(df_cal,df_price,on=['trade_date'],how='outer', validate="one_to_many")
    df_balance=mysql.selectToDf("select ann_date as trade_date,fix_assets,cip,intan_assets,r_and_d from astock_finance_balancesheet where ts_code='"+ts_code+"' and report_type=1 order by trade_date asc",db)
    df_daily_basic=mysql.selectToDf("select trade_date,total_mv from astock_price_daily_basic where ts_code='"+ts_code+"' order by trade_date asc",db)
    df=pd.merge(df_price, df_balance, how='left', on='trade_date', copy=True, indicator=False)
    df=pd.merge(df, df_daily_basic, how='left', on='trade_date', copy=True, indicator=False)
    df=df.fillna(method='ffill')
    df['ts_code']=ts_code
    df['industy']=str(basic[basic['ts_code']==ts_code]['industry'].values[0])
    df=df[df.trade_date>'20150101']
    df=df[df.trade_date<'20220410']
    df=df.reset_index(drop=True)
    df['f1']=df['inventories'].astype('float')/df['total_mv'].astype('float')
    df.rename(columns={'ts_code':'symbol','trade_date':'date'}, inplace = True)
    df['date']=df['date'].map(lambda x: x[:4]+'-'+x[4:6]+'-'+x[6:8])
    return df


db="tushare"
df_cal=mysql.selectToDf("select cal_date as trade_date from astock_trade_cal where is_open=1",db)
basic=mysql.selectToDf("select ts_code,industry from astock_basic",db)

pro = ts.pro_api()
df_code = pro.index_weight(index_code='000300.SH', start_date='20150101', end_date='20220410')
df_code.drop_duplicates(subset=['con_code'],keep='first',inplace=True)
 
df_all=[]
df_mean_all=[]
df_code=df_code['con_code'].to_list()

for ts_code in df_code:
    df=fcompute(ts_code,df_cal,basic)
    df_all.append(df)
    df_mean_all.append({
        'ts_code':ts_code,
        'industry':df['industry'].values[0],
        'mean':df['f1'].mean()
    })
    print(ts_code)

df_all=pd.concat(df_all)


df_mean_all=pd.DataFrame(df_mean_all)
df_all['f2']=df_all.apply(lambda x: df_mean_all[df_mean_all['industry']==x['industry']]['mean'].mean(),axis=1) 
df_all['f3']=df_all['f1']/df_all['f2']
    
print(df_all)
df_all.to_csv("./xlib/cache/fin.csv")

 




# import pandas as pd
# from xlib import data
# import akshare as ak
# df=data.get_all_index_data()

 



# idx_data = ak.index_zh_a_hist(symbol='000300', period="daily", start_date='20200101', end_date='20220410')    
# idx_data.rename(columns={'日期':'date', '开盘':'open', '收盘':'close', 
#                           '最高':'high', '最低':'low', '成交量':'volume',
#                           '成交额':'amount', '振幅':'swing', '涨跌幅':'chg_pct',
#                           '涨跌额':'chg_amount', '换手率':'turnover',
#                           }, inplace = True)
# idx_data['date'] = pd.to_datetime(idx_data['date'], format='%Y-%m-%d')
# idx_data.set_index('date')
# bench=idx_data.drop_duplicates(subset=['date'],keep='first',inplace=True)
# bench=idx_data


# df=pd.read_csv('./xlib/cache/fin.csv',index_col=0)
# print(df)


# # #factors.analysis(df,'MACD')


# from xlib import model

# df_train,df_valid,df_pred=model.datasplit(df,train_end='2019-01-01',valid_end='2020-01-01')

# model.lgbtrain(df_train,df_valid,label='label')  
# preds=model.lgbpred(df_pred,label='label') 


# print(preds)

 
# # #

# from xlib.strategies import Top10Strategy




# from xlib import backtest

# preds['score']=preds['pred']
# preds['rank']=preds.groupby('date')['pred'].rank()
# preds['signal']=preds.apply(lambda x: 1 if x['rank']<=10 else 0 ,axis=1)


# print(preds['symbol'])


# returns=backtest.test(preds,Top10Strategy)
# backtest.analysis(returns,bench)


# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 01:49:23 2018
缠论所有的内容
（1）数据提取
（2）合并
（3）笔的确定
（4）中枢的确定
@author: Everyheart
"""
#%
import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt
#====================================================================================
#（1）数据的处理
def data(code='000001',asset='INDEX',start_date='2014-06-11',end_date='2016-06-20',freq='D'):
    cons = ts.get_apis()
    df = ts.bar(code, conn=cons, freq=freq,asset=asset,start_date=start_date, end_date=end_date)#获取数据表格
    df=df.sort_index(axis=0,ascending=True)
    return df
#df=data()
#====================================================================================
#====================================================================================
#(2)合并的操作
def hebin0(df):
    df=df.values
    H=df[:,3]
    L=df[:,4]
    m=len(L)
    #下面首先对开始的情况进行分析,确定第一个开始的位置
    for i in range(m):
        if H[i]==H[i+1] and L[i]==L[i+1]:
            continue
        else:
            q=i#这里q是q和q+1不相等，为了后面的正确，下面要从q+1开始
            break
    for i in range(q+2,m+1):#从下面开始减一
        if H[i-1]>=H[i-1-1] and L[i-1]<=L[i-1-1]:
            s=1
            while H[i-1-1]==H[i-s-1-1] and L[i-1-1]==L[i-s-1-1]:
                s=s+1
            if H[i-s-1]>=H[i-s-1-1] and L[i-s-1]>=L[i-s-1-1]:
                L[i-1]=L[i-1-1]
                for t in range(1,s+1):
                    H[i-t-1]=H[i-1]
            elif H[i-s-1]<=H[i-s-1-1] and L[i-s-1]<=L[i-s-1-1]:
                H[i-1]=H[i-1-1]
                for t in range(1,s+1):
                    L[i-t-1]=L[i-1]
        elif H[i-1]<=H[i-1-1] and L[i-1]>=L[i-1-1]:
            s=1
            while H[i-1-1]==H[i-s-1-1] and L[i-1-1]==L[i-s-1-1]:
                s=s+1
            if H[i-s-1]>=H[i-s-1-1] and L[i-s-1]>=L[i-s-1-1]:
                H[i-1]=H[i-1-1]
                for t in range(1,s+1):
                    L[i-t-1]=L[i-1]
            elif H[i-s-1]<=H[i-s-1-1] and L[i-s-1]<=L[i-s-1-1]:
                L[i-1]=L[i-1-1]
                for t in range(1,s+1):
                    H[i-t-1]=H[i-1]
    return H,L
#H,L=hebin0(df)
#H1=list(H)
#L1=list(L)
                    
def hebin1(H,L):
    i=1
    H=list(H)
    L=list(L)
    m=len(L)
    X=[]
    while i <=m-1:
        q=i-len(X)
        if H[q-1]==H[q+1-1] and L[q-1]==L[q+1-1]:
            del H[q-1]
            del L[q-1]
            X.append(i-1)
        i=i+1
    return H,L,X
#H,L,jl=hebin1(H,L)
#====================================================================================
#====================================================================================
#%(3)
#下面对于笔进行处理，要找到我们要的可以连接成笔的顶分型和底分型的点，之后画图3，后，用原来的图，在上面画出笔。
def fenbi(H,L):
    i=2
    T=[]
    W=[]
    m=len(L)
    j=-100
    Q=[]
    DD=[]
    GG=[]
    q=20
    m1=max(int(49*m/50),m-20)
    while i<m1:
        if H[i-1]>H[i+1-1] and H[i-1]>H[i-1-1]:
            for s in range(1,len(H)-i):#这里做了修改，
                if H[i+s-1]>H[i+s-1-1] and H[i+s-1]>H[i+s+1-1] and H[i+s-1]>=H[i-1]:
                    break
                elif H[i+s-1]<H[i+s+1-1] and H[i+s-1]<H[i+s-1-1] and s>=4:
                    LQ=L[i+1-1]
                    for t in range(1,s):
                        LQ=min(LQ,L[i+t-1])
                    if LQ<L[i+s-1]:
                        continue
                    else:
                        if q==1:
                            break
                        elif i-j<4:
                            break
                        else:
                            if j<0:
                                lq=H[1-1]
                                for f in range(1,i):
                                    lq=max(lq,H[f-1])
                            elif j>0 :
                                lq=H[j-1]
                                for f in range(j+1,i):
                                    lq=max(lq,H[f-1])
                            if lq>H[i-1]:
                                break
                            else:
                                T.append(i-1)
                                W.append(H[i-1])
                                j=i
                                GG.append(H[i-1])
                                i=i+1
                                q=1
                                Q.append(q)
                                break
            i=i+1
            continue
        elif L[i-1]<L[i+1-1] and L[i-1]<L[i-1-1]:
            for s in range(1,len(H)-i):#这里做了修改，
                if L[i+s-1]<L[i+s-1-1] and L[i+s-1]<L[i+s-1-1] and L[i+s-1]<=L[i-1]:
                    break
                elif H[i+s-1]>H[i+s+1-1] and H[i+s-1] >H[i+s-1-1] and s>=4:
                    PQ=H[i+1-1]
                    for t in range(1,s):
                        PQ=max(PQ,H[i+t-1])
                    if PQ>H[i+s-1]:
                        continue
                    else:
                        if q==-1:
                            break
                        elif i-j<4:
                            break
                        else:
                            if j<0:
                                lq=L[1-1]
                                for f in range(1,i):
                                    lq=min(lq,L[f-1])
                            elif j>0:
                                lq=L[j+1-1]
                                for f in range(j+1,i):
                                    lq=min(lq,L[f-1])
                            if lq<L[i-1]:
                                break
                            else:
                                T.append(i-1)
                                W.append(L[i-1])
                                j=i
                                DD.append(L[i-1])
                                i=i+1
                                q=-1
                                Q.append(q)
                                break
            i=i+1
            continue
        else:
            i=i+1
    return T,W,Q,GG,DD
#T,W,Q,GG,DD=fenbi(H,L)
#====================================================================================
#====================================================================================
#%(4)
#上面是对于第一部分的处理后，接下来对于剩下的部分进行处理
def fenbi1(H,L,T,W,Q,GG,DD):
    hb=len(L)
    zh=T[-1]#这个不用-1
    zhyg=zh
    q=Q[-1]
    for ii in range(zh+1,hb):
        if q==1:
            if H[ii-1]<H[ii-1-1] and H[ii-1]<H[ii+1-1] and (ii-zhyg)>3:
                PQ1=L[zhyg-1]
                for i2 in range(zhyg,ii):
                    PQ1=min(PQ1,L[i2-1])
                if L[ii-1]>PQ1:
                    continue
                elif L[ii-1]<=PQ1:
                    xin=ii-1
                    yin=L[ii-1]
                    for i3 in range(ii+1,hb):
                        if H[i3-1]>H[i3-1-1] and H[i3-1]>H[i3+1-1] and (i3-ii)>3:
                            PQ2=H[ii-1]
                            PP2=L[ii-1]
                            for i4 in range(ii,i3):
                                PQ2=max(PQ2,H[i4-1])
                                PP2=min(PP2,L[i4-1])
                            if H[i3-1]<PQ2:
                                continue
                            elif L[ii-1]>PP2:
                                continue
                            elif H[i4-1]>=PQ2:
                                zhyg=ii
                                T.append(ii)
                                W.append(L[ii-1])
                                q=-1
                                Q.append(q)
                                DD.append(L[ii-1])
                                break
            else:
                continue
        elif q==-1:
            if H[ii-1]>H[ii-1-1] and H[ii-1]>H[ii+1-1] and (ii-zhyg)>3:
                
                PQ1=H[zhyg-1]
                for i2 in range(zhyg,ii-1):
                    PQ1=max(PQ1,H[i2-1])
                if H[ii-1]<PQ1:
                    continue
                elif H[ii-1]>=PQ1:
                    xin=ii-1
                    yin=H[ii-1]
                    for i3 in range(ii+1,hb):
                        if H[i3-1]<H[i3-1-1] and H[i3-1]<H[i3+1-1] and (i3-ii)>3:
                            PQ2=L[ii-1]
                            PP2=H[ii-1]
                            for i4 in range(ii,i3):
                                PQ2=min(PQ2,L[i4-1])
                                PP2=max(PP2,H[i4-1])
                            if L[i3-1]>PQ2:
                                continue
                            elif H[ii-1]<PP2:
                                continue
                            elif L[i3-1]<=PQ2:
                                zhyg=ii
                                T.append(ii)
                                W.append(H[ii-1])
                                q=1
                                Q.append(q)
                                GG.append(H[ii-1])
                                break
            else:  
                continue
    return T,W,Q,xin,yin,GG,DD
#T11,W11,Q11,xin,yin,GG11,DD11=fenbi1(H,L,T,W,Q,GG,DD)
            
    
#====================================================================================
#%(5)
#这个式子是将通过消去处理后的位置复原到他本来就该有的位置
def tt1(x,d):

    m=len(x)
    n=len(d)
    
    x=np.array(x)
    d=np.array(d)
    for i in range(1,m+1):
        q=1
        while x[i-1]>d[q-1]:
            q=q+1
            if q>n:
                break
        d[q-1:]=d[q-1:]+1
    d=d-1
    d=list(d)
    return d

#TT=tt1(jl,T11)
#t2=TT[-1]#%这个是最后一个的实际位置
#y2=W[-1]
#xin1=tt1(jl,[xin])
#XIN=[t2,int(xin1)]#这个是最后一个线段两个点的x轴坐标
#YIN=[y2,yin]#这个是最后一个线段两个点的y轴坐标
#====================================================================================
#====================================================================================
#%(6)

#下面定义中枢

def zhongshu(Q,GG,DD):
    JLZS=[]
    #lw=len(W)
    if Q[1-1]==1:
        del GG[1-1]
        ss=1
    else:
        ss=0

    if GG[2-1]<=DD[1-1]:
        i=1
        while DD[i+1-1]>=GG[2+i-1]:
            i=i+1
        ZG=min(GG[1+i-1],GG[2+i-1])
        ZD=max(DD[1+i-1],DD[2+i-1])
        if ss==1:
            JLZS.append(2*(1+i-1)-1+2)
        else:
            JLZS.append(2*(1+i-1)-1+1)
        
        for t in range(2+i,i+41):#这里的41可以调，回头试试
            if GG[t-1]<ZD:
                ks=t
                pp=-1
                break
            elif DD[t-1]>ZG:
                pp=1
                ks=t
                break
    elif DD[3-1]>=GG[1-1]:
        i=1
        while DD[i+2-1]>GG[i-1]:
            i=i+1
        ZG=min(GG[i-1],GG[i+1-1])
        ZD=max(DD[i+2-1],DD[i+1-1])
        if ss==1:
            JLZS.append(2*(i-1)+2)
        else:
            JLZS.append(2*(i-1)+1)
            
        for t in range(i,i+41):
            if DD[t-1]>ZG:
                pp=1
                ks=t
                break
            elif GG[t-1]<ZD:
                pp=-1
                ks=t
                break
    else:
        ZG=min(GG[1-1],GG[2-1])
        ZD=max(DD[3-1],DD[2-1])
        if ss==1:
            JLZS.append(1-1+2)
        else:
            JLZS.append(1-1+1)

        m=min(len(GG),len(DD))
        for t in range(1,m+1):
            if DD[t-1]>ZG:
                pp=1
                ks=t
                break
            elif GG[t-1]<ZD:
                pp=-1
                ks=t#%对开始的位置记录 ,这里对应的是突破中枢的一个向上笔，都是t
                break
            else:
                pp=2 #这里是处理特别的情况，防止后面没有第二个中枢的
    #在完成之前的内容后，开始对于新形成的中枢进行处理。
    m=min(len(GG),len(DD))
    ZS=[(ZG,ZD)]
    
    k=0
    lk=0
    ck=0
    ll=0
    if len(DD)>m:
        ttt=1
    else:
        ttt=0    
    #return ZS
#ZS=zhongshu(GG11,DD11)
#print(ZS)

    while k<=m:
        if pp==1:
            i=ks
            while DD[i+1-1]>=GG[i-1-1]:
                if i<m-1:
                    i=i+1
                elif i>m-1:
                    break
                elif i==m-1:
                    lk=1
                    break
            if lk==1:
                break
            else:
                ZG=min(GG[i-1-1],GG[i-1])
                ZD=max(DD[i+1-1],DD[i-1])
                ZS.append((ZG,ZD))
                if ss==1:
                    JLZS.append(2*(i-1-1)+2)
                else:
                    JLZS.append(2*(i-1-1)+1)#这里的中枢是由i-1-1,i-1和i+1-1构成的
                    
            for t in range(i,i+201):#这里原来是i+201，但是会超出，我们尝试用len(GG)+1
                if t>m:
                    ll=1
                    break
                if DD[t-1]>ZG:
                    ks=t
                    pp=1
                    if ks==m and ttt==0:
                        ll=1
                    break
                elif GG[t-1]<ZD:
                    ks=t
                    pp=-1
                    if ks==m:
                        ll=1
                    break
                elif t>m:
                    ll=1
                    break
            if ll==1:
                break
            else:
                k=t
        elif pp==-1:
            i=ks
            while GG[i+1-1]<=DD[i-1]:
                if i<m-1:
                    i=i+1
                elif i>m-1:
                    break
                elif i==m-1:
                    ck=1
                    break
            if ck==1:
                break
            else:
                ZD=max(DD[i-1],DD[i+1-1])
                ZG=min(GG[i+1-1],GG[i-1])
                ZS.append((ZG,ZD))
                if ss==1:
                    JLZS.append(2*(i-1)-1+2)  
                else:
                    JLZS.append(2*(i-1)-1+1)
                    
            for t in range(i,i+201):
                if t>=m:
                    ll=1
                    break
                
                if DD[t-1]>ZG:
                    ks=t
                    pp=1
                    if ks==m and ttt==0:
                        ll=1
                    break
                elif GG[t-1]<ZD:
                    ks=t
                    pp=-1
                    if ks==m:
                        ll=1
                    break
                elif t>=m:
                    ll=1
                    break
            if ll==1:
                break
            else:
                k=t
        elif pp==2:
            break
    return ZS,JLZS
#ZS,JLZS=zhongshu(GG11,DD11)
#这里的JLZS得到的结果是形成中枢的第一个i的位置，也就是第一个GG上的位置
#print(ZS)            
                

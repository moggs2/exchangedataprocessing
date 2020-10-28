import pandas as pd
import unittest


class getdata:
    def __init__ (self, timeframe):
        self.timeframe=timeframe

    def getdf(self):
        df = pd.read_json("https://fxmarketapi.com/apitimeseries?api_key=G3uA1XZigyAIEqb5IkdS&currency=EURUSD,GBPUSD,USDEUR&interval=hourly&start_date=2020-07-16&end_date=2020-07-20&format=ohlc")
        return df

class trading:
    def __init__ (self, df, differencereached, symbol):
        
        self.df=df
        self.differencereached=differencereached
        self.symbol=symbol
    
    def getcurrency(self):
     df=self.df
     symbol=self.symbol
    
     currency = pd.DataFrame(columns=('number','date', 'open', 'high','low','close'))
     i=1
     for index, row in df.iterrows():

        thedata=pd.DataFrame.from_dict(row['price'])
        currency=currency.append({'number' : i, 'date' : index, 'open' : thedata[symbol]['open'], 'high' : thedata[symbol]['high'], 'low' : thedata[symbol]['low'], 'close' : thedata[symbol]['close']}, ignore_index=True)
        i=i+1
     return currency
    
    def newtimeframeohlc(self, newtimeframemultiplicator):
        olddf=self.getcurrency()
        self.newtimeframemultiplicator=newtimeframemultiplicator
        newtimeframeohlc = pd.DataFrame(columns=('number','date', 'open', 'high','low','close'))
        i=1
        y=1
        for index, row in olddf.iterrows():
          breakpoint=(i-1)/newtimeframemultiplicator
          lastpoint=i/newtimeframemultiplicator
          if i==1 or (breakpoint %1 == 0):
            dateactual=row['date']
            openactual=row['open']
            highactual=row['high']
            lowactual=row['low']
          elif i!=1 and (lastpoint %1 ==0):
            if row['high']>highactual:
              highactual=row['high']
            if row['low']<lowactual:
              lowactual=row['low']
            closeactual=row['close']
            newtimeframeohlc=newtimeframeohlc.append({'number' : y, 'date' : dateactual, 'open' : openactual, 'high' : highactual, 'low' : lowactual, 'close' : closeactual}, ignore_index=True)
            y=y+1
          elif i!=1:
            if row['high']>highactual:
              highactual=row['high']
            if row['low']<lowactual:
              lowactual=row['low']
          if max(olddf.number)==row['number'] and (lastpoint %1 !=0):
            if row['high']>highactual:
              highactual=row['high']
            if row['low']<lowactual:
              lowactual=row['low']
            closeactual=row['close']
            newtimeframeohlc=newtimeframeohlc.append({'number' : y, 'date' : dateactual, 'open' : openactual, 'high' : highactual, 'low' : lowactual, 'close' : closeactual}, ignore_index=True)
            y=y+1
          i=i+1
        return newtimeframeohlc
    
    def getlowest(self):
        df=self.getcurrency()
        lowest=min(df['low'])
        return lowest
    
    def getlowestbarnumber(self):
        df=self.getcurrency()
        df_lowest=df[(df.low==self.getlowest()) & (df.number>23)]
        dflowestnumber=df_lowest['number']
        return dflowestnumber.iloc[0]
    
    def getdiff(self):
        df=self.getcurrency()
        diffdf=df.close.diff()
        return diffdf
        
    def relevantdata(self):
        df=self.getdiff()
        relevantdatadf=df[df.index>=self.getlowestbarnumber()]
        return relevantdatadf
    
    def getratio(self):
        df=self.relevantdata()
        higher=df[df>=0].count()
        lower=df[df<=0].count()
        ratio=higher/lower
        return ratio
        
    def allrelevantdata(self):
        df=self.getcurrency()
        allrelevantdata=df[df.index>=self.getlowestbarnumber()]
        return allrelevantdata
    
    def highsincelow(self):
        df=self.allrelevantdata()
        highsincelow=max(df.high)
        return highsincelow
    
    def rangetotal(self):
        rangetotal=(self.highsincelow()-self.getlowest())/self.getlowest()*10000
        rangetotal=round(rangetotal,0)
        return rangetotal
    
    def position(self):
        allrelevantdata=self.allrelevantdata()
        price=allrelevantdata[allrelevantdata.number==max(allrelevantdata.number)].close
        position=(price-self.getlowest())/(self.highsincelow()-self.getlowest())*100
        position=round(position,0)
        return position.iloc[0]
    
    def lowrange(self):
        lowrange=self.getlowest()*1.0015
        return lowrange
    
    def lowcount(self):
        allrelevantdata=self.allrelevantdata()
        lowcount=allrelevantdata[allrelevantdata.low<=self.lowrange()].low.count()
        return lowcount
    
    def highrange(self):
        highrange=self.highsincelow()-self.highsincelow()*0.007
        return highrange
    
    def highcount(self):
        allrelevantdata=self.allrelevantdata()
        highcount=allrelevantdata[allrelevantdata.high>=self.highrange()].high.count()
        return highcount
    
    def desiredlevel(self):
        level=self.getlowest()*(1+self.differencereached/10000)
        return level
    
    def desiredlevelcount(self):
        allrelevantdata=self.allrelevantdata()
        count=allrelevantdata[allrelevantdata.high>=self.desiredlevel()].high.count()
        return count

    
class   testing(unittest.TestCase):
    
    def testexample(self):
        testobject=trading(df, 10, 'EURUSD')
        self.assertEqual(testobject.position, 88)
                 
tradingm1 = trading(df, 10, 'EURUSD')

#print(tradingm1.getcurrency())
#print(tradingm1.getcurrency())
#print(tradingm1.newtimeframeohlc(3))
#print(tradingm1.getlowest())
#print(tradingm1.getlowestbarnumber())
#print(tradingm1.getdiff())
#print(tradingm1.relevantdata())
#print(tradingm1.getratio())
#print(tradingm1.allrelevantdata())
#print(tradingm1.highsincelow())
#print(tradingm1.rangetotal())
#print(tradingm1.rangetotal())
#print(tradingm1.position())
#print(tradingm1.lowrange())
#print(tradingm1.lowcount())
#print(tradingm1.highrange())
#print(tradingm1.highcount())
print(tradingm1.desiredlevel())
print(tradingm1.desiredlevelcount())

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
#test

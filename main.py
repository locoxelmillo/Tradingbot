import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from binance.client import Client
from datetime import datetime, timedelta
import time
import talib

def APIcaller(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, time=120):
    # Configurar las credenciales de la API de Binance
    api_key = 'TU_API_KEY'
    api_secret = 'TU_API_SECRET'
    client = Client(api_key, api_secret)    
    # Calcular las fechas de inicio y fin
    end_date = datetime.now()
    start_date = end_date - timedelta(minutes=time)
    # Convertir las fechas al formato requerido por la API
    start_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
    historical_klines = client.get_historical_klines(symbol, interval, start_str=start_str, end_str=end_str) 
    # Crear una lista de columnas para el DataFrame
    columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
               'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
               'Taker Buy Quote Asset Volume', 'Ignore']
    # Crear el DataFrame
    df = pd.DataFrame(historical_klines, columns=columns)
    
    # Convertir las columnas relevantes a tipos de datos adecuados
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df['Open'] = df['Open'].astype(float)
    df['Close'] = df['Close'].astype(float)
    
    return df

sample = 0

try:
    while True:
        df = APIcaller()
        
        # Calcular las Bandas de Bollinger utilizando TA-Lib
        upper_band, middle_band, lower_band = talib.BBANDS(df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2)
        
        # Calcular el RSI utilizando TA-Lib
        rsi = talib.RSI(df['Close'], timeperiod=14)
        
        # Detectar cruces de precio con las Bandas de Bollinger
        crossovers_upper = df['Close'] > upper_band
        crossovers_lower = df['Close'] < lower_band
        
        # Detectar valores de RSI fuera de los niveles 30 y 70
        oversold = rsi < 30
        overbought = rsi > 70
        
        long_signals = crossovers_lower & oversold
        short_signals = crossovers_upper & overbought
        
        if long_signals.iloc[-1]:
            print("Long " + df.iloc[-1]['Timestamp'].strftime('%H:%M'))
        elif short_signals.iloc[-1]:
            print("Short " + df.iloc[-1]['Timestamp'].strftime('%H:%M'))
        else: 
            print("No operation " + df.iloc[-1]['Timestamp'].strftime('%H:%M'))
            
        # Resto del código para crear los gráficos...
            
except KeyboardInterrupt:
   print("Programa terminado")

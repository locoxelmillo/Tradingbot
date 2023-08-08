# Usa una imagen base de Python
FROM python:3.8

# Copia los archivos necesarios al contenedor
COPY main.py /app/main.py

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias necesarias
RUN pip install pandas matplotlib python-binance backtesting
RUN apt-get update && apt-get install -y git

# Comando para ejecutar tu script
CMD ["python", "main.py"]

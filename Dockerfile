FROM python:3.8
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install
RUN pip install TA-Lib
RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

ADD . /code
WORKDIR /code

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# Copia los archivos necesarios al contenedor
COPY main.py /app/main.py

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias necesarias
RUN pip install pandas matplotlib python-binance backtesting

# Comando para ejecutar tu script
CMD ["python", "main.py"]

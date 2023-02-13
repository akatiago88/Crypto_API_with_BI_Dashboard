from datetime import datetime
import time
import locale
import sqlalchemy
from coingecko import CoinGeckoAPI
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, Time, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

api = CoinGeckoAPI(url_base='https://api.coingecko.com/api/v3')

engine = create_engine('postgresql://postgres:admin@localhost/coingecko')
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
Base = sqlalchemy.orm.declarative_base()


class TbCripto(Base):
    __tablename__ = 'tb_cripto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float)
    marketcap = Column(Float)
    vol_dia = Column(Float)
    change_price = Column(Float)
    data = Column(DateTime)
    horario = Column(Time)
    coin = Column(String)


def mensagem():
    try:
        moedas = ['bitcoin', 'ethereum', 'kaspa', 'litecoin', 'monero',
                  'ravencoin', 'cardano', 'matic-network', 'tron', 'ripple']
        for moeda in moedas:
            preco = ''
            atualizado_em = ''
            dados_moeda = ''
            preco, atualizado_em, dados_moeda, marketcap, vol_dia, change_price = api.consulta_preco(moeda)
            data = datetime.fromtimestamp(atualizado_em).strftime('%x %X')
            data_hora = datetime.now()
            dhf = data_hora.strftime('%d/%m/%Y %H:%M')
            horario = data_hora.strftime('%H:%M')
            tb_cripto = TbCripto(price=preco, marketcap=marketcap, vol_dia=vol_dia, change_price=change_price,
                                 data=dhf, horario=horario, coin=moeda)
            session.add(tb_cripto)
            session.commit()
            time.sleep(2)
    except Exception as ex:
        print(f'dev mensagem failed in: {ex}')

        # print(f'Cotação atual: {preco}')
        # print(f'Última atualização: {data}')
        # print(f'Marketcap: {marketcap}')
        # print(f'Volume 24hrs : {vol_dia}')
        # print(f'Mudança nas últimas 24hrs: {change_price}')
        # print('*' * 20)
        # print(dados_moeda)
        # print(datetime.now())


while True:
    current_time = time.time()
    next_minute = (current_time // 300 + 1) * 300
    wait_time = next_minute - current_time
    time.sleep(wait_time)
    mensagem()

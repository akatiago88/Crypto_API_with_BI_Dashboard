import requests


class CoinGeckoAPI:
    def __init__(self, url_base: str):
        self.url_base = url_base

    # def ping(self) -> bool:
    #     print('Verificando se a API esta online...')
    #     url = f'{self.url_base}/ping'
    #     return requests.get(url).status_code == 200

    def consulta_preco(self, id_moeda: str) -> tuple:
        try:
            print(f'Consultando preço da moeda de ID = {id_moeda}...')
            url = f'{self.url_base}/simple/price?ids={id_moeda}' \
                  f'&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=' \
                  f'true&include_last_updated_at=true'
            resposta = requests.get(url)
        except Exception as ex:
            print(f'consulta_preco failed in resposta: {ex}')

        try:
            dados_moeda = resposta.json().get(id_moeda, None)
            preco = dados_moeda.get('usd', None)
            atualizado_em = dados_moeda.get('last_updated_at', None)
            marketcap = dados_moeda.get('usd_market_cap', None)
            vol_dia = dados_moeda.get('usd_24h_vol')
            change_price = dados_moeda.get('usd_24h_change')

            return preco, atualizado_em, dados_moeda, marketcap, vol_dia, change_price

        except Exception as ex:
            print(f'consulta_preco failed in return: {ex}')

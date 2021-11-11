import requests
import lxml.html


def get_inf_avto(avt_num: str) -> dict:
    """
    Функция возвращает информацию об автомобиле c сайта vinru.ru
    :param avt_num: номер авто
    :return: {'auto_name': 'RENAULT DUSTER, ', 'auto_yar': '2012 г.', 'auto_god': 'Год производства: 2012', ...}
    """
    header = {
        'Host': 'vinru.ru',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'sec-ch-ua-mobile': '0',
        'sec-ch-ua-platform': 'Windows',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 '
                      'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://vinru.ru/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    params = {
        'Vin': avt_num,
        'Token': '03AGdBq26vPx_V28VfaF4qf3Hqfkc37xwh-qvBTfBFWUpmhMNKpvCkGDYeGV4x8e2RoIJVyTNSjSYi'
                 '-8Hcb3KezCZT0UG5rCtoWeRTW2m6UvzjC2FF2KJNMOvVq5SmiZXb9mzSpoFTEUc3hvgZZLp83a0FyMPpKSKxEvfayp_sXeB3Qi_IYB3Pe6f1GCxanMupbIi3j-2qYik0asQzhY19dIzl8De6dXv2n7qTi9zdEy_pgwP4ThLJVTj0U1N7xJSsX_-LgM0fnmoKxPjD0SXIfk-wL-8afK90TsAmiMk6TEqBLSPLRUhyL3vmG1amM8xp-WweR1klCkxp9QiCeFLJTn9TIgKcRfOfwJ5Xj3-XtQ5fbrpzoQFxR8Gcu_YeRPRHKcQbKfSGcdISqdk4auCMjviKJGgyZaPeRNGcO9bDZLnUQkOcGvQd3zVrys84mwApJYmAsXm40P5L '
    }

    response = requests.get('https://vinru.ru/poisk', headers=header, params=params)
    page = lxml.html.fromstring(response.content)

    dc_avto = {}
    if len(page.xpath('.//h1[@class="fw-light mb-0"]/text()')) < 1:
        return {}

    dc_avto['auto_name'] = page.xpath('.//h1[@class="fw-light mb-0"]/text()')[0]
    dc_avto['auto_yar'] = page.xpath('.//h1[@class="fw-light mb-0"]/small[@class="text-muted text-nowrap"]/text()')[0]
    dc_avto['auto_god'] = 'Год производства: ' + page.xpath('//*[contains(text(),"Год производства:")]/span/text()')[
        0].strip()
    dc_avto['auto_vin'] = 'VIN: ' + page.xpath('//*[contains(text(),"VIN:")]/span/text()')[0].strip()
    dc_avto['auto_kat'] = 'Категория ТС: ' + page.xpath('//*[contains(text(),"Категория ТС:")]/span/text()')[0]
    dc_avto['auto_w'] = 'Мощность двигателя: ' + page.xpath('//*[contains(text(),"Мощность двигателя:")]/span/text()')[
        0]
    dc_avto['auto_v'] = 'Объем двигателя: ' + page.xpath('//*[contains(text(),"Объем двигателя:")]/span/text()')[0]
    dc_avto['auto_reg'] = 'Место регистрации: ' + page.xpath('//*[contains(text(),"Место регистрации:")]/span/text()')[
        0]

    return dc_avto


if __name__ == '__main__':
    print(get_inf_avto('АОО1мА77'))

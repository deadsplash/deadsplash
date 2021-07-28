import requests
import json
from datetime import date


def downloader(cur):  # this function downloads/updates actual rates for exact currency
    print('Caching values...')
    try:
        new = requests.get(f'http://www.floatrates.com/daily/{cur}.json').json()
    except json.decoder.JSONDecodeError:
        print(f'There is no such a currency like {cur1.upper()}, try again.')  # in case of bad input
        return
    with open(f'curr_{cur}.json', 'w') as f:
        f.write(json.dumps(new))
    return new


def cache_checker(cur):  # checks if exact currency is already cached
    try:
        with open(f'curr_{cur}.json', 'r') as f:
            values = json.load(f)
            if actuality_checker(cur) == True:
                pass
            else:
                print("Data is outdated!")
                values = downloader(cur)
        return values
    except:  # we possibly can have a few errors, they are all fill be fixed using re-downloading file
        new_val = downloader(cur)
        return new_val


def actuality_checker(cur):  # check if cached rates are actual or not (they store date of updating inside)
    check_cur = 'usd'
    if cur == 'usd':  # each json file contains every rate exept self, so we are not letting error to be
        check_cur = 'eur'
    today = date.today().isoformat()
    month = {'Jan': "01", 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
             'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    with open(f'curr_{cur}.json', 'r') as f:
        values = json.load(f)
        today_date = str(values[f'{check_cur}']['date'])[-24:-22]
        today_month = month[f"{str(values[f'{check_cur}']['date'])[-21:-18]}"]
        today_year = str(values[f'{check_cur}']['date'])[-17:-13]
        today_act = f'{today_year}-{today_month}-{today_date}'
        if today_act == today:
            return True
        else:
            return False


def converter(cur1, cur2, q):  # actual converter engine
    value = cache_checker(cur1)
    try:
        try:
            result = float(value[f'{cur2}']["rate"]) * float(q)
        except KeyError:  # in case of bad input
            print(f'There is no such a currency like {cur2.upper()}, try again')
            return
    except TypeError:  # in case of bad input
        return
    print(f'You will receive {result.__round__(2)} {cur2.upper()}')


while True:  # made infinite loop for debugging and using as long as i want
    cur1 = str(input('You sell:  ')).lower()
    cur2 = str(input('You buy:  ')).lower()
    q = float(input(f'How much {cur1.upper()} you have?:  '))
    converter(cur1, cur2, q)

# just remember to use currency code
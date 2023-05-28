import requests
from database.database import token_name, user_db


# Профиль пользователя
def get_profile(api_access_token: str):
    s7 = requests.Session()
    s7.headers['Accept']= 'application/json'
    s7.headers['authorization'] = 'Bearer ' + api_access_token
    p = s7.get('https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true')
    return p.json()


# Проверка Блокировки
def get_restrictions(api_access_token: str):
    s7 = requests.Session()
    s7.headers['Accept']= 'application/json'
    s7.headers['authorization'] = 'Bearer ' + api_access_token
    # получаем номер телефона
    login = get_profile(api_access_token)['contractInfo']['contractId']
    p = s7.get(f'https://edge.qiwi.com/person-profile/v1/persons/{login}/status/restrictions')
    return p.json()


# Баланс QIWI Кошелька
# только по токену
def balance(api_access_token: str):
    s = requests.Session()
    s.headers['Accept']= 'application/json'
    s.headers['authorization'] = 'Bearer ' + api_access_token
    # получаем номер телефона
    login = get_profile(api_access_token)['contractInfo']['contractId']
    b = s.get(f'https://edge.qiwi.com/funding-sources/v2/persons/{login}/accounts')
    return b.json()


# Баланс QIWI Кошелька
# только по токену и номеру
def balance_two(api_access_token: str, my_login: str):
    s = requests.Session()
    s.headers['Accept']= 'application/json'
    s.headers['authorization'] = 'Bearer ' + api_access_token
    b = s.get(f'https://edge.qiwi.com/funding-sources/v2/persons/{my_login}/accounts')
    return b.json()


# История платежей - последние и следующие n платежей
def payment_history_last(api_access_token: str):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token
    login = get_profile(api_access_token)['contractInfo']['contractId']
    parameters = {'rows': 3, 'nextTxnId': '', 'nextTxnDate': ''}
    h = s.get(f'https://edge.qiwi.com/payment-history/v2/persons/{login}/payments', params=parameters)
    return h.json()


def history_list(api_access_token: str):
    history = payment_history_last(api_access_token)['data']
    result, count = '', 1
    for elem in history:
        result += f'Номер платежа: {count}\n'\
                  f"Название: {elem['provider']['shortName'][:24]}...\n"\
                  f"Тип: {elem['type']}\n"\
                  f"Статус: {elem['statusText']}\n"\
                  f"ID: {elem['txnId']}\n"\
                  f"Дата: {elem['date'][:10]}\n"\
                  f"Время: {elem['date'][11:]}\n"\
                  f"{['Получатель', 'Отправитель'][elem['type']=='IN']}: {elem['account']}\n"\
                  f"Сумма: {('-','+')[elem['type']=='IN']}{elem['sum']['amount']} RUB\n\n"
        count += 1
    return result


def info_profile(user_id: int, api_access_token: str):
    profile = get_profile(api_access_token)
    result = f'Название: {user_db[user_id][api_access_token]}\n'\
             f'Блокировка: {["⛔ что то не так","✅ все хорошо"][get_restrictions(api_access_token)==[]]}\n'\
             f'Токен: ***{api_access_token[-15:]}\n'\
             f'Номер: <code>{profile["authInfo"]["personId"]}</code>\n'\
             f'Баланс: {balance_two(api_access_token, profile["authInfo"]["personId"])["accounts"][0]["balance"]["amount"]} RUB\n'\
             f'Статус: {profile["contractInfo"]["identificationInfo"][0]["identificationLevel"]}\n'\
             f'Оператор: {profile["userInfo"]["operator"]}\n' \
             f'Дата создания: {profile["authInfo"]["registrationDate"][:10]}'
    return result

#api_access_token = 'dca5af62d497e5f2baabc4351769afba'
#profile = get_restrictions(api_access_token)
# Профиль пользователя
# статус блокировки
#print(profile)
#api_access_token = '354576624319ee048bfede916ff4c608'
#print(info_profile('354576624319ee048bfede916ff4c608'))
#print(balance('354576624319ee048bfede916ff4c608'))
#print(get_profile(api_access_token)["authInfo"]["personId"])

'''
api = '13b04448560e0a112ac12ec6bbe61237'
for elem in history_list(api):
    print(elem)
'''

'''
api_access_token = 'dca5af62d497e5f2baabc4351769afba'
mylogin = '79094261150'
profile = get_profile(api_access_token)
balances = balance(api_access_token)['accounts']
# Профиль пользователя
# статус блокировки
print(profile['contractInfo']['contractId'])
print(f"Баланс: {balances[0]['balance']['amount']} RUB")


# последние 3 платежа
lastPayments = payment_history_last(api_access_token)
count = 1
for elem in lastPayments['data']:
    print(f'Номер платежа: {count}')
    print(f"Название: {elem['provider']['shortName']}")
    print(f"Тип: {elem['type']}")
    print(f"Статус: {elem['statusText']}")
    print(f"ID: {elem['txnId']}")
    print(f"Дата: {elem['date'][:10]}")
    print(f"Время: {elem['date'][11:]}")
    print(f"Получатель: {elem['account']}")
    print(f"Сумма: {('-','+')[elem['type']=='IN']}{elem['sum']['amount']}")
    print()
    count += 1
'''

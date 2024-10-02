from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Начальная цена токена в биткойнах
token_price = 0.000001  # Примерная цена в BTC
last_buyer_wallet = "1Cd8nZHAYFH7ZG8aJ1wfhCXhHuxzeRtqoB"  # Стартовый кошелек

def check_transaction_status(wallet_address):
    url = f'https://blockchair.com/bitcoin/address/{wallet_address}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Найдите элемент с последними транзакциями
        transactions = soup.find_all('tr', class_='transaction-row')
        
        for transaction in transactions:
            # Получите информацию о транзакции (например, сумму и статус)
            tx_data = transaction.find_all('td')
            if tx_data:
                amount = float(tx_data[2].text.replace(' BTC', '').replace(',', ''))
                if amount >= token_price:  # Проверяем, достаточно ли средств для покупки токена
                    return True  # Транзакция найдена и подтверждена
        
        return False  # Транзакция не найдена или сумма недостаточна
    else:
        return False  # Ошибка при получении данных

@app.route('/')
def index():
    return render_template('index.html', price=token_price, wallet_address=last_buyer_wallet)

@app.route('/update')
def update():
    global last_buyer_wallet, token_price
    
    if check_transaction_status(last_buyer_wallet):
        token_price *= 2  # Увеличиваем цену токена
        
    return jsonify({'price': token_price, 'wallet_address': last_buyer_wallet})

if __name__ == '__main__':
    app.run(debug=True)
import yfinance as yf_apple
import pandas as pd_apple
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt_apple
import matplotlib.dates as mdates_apple


# Прогноз на акции Apple
ticker_apple = "AAPL"

# Парсинг данных от Yahoo Finance
data_apple = yf_apple.download(ticker_apple, start="2016-01-01", end="2023-03-04")

# Создание нового DataFrame со столбцом «Adj Close»
df_apple = pd_apple.DataFrame(data_apple["Adj Close"])

# Рассчитать 7-дневный ценовой тренд
df_apple["PriceTrendApple"] = df_apple["Adj Close"].rolling(window=7).mean().shift(1)

# Разделение данных на наборы для обучения и тестирования
train_data_apple = df_apple[:len(df_apple) - 100]
test_data_apple = df_apple[len(df_apple) - 100:]

# Заполнение всех пропущенных значений средним значением столбца.
train_data_apple = train_data_apple.fillna(train_data_apple.mean())
test_data_apple = test_data_apple.fillna(test_data_apple.mean())

# Обучение модели линейной регрессии на данных
X_train_apple = train_data_apple["PriceTrendApple"].values.reshape(-1, 1)
y_train_apple = train_data_apple["Adj Close"].values.reshape(-1, 1)
model_apple = LinearRegression()
model_apple.fit(X_train_apple, y_train_apple)

# Создание прогноза на основе тестовых данных
X_test_apple = test_data_apple["PriceTrendApple"].values.reshape(-1, 1)
predictions_apple = model_apple.predict(X_test_apple)

# Создание DataFrame с датами и прогнозируемыми ценами
forecast_apple = pd_apple.DataFrame({'Date': test_data_apple.index, 'Predictions': predictions_apple.reshape(-1)})
# Объединение прогнозируемых DataFrame с исходным DataFrame
merged_apple = pd_apple.merge(df_apple, forecast_apple, how='outer', on='Date')

print(merged_apple.tail(10))

# Выстраивание на графике истории цен
plt_apple.plot(df_apple.index, df_apple['Adj Close'], label='Apple')

# График прогнозируемых цен
plt_apple.plot(merged_apple['Date'], merged_apple['Predictions'], label='Прогноз Apple')

# Установка названия графика и меток
plt_apple.title('Прогноз цен на акции')
plt_apple.xlabel('Даты')
plt_apple.ylabel('Цены')

# Установка частоты тиков по оси X, чтобы корректно отображать временной промежуток
plt_apple.gca().xaxis.set_major_locator(mdates_apple.DayLocator(interval=150))
plt_apple.gcf().autofmt_xdate()

# Show the legend and plot the chart
plt_apple.legend()
apple_filename = "apple.png"
plt_apple.savefig(apple_filename)


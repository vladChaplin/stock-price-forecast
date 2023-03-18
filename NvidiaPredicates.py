import yfinance as yf_nvda
import pandas as pd_nvda
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt_nvda
import matplotlib.dates as mdates_nvda


# Указание на нужный тикет(название акции)
ticker_nvda = "NVDA"

# Парсинг данных от Yahoo Finance
data_nvda = yf_nvda.download(ticker_nvda, start="2016-01-01", end="2023-03-04")

# Создание нового DataFrame со столбцом «Adj Close»
df_nvda = pd_nvda.DataFrame(data_nvda["Adj Close"])

# Рассчитать 7-дневный ценовой тренд
df_nvda["PriceTrend"] = df_nvda["Adj Close"].rolling(window=7).mean().shift(1)

# Разделение данных на наборы для обучения и тестирования
train_data_nvda = df_nvda[:len(df_nvda) - 100]
test_data_nvda = df_nvda[len(df_nvda) - 100:]

# Заполнение всех пропущенных значений средним значением столбца.
train_data_nvda = train_data_nvda.fillna(train_data_nvda.mean())
test_data_nvda = test_data_nvda.fillna(test_data_nvda.mean())

# Обучение модели линейной регрессии на данных
X_train_nvda = train_data_nvda["PriceTrend"].values.reshape(-1, 1)
y_train_nvda = train_data_nvda["Adj Close"].values.reshape(-1, 1)
model_nvda = LinearRegression()
model_nvda.fit(X_train_nvda, y_train_nvda)

# Создание прогноза на основе тестовых данных
X_test_nvda = test_data_nvda["PriceTrend"].values.reshape(-1, 1)
predictions_nvda = model_nvda.predict(X_test_nvda)

# Создание DataFrame с датами и прогнозируемыми ценами
forecast_nvda = pd_nvda.DataFrame({'Date': test_data_nvda.index, 'Predictions': predictions_nvda.reshape(-1)})
# Объединение прогнозируемых DataFrame с исходным DataFrame
merged_nvda = pd_nvda.merge(df_nvda, forecast_nvda, how='outer', on='Date')

print(merged_nvda.tail(10))

# Выстраивание на графике истории цен
plt_nvda.plot(df_nvda.index, df_nvda['Adj Close'], label='Nvidia')

# График прогнозируемых цен
plt_nvda.plot(merged_nvda['Date'], merged_nvda['Predictions'], label='Прогноз Nvidia')

# Установка названия графика и меток
plt_nvda.title('Прогноз цен на акции Nvidia')
plt_nvda.xlabel('Даты')
plt_nvda.ylabel('Цены')

# Установка частоты тиков по оси X, чтобы корректно отображать временной промежуток
plt_nvda.gca().xaxis.set_major_locator(mdates_nvda.DayLocator(interval=150))
plt_nvda.gcf().autofmt_xdate()

# Show the legend and plot the chart
plt_nvda.legend()
nvda_filename = "nvda.png"
plt_nvda.savefig(nvda_filename)

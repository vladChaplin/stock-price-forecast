import yfinance as yf_tsla
import pandas as pd_tsla
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt_tsla
import matplotlib.dates as mdates_tsla


# Прогноз на акции Apple
ticker_tsla = "TSLA"

# Парсинг данных от Yahoo Finance
data_tsla = yf_tsla.download(ticker_tsla, start="2016-01-01", end="2023-03-04")

# Создание нового DataFrame со столбцом «Adj Close»
df_tsla = pd_tsla.DataFrame(data_tsla["Adj Close"])

# Рассчитать 7-дневный ценовой тренд
df_tsla["PriceTrendApple"] = df_tsla["Adj Close"].rolling(window=7).mean().shift(1)

# Разделение данных на наборы для обучения и тестирования
train_data_tsla = df_tsla[:len(df_tsla) - 100]
test_data_tsla = df_tsla[len(df_tsla) - 100:]

# Заполнение всех пропущенных значений средним значением столбца.
train_data_tsla = train_data_tsla.fillna(train_data_tsla.mean())
test_data_tsla = test_data_tsla.fillna(test_data_tsla.mean())

# Обучение модели линейной регрессии на данных
X_train_tsla = train_data_tsla["PriceTrendApple"].values.reshape(-1, 1)
y_train_tsla = train_data_tsla["Adj Close"].values.reshape(-1, 1)
model_tsla = LinearRegression()
model_tsla.fit(X_train_tsla, y_train_tsla)

# Создание прогноза на основе тестовых данных
X_test_tsla = test_data_tsla["PriceTrendApple"].values.reshape(-1, 1)
predictions_tsla = model_tsla.predict(X_test_tsla)

# Создание DataFrame с датами и прогнозируемыми ценами
forecast_tsla = pd_tsla.DataFrame({'Date': test_data_tsla.index, 'Predictions': predictions_tsla.reshape(-1)})
# Объединение прогнозируемых DataFrame с исходным DataFrame
merged_tsla = pd_tsla.merge(df_tsla, forecast_tsla, how='outer', on='Date')

print(merged_tsla.tail(10))

# Выстраивание на графике истории цен
plt_tsla.plot(df_tsla.index, df_tsla['Adj Close'], label='Tesla')

# График прогнозируемых цен
plt_tsla.plot(merged_tsla['Date'], merged_tsla['Predictions'], label='Прогноз Tesla')

# Установка названия графика и меток
plt_tsla.title('Прогноз цен на акции')
plt_tsla.xlabel('Даты')
plt_tsla.ylabel('Цены')

# Установка частоты тиков по оси X, чтобы корректно отображать временной промежуток
plt_tsla.gca().xaxis.set_major_locator(mdates_tsla.DayLocator(interval=150))
plt_tsla.gcf().autofmt_xdate()

# Show the legend and plot the chart
plt_tsla.legend()
tesla_filename = "tesla.png"
plt_tsla.savefig(tesla_filename)


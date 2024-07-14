import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

################### Блок загрузки данных ###################

# Функция для загрузки данных из Excel файла
def load_data(file_path):
    return pd.read_excel(file_path, header=None)

# Пути к файлам
december_file_path = 'Analytics/Декабрь.xlsx'
january_file_path = 'Analytics/Январь.xlsx'

# Загрузка данных
df_december = load_data(december_file_path)
df_january = load_data(january_file_path)

################### Объединение данных ###################

# Транспонирование и объединение данных
df_december_t = df_december.T
df_january_t = df_january.T

# Объединение данных по строкам (сутки декабря и января)
df_combined = pd.concat([df_december_t, df_january_t])

################### Преобразование индексов в даты ###################

# Преобразуем индексы в формат дат
dates = pd.date_range(start='2023-12-01', periods=df_combined.shape[0], freq='D')
df_combined.index = dates

# Сохранение DataFrame в CSV файл
df_combined.to_csv('df_combined.csv')

################### Рассчет среднесуточных продаж ###################

# Рассчитываем среднесуточные продажи для каждого товара
average_daily_sales = df_combined.mean(axis=0)

# Округляем значения в меньшую сторону
average_daily_sales_rounded = np.floor(average_daily_sales)

print("Среднесуточные продажи для каждого товара (без округления):")
print(average_daily_sales)

print("Среднесуточные продажи для каждого товара (с округлением в меньшую сторону):")
print(average_daily_sales_rounded)

################### Отдельный расчет для декабря ###################

# Выделение данных за декабрь
df_december_only = df_combined.loc['2023-12-01':'2023-12-31']

# Рассчитываем среднесуточные продажи для каждого товара за декабрь
average_daily_sales_december = df_december_only.mean(axis=0)

# Округляем значения за декабрь в меньшую сторону
average_daily_sales_december_rounded = np.floor(average_daily_sales_december)

print("Среднесуточные продажи для каждого товара за декабрь (без округления):")
print(average_daily_sales_december)

print("Среднесуточные продажи для каждого товара за декабрь (с округлением в меньшую сторону):")
print(average_daily_sales_december_rounded)

################### Прогнозирование продаж ###################

# Функция для расчета прогнозов продаж на основе среднесуточных продаж
def forecast_sales(average_daily_sales, months, days_in_month):
    return average_daily_sales * days_in_month * months

# Количество дней в каждом месяце
days_in_march = 31
days_in_april = 30
days_in_may = 31

# Наименование товара

item_names = [
    "Зубная паста от КАРИЕСА и БАКТЕРИЙ 2 шт",
    "Антиперспирант женский шариковый 50мл х2",
    "МАСКА-СКРАБ Массажная PHARMACOS DEAD SEA",
    "Скраб для тела отшелушивание 600мл, 2 шт",
    "Крем обертывание для похудения 2 шуки",
    "Смягчающий крем для рук НАБОР увлажняющий 240 мл + пантенол",
    "Ночной питательный крем для рук с коллагеном, НАБОР 240 мл",
    "Восковые полоски для депиляции Воск эпиляция для чувствительной кожи Уход за кожей Набор для бикини",
    "Крем для лица FARMSTAY от морщин 80 мл",
    "Мыло для диспенсера с АЛОЭ ВЕРА 5 Л",
    "Набор носки женские 3 ПАРЫ",
    "Стиральный порошок автомат 6.5 кг",
    "Уличная гирлянда новогодняя ретро декор для праздника 15 м",
    "Коврик детский игровой развивающий складной двухсторонний",
    "Палатка детская игровая АВТОМАТИЧЕСКАЯ пляжная",
    "Фитолампа для растений лампа для рассады",
    "Сундук шкатулка для украшений с замком органайзер для колец",
    "Шоколад белый плиточный с кокосом и миндалем НАБОР 8 шт",
    "Кофе молотый Prodomo 1кг (500 грамм х2)"
]

# Прогнозируем продажи на март, апрель и май
forecast_march = forecast_sales(average_daily_sales_rounded, 1, days_in_march)
forecast_april = forecast_sales(average_daily_sales_rounded, 1, days_in_april)
forecast_may = forecast_sales(average_daily_sales_rounded, 1, days_in_may)

# Суммарный прогноз на три месяца
total_forecast = forecast_march + forecast_april + forecast_may

# Создание DataFrame с названиями товаров и прогнозами
forecast_df = pd.DataFrame({
    'Item': item_names,
    'Forecast_March': forecast_march,
    'Forecast_April': forecast_april,
    'Forecast_May': forecast_may,
    'Total_Forecast': total_forecast
})

# print("Прогноз продаж на три месяца:")
# print(forecast_df)

################### Прогнозирование с использованием ARIMA ###################

# Функция для прогнозирования продаж с использованием ARIMA
def arima_forecast(df, periods):
    forecasts = {}
    for item in df.columns:
        model = ARIMA(df[item], order=(5, 1, 0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=periods)
        forecasts[item] = forecast
    return pd.DataFrame(forecasts)

# Прогнозируем продажи на 3 месяца (90 дней)
arima_forecasts = arima_forecast(df_combined, 91)

# Разделяем прогнозы по месяцам
forecast_march_arima = arima_forecasts.iloc[:days_in_march]
forecast_april_arima = arima_forecasts.iloc[days_in_march:days_in_march + days_in_april]
forecast_may_arima = arima_forecasts.iloc[days_in_march + days_in_april:]

# Суммарный прогноз ARIMA на три месяца
total_forecast_arima = arima_forecasts.sum()

# Создание DataFrame с названиями товаров и прогнозами ARIMA
arima_forecast_df = pd.DataFrame({
    'Item': item_names,
    'ARIMA_Forecast_March': forecast_march_arima.sum().astype(int),
    'ARIMA_Forecast_April': forecast_april_arima.sum().astype(int),
    'ARIMA_Forecast_May': forecast_may_arima.sum().astype(int),
    'Total_ARIMA_Forecast': total_forecast_arima.astype(int)
})

print("ARIMA прогноз продаж на три месяца:")
print(arima_forecast_df)


# Визуализация прогнозов ARIMA
arima_forecasts.plot(figsize=(12, 8), title='ARIMA прогноз продаж на 3 месяца')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Функция для загрузки данных из Excel файла с первой строкой в качестве заголовков
def load_data(file_path):
    return pd.read_excel(file_path, header=0)

# Пути к файлам
december_file_path = 'Analytics/Книга11.xlsx'

# Загрузка данных
df = load_data(december_file_path)

# Преобразуем столбец 'Дата' к типу datetime
df['Дата'] = pd.to_datetime(df['Дата'], errors='coerce')

# Разделение данных на две части: до и после 11/02/2022
date_threshold = pd.to_datetime('2022-11-02')

# Фильтрация данных для двух периодов
df_before = df[df['Дата'] < date_threshold]
df_after = df[df['Дата'] >= date_threshold]

# Вычисление суммарных продаж и выручки для каждой части данных
total_sales_before = df_before['Количество продаж'].sum()
total_revenue_before = df_before['Выручка с продаж'].sum()

total_sales_after = df_after['Количество продаж'].sum()
total_revenue_after = df_after['Выручка с продаж'].sum()

# Вычисление количества дней в каждом периоде
days_before = (date_threshold - df_before['Дата'].min()).days
days_after = (df_after['Дата'].max() - date_threshold).days + 1  # +1 чтобы включить последний день

# Расчет среднесуточной выручки и среднесуточного объема продаж
avg_daily_revenue_before = total_revenue_before / days_before
avg_daily_sales_before = int(total_sales_before / days_before)

avg_daily_revenue_after = total_revenue_after / days_after
avg_daily_sales_after = int(total_sales_after / days_after)

# Вывод результатов
print("Данные до 11/02/2022:")
print(f"Суммарные продажи: {total_sales_before}")
print(f"Выручка: {total_revenue_before}")
print(f"Среднесуточный объем продаж: {avg_daily_sales_before}")
print(f"Среднесуточная выручка: {avg_daily_revenue_before}")
print(f"Количество суток в периоде: {days_before}")

print("\nДанные после 11/02/2022:")
print(f"Суммарные продажи: {total_sales_after}")
print(f"Выручка: {total_revenue_after}")
print(f"Среднесуточный объем продаж: {avg_daily_sales_after}")
print(f"Среднесуточная выручка: {avg_daily_revenue_after}")
print(f"Количество суток в периоде: {days_after}\n")

print(f"Общая выручка: {total_revenue_before + total_revenue_after}")
print(f"Общее количество продаж за период: {total_sales_before + total_sales_after}")

# Визуализация результатов
labels = ['До 11/02/2022', 'После 11/02/2022']
total_sales = [total_sales_before, total_sales_after]
total_revenue = [total_revenue_before, total_revenue_after]
avg_daily_revenue = [avg_daily_revenue_before, avg_daily_revenue_after]
avg_daily_sales = [avg_daily_sales_before, avg_daily_sales_after]

# График суммарных продаж
plt.figure(figsize=(10, 6))
plt.subplot(2, 2, 1)
plt.bar(labels, total_sales, color=['blue', 'green'])
plt.title('Суммарные продажи')
plt.ylabel('Количество продаж')

# График суммарной выручки
plt.subplot(2, 2, 2)
plt.bar(labels, total_revenue, color=['blue', 'green'])
plt.title('Суммарная выручка')
plt.ylabel('Выручка')

# График среднесуточного объема продаж
plt.subplot(2, 2, 3)
plt.bar(labels, avg_daily_sales, color=['blue', 'green'])
plt.title('Среднесуточный объем продаж')
plt.ylabel('Количество продаж')

# График среднесуточной выручки
plt.subplot(2, 2, 4)
plt.bar(labels, avg_daily_revenue, color=['blue', 'green'])
plt.title('Среднесуточная выручка')
plt.ylabel('Выручка')

plt.tight_layout()
plt.show()

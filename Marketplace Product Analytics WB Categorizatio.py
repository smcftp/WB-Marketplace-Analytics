import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных о продажах
df_sales = pd.read_csv('df_combined.csv', index_col=0, parse_dates=True)

# Словарь с наименованием товаров
products = {
    '0': 'Зубная паста от КАРИЕСА и БАКТЕРИЙ 2 шт',
    '1': 'Антиперспирант женский шариковый 50мл х2',
    '2': 'МАСКА-СКРАБ Массажная PHARMACOS DEAD SEA',
    '3': 'Скраб для тела отшелушивание 600мл, 2 шт',
    '4': 'Крем обертывание для похудения 2 шуки',
    '5': 'Смягчающий крем для рук НАБОР увлажняющий 240 мл + пантенол',
    '6': 'Ночной питательный крем для рук с коллагеном, НАБОР 240 мл',
    '7': 'Восковые полоски для депиляции Воск эпиляция для чувствительной кожи Уход за кожей Набор для бикини',
    '8': 'Крем для лица FARMSTAY от морщин 80 мл',
    '9': 'Мыло для диспенсера с АЛОЭ ВЕРА 5 Л',
    '10': 'Набор носки женские 3 ПАРЫ',
    '11': 'Стиральный порошок автомат 6.5 кг',
    '12': 'Уличная гирлянда новогодняя ретро декор для праздника 15 м',
    '13': 'Коврик детский игровой развивающий складной двухсторонний',
    '14': 'Палатка детская игровая АВТОМАТИЧЕСКАЯ пляжная',
    '15': 'Фитолампа для растений лампа для рассады',
    '16': 'Сундук шкатулка для украшений с замком органайзер для колец',
    '17': 'Шоколад белый плиточный с кокосом и миндалем НАБОР 8 шт',
    '18': 'Кофе молотый Prodomo 1кг (500 грамм х2)'
}

# Словарь с категориями спроса на товары
demand_categories = {
    'Зубная паста от КАРИЕСА и БАКТЕРИЙ 2 шт': '2',
    'Антиперспирант женский шариковый 50мл х2': '4',
    'МАСКА-СКРАБ Массажная PHARMACOS DEAD SEA': '3',
    'Скраб для тела отшелушивание 600мл, 2 шт': '1',
    'Крем обертывание для похудения 2 шуки': '1',
    'Смягчающий крем для рук НАБОР увлажняющий 240 мл + пантенол': '1',
    'Ночной питательный крем для рук с коллагеном, НАБОР 240 мл': '2',
    'Восковые полоски для депиляции Воск эпиляция для чувствительной кожи Уход за кожей Набор для бикини': '1',
    'Крем для лица FARMSTAY от морщин 80 мл': '1',
    'Мыло для диспенсера с АЛОЭ ВЕРА 5 Л': '3',
    'Набор носки женские 3 ПАРЫ': '2',
    'Стиральный порошок автомат 6.5 кг': '4',
    'Уличная гирлянда новогодняя ретро декор для праздника 15 м': '3',
    'Коврик детский игровой развивающий складной двухсторонний': '1',
    'Палатка детская игровая АВТОМАТИЧЕСКАЯ пляжная': '1',
    'Фитолампа для растений лампа для рассады': '2',
    'Сундук шкатулка для украшений с замком органайзер для колец': '1',
    'Шоколад белый плиточный с кокосом и миндалем НАБОР 8 шт': '1',
    'Кофе молотый Prodomo 1кг (500 грамм х2)': '1'
}

# Цены и маржа каждого товара
prices = [859, 445, 308, 409, 392, 443, 429, 358, 826, 449, 427, 1086, 1849, 2069, 1149, 931, 1449, 1426, 1334]
margins = [12, 14, 16, 25, 20, 20, 17, 15, 4, 20, 20, 17, 16, 30, 16, 20, 20, 17, 20]

# Общие продажи по каждому товару
total_sales = df_sales.sum()

# Рассчитываем доход и прибыль
revenue = total_sales * prices
profit = revenue * (np.array(margins) / 100)

# Создаем DataFrame для анализа
data = {
    'Product Name': [products[str(i)] for i in range(len(products))],
    'Total Sales': total_sales,
    'Price': prices,
    'Margin': margins,
    'Revenue': revenue,
    'Profit': profit
}
df_analysis = pd.DataFrame(data)

# ABC-анализ
total_revenue = df_analysis['Revenue'].sum()
df_analysis_sorted = df_analysis.sort_values(by='Revenue', ascending=False)

print(df_analysis_sorted)

df_analysis_sorted_len = len(df_analysis_sorted)
df_analysis_sorted['ABC Category'] = pd.cut(np.arange(len(df_analysis_sorted)), 
                                            bins=[-0.1, df_analysis_sorted_len * 0.2, df_analysis_sorted_len * 0.7, df_analysis_sorted_len + 0.1], 
                                            labels=['A', 'B', 'C'])


# Портфельный анализ
portfolio_analysis = df_analysis[['Revenue', 'Profit']].sum()

# Функция для извлечения категории спроса из названия продукта
def extract_demand_category(product_name):
    for key in demand_categories.keys():
        if key in product_name:
            return demand_categories[key]
    return None  # Возвращаем None, если категория спроса не найдена

# Добавление столбца с категорией спроса на основе функции extract_demand_category
df_analysis_sorted['Demand Category'] = df_analysis_sorted['Product Name'].apply(extract_demand_category)

# Создание столбца 'Combined Category' как конкатенации значений 'ABC Category' и 'Demand Category'
df_analysis_sorted['Combined Category'] = df_analysis_sorted['ABC Category'].astype(str) + df_analysis_sorted['Demand Category']

# Вывод результатов анализа
print("Анализ ассортимента и портфеля товаров:")
print(df_analysis_sorted)

print("\nПортфельный анализ:")
print(portfolio_analysis)

# Сохранение df_analysis_sorted в CSV файл только с нужными колонками
df_analysis_sorted[['Product Name', 'ABC Category']].to_csv('df_analysis_sorted.csv', index=False)

# Рекомендации по оптимизации прибыли
print("\nРекомендации по оптимизации прибыли:")
print("1. Оптимизация ассортимента")
print("  - Устранение неэффективных товаров: Рассмотрите возможность сокращения ассортимента товаров категории 'C'.")
print("  - Развитие лидирующих товаров: Инвестируйте в продвижение и улучшение качества товаров категории 'A'.")


##################################### Визуализация ####################################


# Визуализация результатов анализа
plt.figure(figsize=(10, 6))
plt.bar(df_analysis['Product Name'], df_analysis['Total Sales'])
plt.xlabel('Товары')
plt.ylabel('Общие продажи')
plt.title('Общие продажи по каждому товару')
plt.xticks(rotation=90)
plt.show()

# Визуализация ABC-анализа
abc_counts = df_analysis_sorted['ABC Category'].value_counts().sort_index()
plt.figure(figsize=(8, 6))
plt.bar(abc_counts.index, abc_counts.values)
plt.xlabel('ABC Категория')
plt.ylabel('Количество товаров')
plt.title('ABC-анализ товаров')
plt.show()

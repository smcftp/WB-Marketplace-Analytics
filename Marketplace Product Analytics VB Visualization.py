import pandas as pd
import matplotlib.pyplot as plt

# Словарь с товарами
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

# Загрузка данных из CSV файла
df = pd.read_csv('df_combined.csv', index_col=0)  

# Построение линейного графика для каждого товара
for column in df.columns:
    plt.figure(figsize=(10, 8))
    plt.plot(df.index, df[column], label=products[column], color='blue', marker='o')
    plt.title(f'Линейный график продаж для товара: {products[column]}')
    plt.xlabel('Дата')
    plt.ylabel('Количество продаж')
    plt.legend(title='Товар')
    plt.xticks(rotation=90)  # Поворот подписей на оси X
    plt.grid(True)
    plt.tight_layout()
    plt.show()

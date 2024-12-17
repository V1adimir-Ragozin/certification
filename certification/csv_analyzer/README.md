# PriceMachine

PriceMachine - это приложение для работы с файлами CSV, которое сканирует указанный каталог на наличие файлов с информацией о ценах, извлекает данные о товарах, ценах и весах, а также предоставляет возможность поиска и экспорта этих данных в HTML-формат.

## Описание функций

### Импорты
Импорт необходимых библиотек для работы с файлами и HTML.

```python
import os
import csv
import re
import tabulate
```

### Класс `PriceMachine`
Класс, содержащий основные методы для загрузки, поиска и экспорта данных.

#### Метод `__init__(self)`
Инициализирует пустой список для хранения данных.

```python
class PriceMachine:

    def __init__(self):
        self.data = []  # сохраняем полученные списки строк в список после применения условий и патернов
```

#### Метод `load_prices(self, directory)`
Сканирует указанный каталог на наличие CSV-файлов с информацией о ценах и извлекает данные о товарах, ценах и весах.

##### Параметры
- `directory` (str): Путь к каталогу.

##### Возвращаемое значение
- Заполняет `self.data` списками данных, соответствующими паттернам.

```python
    def load_prices(self, directory):
        '''
        Сканирует указанный путь к каталогу. Ищет файлы со словом price в названии.
        В файле ищет столбцы с названием товара, ценой и весом.
        Возвращает список из списков со строками удовлетворяющим патернам

        :param directory: file path from user_input
        :return: self.data = [[filename, product, price, weight, price/kg)]
        '''
        for filename in os.listdir(directory):
            if filename.endswith('.csv') and 'price' in filename.lower():
                with open(os.path.join(directory, filename), 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        for column in row:
                            if re.search(r'(товар|название|наименование|продукт)', column, re.IGNORECASE):
                                product = row[column].strip()
                            elif re.search(r'(розница|цена)', column, re.IGNORECASE):
                                price = float(row[column].replace(',', '.').strip())
                            elif re.search(r'(вес|масса|фасовка)', column, re.IGNORECASE):
                                weight = float(row[column].replace(',', '.').strip())
                        if product:
                            self.data.append([filename, product, price, weight, round(price / weight, 2)])
```

#### Метод `export_to_html(self, sorted_result)`
Экспортирует отсортированные данные в HTML-формат и выводит их в консоль.

##### Параметры
- `sorted_result` (list): Список данных для экспорта.

##### Возвращаемое значение
- Создает HTML-файл и выводит данные в консоль.

```python
    def export_to_html(self, sorted_result):
        '''
        Функция принимает подготовленный  список от поисковика search_ingine,
        добавляет заголовоки для таблицы, записывает файл и выводит в консоль
        :param sorted_result: list
         :return: write file *.html
        '''
        # Инициализируем  HTML
        result = '''
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8">
                <title>Позиции продуктов</title>
                </head>
                <body>
                <table>
                    <tr>
                        <th>Номер</th>
                        <th>Название</th>
                        <th>Цена</th>
                        <th>Фасовка</th>
                        <th>Файл</th>
                        <th>Цена за кг.</th>
                    </tr>
                '''
        index = 0  # нумеруем позиции
        for i in sorted_result:
            index += 1
            result += f'''
                <tr>
                    <td>{index}</td> 
                            <td>{i[1]}</td> 
                            <td>{i[2]}</td>
                            <td>{i[3]}{' кг'}</td>
                            <td>{i[0]}</td>
                            <td>{i[4]}</td>                        
                        </tr>
                    '''
        result += '''
        </table>
        </body>
        </html>
        '''
        with open('Out data.html', 'w', encoding='utf8') as file:
            file.write(result)

        # вывод в консоль:
        headers = ['№', 'Наименование', 'Цена', 'Вес', 'Цена\кг.', 'Файл']
        results_num = [[i + 1] + res[1:] + [res[0]] for i, res in enumerate(sorted_result)]  # нумеруем строчки
        print(tabulate.tabulate(results_num, headers=headers, tablefmt='simple'))
```

#### Метод `search_engine(self, input_text)`
Ищет заданное слово в данных и возвращает отсортированный результат поиска.

##### Параметры
- `input_text` (str): Текст для поиска.

##### Возвращаемое значение
- (list): Отсортированный список результатов поиска.

```python
    def search_engine(self, input_text):
        '''
        Ищет переданное слово от пользователя в списке от load_price(self.data)
        Возвращает отсортированный результат поиска на экспорт и в консоль
        :param input_text: value(text) from user_input_find_text
        :return: sorted_results
        '''
        results = []
        for row in self.data:
            if re.search(input_text, row[1], re.IGNORECASE):  # поиск по столбцу с названием
                results.append(row)
        sorted_results = sorted(results, key=lambda x: x[4])  # сортировка по цене за кг
        self.export_to_html(sorted_results)  # передаем остротированный результат на экспорт
```

#### Метод `user_input(self, file_path)`
Запрашивает у пользователя ввод и выполняет поиск по данным.

##### Параметры
- `file_path` (str): Путь к каталогу с файлами.

##### Возвращаемое значение
- None

```python
    def user_input(self, file_path):
        """
        Функция осуществляет ввод пользователя и передает искомое значение в поисковик search_engine
        А так же принимает абсолютный путь к папке с файлами и передает в загрузчик load_prices

        :param file_path: file path
        :return: value(text)
        """
        self.load_prices(file_path)  # передаем путь папки в загрузчик load_prices

        while True:
            find_text_value = input('Что найти ("exit" или "выход" чтобы закончить работу) ?: \n')
            if find_text_value.lower() == 'exit' или find_text_value.lower() == 'выход':
                print('Поиск завершен')
                break
            self.search_engine(find_text_value)  # передаем введненное слово в поисковик
```

### Основной блок
Создает экземпляр класса `PriceMachine` и запускает основной процесс.

```python
if __name__ == '__main__':
    pm = PriceMachine()
    local_directory = os.path.dirname(os.path.abspath(__file__))  # абсолютный путь к файлам
    pm.user_input(local_directory)
```



# Задача:
## Написать анализатор прайс-листов.

### Описание и требования:
В папке находятся несколько файлов, содержащих прайс-листы от разных поставщиков.
Количество и название файлов заранее неизвестно, однако точно известно, что в названии файлов прайс-листов есть слово "price".
Файлы, не содержащие слово "price" следует игнорировать.
Формат файлов: данные, разделенные точкой с запятой.
Порядок колонок в файле заранее неизвестен, но известно, что столбец с названием товара называется одним из вариантов: "название", "продукт", "товар", "наименование".
Столбец с ценой может называться "цена" или "розница".
Столбец с весом имеет название "фасовка", "масса" или "вес" и всегда указывается в килограммах.
Остальные столбцы игнорировать.

### Особенности реализации:
Программа должна загрузить данные из всех прайс-листов и предоставить интерфейс для поиска товара по фрагменту названия с сорторовкой по цене за килогорамм.
Интерфейс для поиска реализовать через консоль, циклически получая информацию от пользователя.
Если введено слово "exit", то цикл обмена с пользователем завершается, программа выводит сообщение о том, что работа закончена и завершает свою работу. В противном случае введенный текст считается текстом для поиска. Программа должна вывести список найденных позиций в виде таблицы:

```№   Наименование               цена вес   файл   цена за кг.
1   филе гигантского кальмара         617  1 price_0.csv 617.0
2   филе гигантского кальмара         639  1 price_4.csv 639.0
3   филе гигантского кальмара         639  1 price_6.csv 639.0
4   филе гигантского кальмара         683  1 price_1.csv 683.0
5   филе гигантского кальмара         1381  2 price_5.csv 690.5
6   кальмар тушка                   3420  3 price_3.csv 1140.0
7   кальмар тушка                   4756  4 price_0.csv 1189.0```


Список должен быть отсортирован по возрастанию стоимости за килограмм.

Предусмотреть вывод массива данных в текстовый файл в формате html.

import os
import csv
import re
import tabulate


class PriceMachine:

    def __init__(self):
        self.data = []  # сохраняем полученные списки строк в список после применения условий и патернов

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
            if find_text_value.lower() == 'exit' or find_text_value.lower() == 'выход':
                print('Поиск завершен')
                break
            self.search_engine(find_text_value)  # передаем введненное слово в поисковик


if __name__ == '__main__':
    pm = PriceMachine()
    local_directory = os.path.dirname(os.path.abspath(__file__))  # абсолютный путь к файлам
    pm.user_input(local_directory)

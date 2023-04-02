from bs4 import BeautifulSoup
import os

files = os.listdir('detail_pages')
abs_files = ['detail_pages/{0}'.format(f) for f in files]
for abs_file in abs_files:
    with open(abs_file, 'r', encoding='utf-8') as r:
        soup = BeautifulSoup(r.read(), 'lxml')
        name = soup.find(class_='h30').text
        items = soup.find(class_='table').text.split('\n')
        info_dict = {item.split('：')[0]: item.split('：')[1] for item in items if item}
        info_dict['项目名称'] = name
        text_content = soup.find_all(class_='text')
        print(text_content[1].text)
        exit(0)

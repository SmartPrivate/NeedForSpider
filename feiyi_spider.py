import db_tool
import spider_tool
import requests
import json
import time
from tqdm import tqdm
import os
import redis


def spider_by_request():
    header = spider_tool.get_header()
    redis_cli = redis.Redis(host='127.0.0.1', port=6379, db=0)
    project_ids = redis_cli.lrange('project_ids', 0, -1)
    project_ids = list(map(lambda o: str(o, encoding='utf-8'), project_ids))
    project_ids = [project_id for project_id in project_ids if not os.path.exists('detail_pages/{0}.html'.format(project_id))]
    for project_id in tqdm(project_ids):
        if os.path.exists('detail_pages/{0}.html'.format(project_id)):
            continue
        detail_url = 'https://www.ihchina.cn/project_details/{0}'.format(project_id)
        with open('detail_pages/{0}.html'.format(project_id), 'w', encoding='utf-8') as writer:
            detail_page = requests.get(url=detail_url, headers=header).text
            writer.write(detail_page)
        time.sleep(0.5)


def set_id_list_to_redis():
    redis_cli = redis.Redis(host='127.0.0.1', port=6379, db=0)
    header = spider_tool.get_header()
    base_url = 'https://www.ihchina.cn/Article/Index/getProject.html'
    params_dict = dict(provice='', rx_time='', type='', cate='', keywords='', category_id=16, limit=10)
    for i in tqdm(range(361)):
        page_index = i + 1
        params_dict['p'] = page_index
        r = requests.get(url=base_url, headers=header, params=params_dict)
        r_text_json = json.loads(r.text)
        project_id_list = [project_id['id'] for project_id in r_text_json['list']]
        for project_id in project_id_list:
            redis_cli.lpush('project_ids', project_id)
        time.sleep(0.5)


spider_by_request()

from tqdm import tqdm
import pymongo

word2vec_file = 'D:/DataSet/tencent-ailab-embedding-zh-d200-v0.2.0/tencent-ailab-embedding-zh-d200-v0.2.0.txt'  # 源文件路径
insert_batch_size = 10000  # 批量插入大小
total_words = 12287936  # 总单词数
db_name = 'word2vec_db'  # 数据库名称
collection_name = 'tencent_chinese_word2vec'  # 集合名称

session = pymongo.MongoClient()
db = session.get_database(db_name)
collection = db.get_collection(collection_name)
collection.create_index('word', unique=True)

with open(word2vec_file, 'r', encoding='utf-8') as f:
    f.readline()
    insert_dicts = []
    for i in tqdm(range(total_words)):
        line = f.readline().strip('\n').split(' ')
        word = line[0]
        vector = [float(v) for v in line[1:]]
        insert_dicts.append(dict(word=word, vector=vector))
        if len(insert_dicts) < insert_batch_size:
            continue
        collection.insert_many(insert_dicts)
        insert_dicts.clear()

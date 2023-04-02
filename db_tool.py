import pymongo


class MongoSessionHelper:
    def __init__(self, host='127.0.0.1', port=27017):
        self.__host = host
        self.__port = port
        self.__session = pymongo.MongoClient(host=self.__host, port=self.__port)

    def get_active_session(self):
        """
        获取新连接
        :return: 一个激活的mongodb session
        """
        return self.__session

    def get_active_db(self, db_name: str):
        """
        获取数据库
        :param db_name: 数据库名称
        :return: 一个激活的mongodb db session
        """
        return self.__session.get_database(db_name)

    def get_active_collection(self, db_name: str, collection_name: str):
        """
        获取集合
        :param db_name: 数据库名称
        :param collection_name: 集合名称
        :return: 一个激活的mongodb collection session
        """
        return self.__session.get_database(db_name).get_collection(collection_name)

    def get_all_data(self, db_name: str, collection_name: str) -> [dict]:
        """
        返回集合中所有数据
        :param db_name: 数据库名称
        :param collection_name: 集合名称
        :return: 数据全集
        """
        return list(self.__session.get_database(db_name).get_collection(collection_name).find())

    def get_one_column_data(self, db_name: str, collection_name: str, column_name: str):
        return [item[column_name] for item in self.get_all_data(db_name=db_name, collection_name=collection_name)]

    def get_chinese_stopwords_list(self) -> [str]:
        """
        获取中文停止词列表
        :return: 中文停止词list
        """
        return self.get_one_column_data(db_name='tools_db', collection_name='chinese_stopwords', column_name='word')

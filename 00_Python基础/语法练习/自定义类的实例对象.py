class BigList:  # 类名：大驼峰
    def __init__(self, game_list):  # 实例名：全小写+下划线
        self._data = game_list


A = BigList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
B = BigList(["xyx", "xyl"])

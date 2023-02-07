class Product:
    def __init__(self, id, name, price, total, remain):
        self.__id = id
        self.__name = name
        self.__price = price
        self.__total = total
        self.__remain = remain

    def display(self):
        print("商品序号：", self.__id)
        print("商品名：", self.__name)
        print("单价：", self.__price)
        print("总数量：", self.__total)
        print("剩余数量：", self.__remain)

    def income(self):
        return (self.__total - self.__remain) * self.__price

    def setdata(self, id=None, name=None, price=None, total=None, remain=None):
        if id:
            self.__id = id
        if name:
            self.__name = name
        if price:
            self.__price = price
        if total:
            self.__total = total
        if remain:
            self.__remain = remain

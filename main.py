class Node:

    def __init__(self, val, left=None, right=None, chooser=None):
        self.__chooser__ = chooser
        self.__val__ = val
        self.__left__ = left
        self.__right__ = right
        if left is not None or right is not None:
            self.__val__ = self.choose(self.__left__, self.__right__, self.__chooser__)

    @classmethod
    def choose(cls, left, right, chooser=None):
        if isinstance(left, Node):
            left = left.__val__
        if isinstance(right, Node):
            right = right.__val__
        if left is None and right is None:
            return None
        elif left is None:
            return right
        elif right is None:
            return left
        else:
            return chooser(left, right)

    @classmethod
    def build(cls, data, left=None, right=None, chooser=None):
        if left is None:
            left, right = 0, len(data)
        data = iter(data)
        if chooser is None:
            return None
        if right is None:
            left, right = 0, left
        if left + 1 == right:
            return cls(next(data))
        middle = (left + right) // 2
        return cls(
            None,
            cls.build(data, left, middle, chooser),
            cls.build(data, middle, right, chooser),
            chooser
        )

    def update(self, index, val, left, right=None):
        if right is None:
            left, right = 0, left
        if index < left or index >= right:
            return self.__val__
        if left + 1 == right:
            self.__val__ = val
            return self.__val__
        middle = (left + right) // 2
        self.__val__ = self.choose(
            self.__left__.update(index, val, left, middle),
            self.__right__.update(index, val, middle, right),
            self.__chooser__
        )
        return self.__val__

    def query(self, query_left, query_right, left, right=None):
        if right is None:
            left, right = 0, left
        if right <= query_left or left >= right:
            return None
        if left >= query_left and right <= query_right:
            return self.__val__
        middle = (left + right) // 2
        left_res, right_res = None, None
        if self.__left__ is not None:
            left_res = self.__left__.query(query_left, query_right, left, middle)
        if self.__right__ is not None:
            right_res = self.__right__.query(query_left, query_right, middle, right)
        return self.choose(left_res, right_res, self.__chooser__)

    def __str__(self):
        if self.__left__ is not None or self.__right__ is not None:
            return f'{self.__val__} ({self.__left__}, {self.__right__})'
        return f'{self.__val__}'

# data = list(map(int, input().split()))
# t_max = Node.build(data, chooser=max)
# t_min = Node.build(data, chooser=min)
# t_sum = Node.build(data, chooser=lambda x, y: x + y)

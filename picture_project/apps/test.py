class User:
    def __init__(self):
        self._name = None

    @property
    def name(self):
        print("ゲッターが呼ばれました")
        return self._name

    @name.setter
    def name(self, value):
        print("セッターが呼ばれました")
        if not isinstance(value, str):
            raise ValueError("名前は文字列で指定してください")
        self._name = value


u = User()
u.name = "Alice"  # セッターが呼ばれる
print(u.name)  # ゲッターが呼ばれる

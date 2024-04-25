class NumericEncoder(dict):
    """scikit-learnの`LabelEncoder`のオマージュ. 通称: 座標圧縮.

    Args:
        dict (_type_): _description_
    """

    def __init__(self):
        pass

    def fit(self, a: list[int]):
        self.a = sorted(set(a))
        super().__init__(dict(zip(self.a, range(len(self.a)))))
        return self

    def decode(self, index: int) -> int:
        return self.a[index]

    def transform(self, raw_values: list[int]) -> list[int]:
        return [self[raw_value] for raw_value in raw_values]
    
    def fit_transform(self, a: list[int]):
        self.fit(a)
        return self.transform(a)

    def __call__(self, raw_value: int) -> int:
        return self[raw_value]

    def __len__(self) -> int:
        return len(self.a)
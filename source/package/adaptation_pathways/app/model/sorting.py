class SortingInfo:
    def __init__(
        self,
        sort_key: str | None = None,
        ascending=True,
    ):
        self.sort_key = sort_key
        self.ascending = ascending

class ColumnProfile:
    def __init__(self, name: str, inferred_type: str, total: int, missing: int, non_empty: int):
        self.name = name
        self.inferred_type = inferred_type
        self.total = total  # total number of entries
        self.missing = missing
        self.non_empty = non_empty              

  

    def to_dict(self) -> dict:
        return {
        "name": self.name,
        "inferred_type": self.inferred_type,
        "total": self.total,
        "missing": self.missing,
        "non_empty": self.non_empty,
        }
    
    def __repr__(self) -> str:
        return (
        f"ColumnProfile(name={self.name!r}, type={self.inferred_type!r}, "
        f"missing={self.missing}, total={self.total}, unique={self.unique})"
        )
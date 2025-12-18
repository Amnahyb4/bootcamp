def basic_profile(rows: list[dict[str, str]]) -> dict:
    if not rows:
        return {"source": None, "summary": {"rows": 0, "columns": 0}, "columns": {}, "notes": ["Empty dataset"]}

    MISSING = {"", "na", "n/a", "null", "none", "nan"}

    def is_missing(value: str | None) -> bool:
        if value is None:
            return True
        return value.strip().lower() in MISSING

    def try_float(value: str | None) -> float | None:
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def infer_type(values: list[str]) -> str:
        usable = [v for v in values if not is_missing(v)]
        if not usable:
            return "text"
        for v in usable:
            if try_float(v) is None:
                return "text"
        return "number"

    def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
        return [row.get(col, "") for row in rows]

    def numeric_stats(values: list[str]) -> dict:
        usable = [v for v in values if not is_missing(v)]
        if not usable:
            return {}

        nums: list[float] = []
        for v in usable:
            f = try_float(v)
            if f is None:
                return {}
            nums.append(f)

        count = len(nums)
        return {
            "count": count,
            "unique": len(set(nums)),
            "mean": sum(nums) / count,
            "min": min(nums),
            "max": max(nums),
        }

    def text_stats(values: list[str], top_k: int = 5) -> dict:
        usable = [v for v in values if not is_missing(v)]
        missing_count = len(values) - len(usable)

        counts: dict[str, int] = {}
        for v in usable:
            counts[v] = counts.get(v, 0) + 1

        top_items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
        top = [{"value": v, "count": c} for v, c in top_items[:top_k]]

        return {
            "count": len(usable),
            "missing": missing_count,
            "unique": len(counts),   # helpful for the table
            "top": top,
        }

    columns = list(rows[0].keys())

    # counts needed for missing %
    missing = {c: 0 for c in columns}
    non_empty = {c: 0 for c in columns}

    for row in rows:
        for c in columns:
            v = row.get(c)
            if is_missing(v):
                missing[c] += 1
            else:
                non_empty[c] += 1

    report_columns: dict = {}
    total_rows = len(rows)
    for c in columns:
        vals = column_values(rows, c)
        col_type = infer_type(vals)
        stats = numeric_stats(vals) if col_type == "number" else text_stats(vals)

        report_columns[c] = {
            "type": col_type,
            "missing": missing[c],
            "non_empty": non_empty[c],
            "stats": stats,
            "missing_pct": (missing[c] / total_rows) * 100 if total_rows else 0.0,
            "unique": stats.get("unique", 0),

        }

    return {
        "source": None,
        "summary": {
            "rows": len(rows),
            "columns": len(columns),
        },
        "columns": report_columns,
    }



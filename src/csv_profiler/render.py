from __future__ import annotations
from pathlib import Path
import json

def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    summary = report.get("summary", {})
    cols = report.get("columns", {})

    total_rows = int(summary.get("rows", 0) or 0)
    total_cols = int(summary.get("columns", 0) or 0)

    lines: list[str] = []
    lines.append("# CSV report profiling\n\n")
    lines.append(f"- Rows: **{total_rows}**\n")
    lines.append(f"- Columns: **{total_cols}**\n\n")

    # Table (summary)
    lines.append("## Columns (summary)\n\n")
    lines.append("| Column | Type | Missing % | Unique |\n")
    lines.append("|---|---|---:|---:|\n")

    for col, info in cols.items():
        col_type = info.get("type", "text")
        missing_pct = info.get("missing_pct", 0.0)
        unique = info.get("unique", 0)

        lines.append(f"| {col} | {col_type} | {missing_pct:.1f}% | {unique} |\n")

    # Details
    lines.append("\n## Columns (details)\n\n")

    for col, info in cols.items():
        col_type = info.get("type", "text")
        stats = info.get("stats", {})

        lines.append(f"### {col}\n\n")
        lines.append(f"- Type: **{col_type}**\n")
        lines.append(f"- Missing: **{info.get('missing', 0)}**\n")
        lines.append(f"- Non-empty: **{info.get('non_empty', 0)}**\n")

        if col_type == "number":
            lines.append(f"- Min: **{stats.get('min', '')}**\n")
            lines.append(f"- Max: **{stats.get('max', '')}**\n")
            lines.append(f"- Mean: **{stats.get('mean', '')}**\n")
            lines.append(f"- Unique: **{stats.get('unique', '')}**\n")
            lines.append(f"- Count: **{stats.get('count', '')}**\n")
        else:
            lines.append(f"- Unique: **{stats.get('unique', '')}**\n")
            lines.append(f"- Count: **{stats.get('count', '')}**\n")
            lines.append("\nTop values:\n")
            top = stats.get("top", [])
            if not top:
                lines.append("- (none)\n")
            else:
                for item in top:
                    lines.append(f"- {item.get('value')}: {item.get('count')}\n")

        lines.append("\n")

    path.write_text("".join(lines), encoding="utf-8")


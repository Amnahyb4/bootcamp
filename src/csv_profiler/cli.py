import json
import time
import typer
from pathlib import Path
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile  
from csv_profiler.render import write_json, write_markdown

app = typer.Typer()

@app.command(help="Profile a CSV file and generate reports (JSON and Markdown).")
def profile(
    input_path:Path=typer.Argument(...,help="Path to the input CSV file."),
    output_dir:Path=typer.Option(Path("outputs"),"--output-dir",help=" output folder" ),
    report_name: str = typer.Option("report", "--report-name", help="Base name for the output reports:"),
    preview: bool = typer.Option(False, "--preview", help="Print a short summary:"),
):
    typer.echo(f"Profiling {input_path}...")
    typer.echo(f"Reports will be saved to {output_dir}")
    typer.echo(f"Report base name: {report_name}")
    typer.echo(f"Preview mode: {'ON' if preview else 'OFF'}")

    try:
        t0=time.perf_counter()
        rows=read_csv_rows(input_path)
        report=basic_profile(rows)
        t1 = time.perf_counter_ns()
        report["timing_ms"] = (t1 - t0) / 1_000_000

        output_dir.mkdir(Parents=True,exist_ok=True)

        json_path = output_dir / f"{report_name}.json"
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        typer.secho(f"Wrote {json_path}", fg=typer.colors.GREEN)

        md_path = output_dir / f"{report_name}.md"
        md_path.write_text(write_markdown(report, md_path), encoding="utf-8")
        typer.secho(f"Wrote {md_path}", fg=typer.colors.GREEN)

        if preview:
            typer.echo(f"Rows: {report['n_rows']} | Cols: {report['n_cols']} | {report['timing_ms']:.2f}ms")

    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)





if __name__ == "__main__":
    app()   ##work as CLI tool 





import typer
import re
import importlib

app = typer.Typer()

@app.command("solve")
def solve(file: str):
    """Solve a day's challenge based on filename"""
    day = int(re.findall("\d+", file)[0])
    module = importlib.import_module(f"aoc2018.day{day}")
    print("Part 1:", getattr(module, 'part1')())
    print("Part 2:", getattr(module, 'part2')())

def main():
    app()

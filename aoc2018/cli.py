import typer
import re
import importlib

app = typer.Typer()

@app.command("solve")
def solve(file: str):
    """Solve a day's challenge"""
    day = int(re.findall("\d+", "inputs/day01.txt")[0])
    module = importlib.import_module('aoc2018.day1')
    print("Part 1:", getattr(module, 'part1')())
    print("Part 2:", getattr(module, 'part2')())

def main():
    app()
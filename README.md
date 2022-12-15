# Advent of Code '22

![](https://img.shields.io/badge/day%20📅-15-blue) ![](https://img.shields.io/badge/stars%20⭐-28-yellow) ![](https://img.shields.io/badge/days%20completed-14-red) [![Update AoC Badges](https://github.com/nryabykh/aoc2022/actions/workflows/main.yml/badge.svg)](https://github.com/nryabykh/aoc2022/actions/workflows/main.yml)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aoc2022-nriabykh.streamlit.app/)

<img src="images/banner.jpeg" width="800" alt="AoC2000 banner"/>


My solutions of [Advent of Code 2022](https://adventofcode.com/2022).

- Inputs: `./input`
- Code: `./solutions`

## Usage

`Main.py` reads input from `./input/<day>.txt` file by default. You can specify a custom input file with `-i`.

```bash
usage: main.py [-h] [-d DAY] [-i INPUT] [-t]

options:
  -h, --help            show this help message and exit
  -d DAY, --day DAY     Number of day (from 1 to 25)
  -i INPUT, --input INPUT
                        Relative path to custom input file
  -t, --test            Use test data


example: 
python3 main.py -d 6
python3 main.py -d 9 -i ./path/to/input/file.txt
```

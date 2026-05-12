#!/usr/bin/env python3

import sys
from pathlib import Path

from uvs_nirmana.solution import (
    LEVELS,
    InvalidMetricError,
    InvalidSolutionError,
    Solution,
)

valid_sols = []
for filepath in map(Path, sys.argv[1:]):
    with open(filepath, "rb") as f:
        sol = Solution.parse(f)
    if sol.level_id not in LEVELS:
        continue
    level = LEVELS[sol.level_id]
    try:
        sol.check_all()
    except InvalidSolutionError as e:
        print(f"Error: {filepath.name}: {e}")
    except InvalidMetricError as e:
        print(f"Skipping: {filepath.name}: {e}")
    else:
        index = int(filepath.stem.removeprefix(level.prefix + "-"))
        valid_sols.append((sol, index))

for sol, index in sorted(
    valid_sols, key=lambda x: (x[0].level.order if x[0].level else 0, x[1])
):
    print(f"{sol.level}, solution {index}: {sol.get_metrics()}")

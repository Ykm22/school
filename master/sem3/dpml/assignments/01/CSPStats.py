from dataclasses import dataclass


@dataclass
class CSPStats:
    """Statistics for CSP solver performance"""

    nodes_visited: int = 0
    backtracks: int = 0
    constraint_checks: int = 0
    time_elapsed: float = 0.0
    solution_found: bool = False

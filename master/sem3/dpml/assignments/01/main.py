import json
from typing import Dict, Tuple, Any, Optional

from CSPSolver import CSPSolver


def load_problem_from_json(filename: str) -> Tuple[CSPSolver, Dict[str, Any]]:
    """Load CSP problem from JSON and create solver"""
    with open(filename, "r") as f:
        data = json.load(f)

    variables = data["variables"]

    # Convert domain keys to match variable types
    # JSON converts integer keys to strings, so we need to handle this
    domains = {}
    for var in variables:
        # Try to find the domain with the matching key (as string or as-is)
        if var in data["domains"]:
            domains[var] = data["domains"][var]
        elif str(var) in data["domains"]:
            domains[var] = data["domains"][str(var)]
        else:
            raise ValueError(f"No domain found for variable {var}")

    # Process constraints
    constraints = []
    for constraint_def in data["constraints"]:
        constraint = {
            "type": constraint_def["type"],
            "variables": constraint_def["variables"],
        }

        # Handle custom constraints with Python expressions
        if constraint_def["type"] == "custom" and "expression" in constraint_def:
            expr = constraint_def["expression"]
            var_names = constraint_def["variables"]

            # Create lambda parameters as v0, v1, v2, etc.
            param_names = [f"v{i}" for i in range(len(var_names))]
            lambda_str = f"lambda {', '.join(param_names)}: {expr}"

            constraint["function"] = eval(lambda_str)

        constraints.append(constraint)

    solver = CSPSolver(variables, domains, constraints)

    return solver, data


def print_solution(data: Dict[str, Any], solution: Optional[Dict[Any, Any]]):
    """Pretty print the solution based on visualization info in JSON"""
    if solution is None:
        print("No solution found!")
        return

    print("\n=== Solution ===")

    viz_type = data.get("visualization", {}).get("type")

    if viz_type == "mapping":
        # Key-value mapping (for Graph Coloring)
        print("Assignments:")
        for var in sorted(solution.keys(), key=str):
            print(f"  {var}: {solution[var]}")

    elif viz_type == "logic_puzzle":
        # Logic puzzle visualization - organize by houses
        print("\nHouse Layout:")
        print("-" * 70)

        # Extract number of houses from variable names
        houses = set()
        for var in solution.keys():
            if "house" in str(var):
                house_num = str(var).split("_")[0].replace("house", "")
                houses.add(int(house_num))

        for house_num in sorted(houses):
            print(f"\nHouse {house_num}:")
            for key in sorted(solution.keys()):
                if key.startswith(f"house{house_num}_"):
                    attribute = key.split("_", 1)[1]
                    value = solution[key]
                    print(f"  {attribute.capitalize()}: {value}")

        # Answer the questions
        print("\n" + "=" * 70)
        print("ANSWERS:")
        print("=" * 70)

        # For zebra puzzle: Who drinks water? Who owns the zebra?
        water_drinker = None
        zebra_owner = None

        for house_num in sorted(houses):
            if solution.get(f"house{house_num}_drink") == "water":
                water_drinker = solution.get(f"house{house_num}_national")
            if solution.get(f"house{house_num}_pet") == "zebra":
                zebra_owner = solution.get(f"house{house_num}_national")

        if water_drinker:
            print(f"Who drinks water? {water_drinker}")
        if zebra_owner:
            print(f"Who owns the zebra? {zebra_owner}")

        # Also check for LM smoker and dog owner (3-house puzzle)
        lm_smoker = None
        dog_owner = None

        for house_num in sorted(houses):
            if solution.get(f"house{house_num}_cigarette") == "LM":
                lm_smoker = solution.get(f"house{house_num}_national")
            if solution.get(f"house{house_num}_pet") == "dog":
                dog_owner = solution.get(f"house{house_num}_national")

        if lm_smoker:
            print(f"Who smokes LM? {lm_smoker}")
        if dog_owner:
            print(f"Who has the dog? {dog_owner}")
    else:
        # Default: just print assignment
        print("Assignment:")
        for var, val in sorted(solution.items(), key=lambda x: str(x[0])):
            print(f"  {var} = {val}")


def main():
    problems = [
        "problems/einstein_zebra_puzzle_3_houses.json",
        "problems/graph_coloring.json",
    ]

    # Set verbose mode
    verbose = False

    for filename in problems:
        print(f"\n{'=' * 70}")

        solver, problem_data = load_problem_from_json(filename)

        print(f"Problem: {problem_data.get('name', 'Unknown')}")
        print(f"Description: {problem_data.get('description', 'N/A')}")
        print(f"{'=' * 70}")

        # Display constraint graph size
        nodes, edges = solver.get_constraint_graph_size()
        print(f"\nConstraint Graph: {nodes} nodes, {edges} edges")
        print(f"Variables: {len(solver.variables)}")
        print(f"Constraints: {len(solver.constraints)}")

        # Display original domain info
        solver.print_domain_info("Original")

        # Test 1: Plain Backtracking
        print(f"\n{'-' * 70}")
        print("METHOD 1: Plain Backtracking (Baseline)")
        print(f"{'-' * 70}")
        solution = solver.solve_backtracking(verbose)
        print_solution(problem_data, solution)
        solver.print_stats("Plain Backtracking")

        # # Test 2: Node Consistency + Backtracking
        print(f"\n{'-' * 70}")
        print("METHOD 2: Node Consistency + Backtracking")
        print(f"(Problem Reduction Method)")
        print(f"{'-' * 70}")
        solution = solver.solve_with_preprocessing("node_consistency", verbose)
        solver.print_domain_info("After Node Consistency")
        print_solution(problem_data, solution)
        solver.print_stats("Node Consistency + Backtracking")

        # Test 3: Arc Consistency + Backtracking
        print(f"\n{'-' * 70}")
        print("METHOD 3: Arc Consistency (AC-3) + Backtracking")
        print(f"(Problem Reduction Method)")
        print(f"{'-' * 70}")
        solution = solver.solve_with_preprocessing("arc_consistency", verbose)
        solver.print_domain_info("After Arc Consistency")
        print_solution(problem_data, solution)
        solver.print_stats("Arc Consistency + Backtracking")

        # Test 4: Forward Checking
        print(f"\n{'-' * 70}")
        print("METHOD 4: Forward Checking")
        print(f"(Basic Search Strategy - from ch05-basic-search.pdf)")
        print(f"{'-' * 70}")
        solution = solver.solve_forward_checking(verbose)
        print_solution(problem_data, solution)
        solver.print_stats("Forward Checking")

        # Test 5: Min-Conflicts
        print(f"\n{'-' * 70}")
        print("METHOD 5: Min-Conflicts")
        print(f"(Stochastic Search Method - from ch08-stochastic-search.pdf)")
        print(f"{'-' * 70}")
        solution = solver.solve_min_conflicts(max_steps=10000, verbose=verbose)
        print_solution(problem_data, solution)
        solver.print_stats("Min-Conflicts")


if __name__ == "__main__":
    main()

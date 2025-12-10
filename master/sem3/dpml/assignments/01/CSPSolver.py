import time
from typing import List, Dict, Set, Tuple, Any, Optional

from CSPStats import CSPStats


class CSPSolver:
    """Generic CSP solver - problem agnostic"""

    def __init__(
        self,
        variables: List[Any],
        domains: Dict[Any, List[Any]],
        constraints: List[Dict[str, Any]],
    ):
        """
        Initialize CSP solver with:
        - variables: list of variable identifiers
        - domains: dict mapping each variable to its possible values
        - constraints: list of constraint definitions
        """
        self.variables = variables
        self.original_domains = {var: list(domain) for var, domain in domains.items()}
        self.domains = {var: list(domain) for var, domain in domains.items()}
        self.constraints = constraints
        self.stats = CSPStats()

        # Build constraint graph
        self.neighbors = self._build_neighbor_graph()

    def _build_neighbor_graph(self) -> Dict[Any, Set[Any]]:
        """Build adjacency list of which variables constrain each other"""
        neighbors = {var: set() for var in self.variables}

        for constraint in self.constraints:
            involved_vars = constraint["variables"]
            # Each variable in constraint is neighbor to all others
            for var in involved_vars:
                for other_var in involved_vars:
                    if var != other_var:
                        neighbors[var].add(other_var)

        return neighbors

    def is_consistent(self, var: Any, value: Any, assignment: Dict[Any, Any]) -> bool:
        """Check if assigning value to var satisfies all constraints"""
        self.stats.constraint_checks += 1

        for constraint in self.constraints:
            if var not in constraint["variables"]:
                continue

            # Check if all variables in this constraint are assigned
            involved_vars = constraint["variables"]
            if not all(v in assignment or v == var for v in involved_vars):
                continue

            # Build values tuple for constraint check
            temp_assignment = assignment.copy()
            temp_assignment[var] = value

            if not self._check_constraint(constraint, temp_assignment):
                return False

        return True

    def _check_constraint(
        self, constraint: Dict[str, Any], assignment: Dict[Any, Any]
    ) -> bool:
        """Evaluate a constraint given current assignment"""
        constraint_type = constraint["type"]
        involved_vars = constraint["variables"]

        # Check if all required variables are assigned
        if not all(v in assignment for v in involved_vars):
            return True  # Can't violate if not all assigned

        if constraint_type == "all_different":
            values = [assignment[v] for v in involved_vars]
            return len(values) == len(set(values))

        elif constraint_type == "not_equal":
            var1, var2 = involved_vars
            return assignment[var1] != assignment[var2]

        elif constraint_type == "custom":
            # Custom constraint with lambda function
            func = constraint["function"]
            values = [assignment[v] for v in involved_vars]
            return func(*values)

        return True

    def get_constraint_graph_size(self) -> Tuple[int, int]:
        """Returns (num_nodes, num_edges) of constraint graph"""
        num_nodes = len(self.variables)
        edges = set()

        for var in self.variables:
            for neighbor in self.neighbors[var]:
                edge = tuple(sorted([str(var), str(neighbor)]))
                edges.add(edge)

        return (num_nodes, len(edges))

    def reset_stats(self):
        """Reset statistics for a new solve"""
        self.stats = CSPStats()

    def reset_domains(self):
        """Reset domains to original state"""
        self.domains = {
            var: list(domain) for var, domain in self.original_domains.items()
        }

    # ==================== PROBLEM REDUCTION METHODS ====================

    def apply_node_consistency(self, verbose: bool = False) -> bool:
        """
        Apply node consistency - remove values violating unary constraints
        Returns False if any domain becomes empty
        """
        if verbose:
            print("  Applying node consistency...")

        removed_count = 0
        for var in self.variables:
            values_to_remove = []
            for value in self.domains[var]:
                # Check unary constraints (constraints involving only this variable)
                for constraint in self.constraints:
                    if (
                        len(constraint["variables"]) == 1
                        and var in constraint["variables"]
                    ):
                        temp_assignment = {var: value}
                        if not self._check_constraint(constraint, temp_assignment):
                            values_to_remove.append(value)
                            break

            for value in values_to_remove:
                self.domains[var].remove(value)
                removed_count += 1

            if len(self.domains[var]) == 0:
                if verbose:
                    print(f"  Domain wipeout at variable {var}!")
                return False

        if verbose:
            print(f"  Removed {removed_count} values from domains")

        return True

    def apply_arc_consistency(self, verbose: bool = False) -> bool:
        """
        Apply AC-3 algorithm to reduce domains
        Returns False if inconsistency detected (no solution exists)
        """
        if verbose:
            print("  Applying arc consistency (AC-3)...")

        # Create queue of all arcs (directed constraint edges)
        queue = []
        for constraint in self.constraints:
            vars_in_constraint = constraint["variables"]
            # Add arcs for binary constraints
            if len(vars_in_constraint) == 2:
                queue.append((vars_in_constraint[0], vars_in_constraint[1], constraint))
                queue.append((vars_in_constraint[1], vars_in_constraint[0], constraint))

        initial_queue_size = len(queue)
        processed = 0

        while queue:
            (xi, xj, constraint) = queue.pop(0)
            processed += 1

            if verbose and processed % 100 == 0:
                print(
                    f"  Processed {processed}/{initial_queue_size + len(queue)} arcs..."
                )

            if self._revise(xi, xj, constraint):
                if len(self.domains[xi]) == 0:
                    if verbose:
                        print(f"  Domain wipeout at variable {xi}!")
                    return False

                # Add all neighbors of xi back to queue (except xj)
                for neighbor in self.neighbors[xi]:
                    if neighbor != xj:
                        # Find constraint between xi and neighbor
                        for c in self.constraints:
                            if (
                                xi in c["variables"]
                                and neighbor in c["variables"]
                                and len(c["variables"]) == 2
                            ):
                                queue.append((neighbor, xi, c))

        if verbose:
            print(f"  AC-3 completed. Processed {processed} arcs total.")

        return True

    def _revise(self, xi: Any, xj: Any, constraint: Dict[str, Any]) -> bool:
        """
        Remove values from xi's domain that have no support in xj's domain
        Returns True if domain was revised
        """
        revised = False
        values_to_remove = []

        for value_i in self.domains[xi]:
            # Check if there exists a value in xj's domain that satisfies constraint
            has_support = False
            for value_j in self.domains[xj]:
                # Create temporary assignment to test
                temp_assignment = {xi: value_i, xj: value_j}
                if self._check_constraint(constraint, temp_assignment):
                    has_support = True
                    break

            if not has_support:
                values_to_remove.append(value_i)
                revised = True

        # Remove unsupported values
        for value in values_to_remove:
            self.domains[xi].remove(value)

        return revised

    def solve_with_preprocessing(
        self, method: str, verbose: bool = False
    ) -> Optional[Dict[Any, Any]]:
        """
        Solve CSP with preprocessing (node consistency or arc consistency)
        """
        self.reset_stats()
        self.reset_domains()
        start_time = time.time()

        # Apply preprocessing
        if method == "node_consistency":
            if not self.apply_node_consistency(verbose):
                self.stats.time_elapsed = time.time() - start_time
                self.stats.solution_found = False
                return None
        elif method == "arc_consistency":
            if not self.apply_arc_consistency(verbose):
                self.stats.time_elapsed = time.time() - start_time
                self.stats.solution_found = False
                return None

        if verbose:
            print("  Starting backtracking on reduced domains...")

        # Solve with backtracking on reduced domains
        assignment = {}
        result = self._backtrack(assignment, verbose)

        self.stats.time_elapsed = time.time() - start_time
        self.stats.solution_found = result is not None
        return result

    # ==================== BASIC SEARCH STRATEGIES ====================

    def solve_forward_checking(self, verbose: bool = False) -> Optional[Dict[Any, Any]]:
        """
        Forward Checking: Check ahead and remove inconsistent values from future variables
        This is a basic search strategy that combines backtracking with look-ahead
        """
        self.reset_stats()
        self.reset_domains()
        start_time = time.time()

        if verbose:
            print("  Starting forward checking...")

        assignment = {}
        result = self._backtrack_fc(assignment, verbose)

        self.stats.time_elapsed = time.time() - start_time
        self.stats.solution_found = result is not None
        return result

    def _backtrack_fc(
        self, assignment: Dict[Any, Any], verbose: bool = False
    ) -> Optional[Dict[Any, Any]]:
        """Backtracking with forward checking"""
        self.stats.nodes_visited += 1

        if verbose and self.stats.nodes_visited % 5000 == 0:
            print(
                f"  Nodes: {self.stats.nodes_visited}, Depth: {len(assignment)}/{len(self.variables)}, Backtracks: {self.stats.backtracks}"
            )

        # Check if assignment is complete
        if len(assignment) == len(self.variables):
            if verbose:
                print(f"  Solution found at node {self.stats.nodes_visited}!")
            return assignment

        # Select next unassigned variable
        var = self._select_unassigned_variable(assignment)

        # Try each value in domain
        for value in list(self.domains[var]):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value

                # Save domains before forward checking
                saved_domains = {v: list(self.domains[v]) for v in self.domains}

                # Forward check: prune inconsistent values from unassigned neighbors
                if self._forward_check(var, value, assignment):
                    result = self._backtrack_fc(assignment, verbose)
                    if result is not None:
                        return result

                # Restore domains
                self.domains = saved_domains
                del assignment[var]
                self.stats.backtracks += 1

        return None

    def _forward_check(self, var: Any, value: Any, assignment: Dict[Any, Any]) -> bool:
        """
        Remove inconsistent values from unassigned neighbors' domains
        Returns False if any domain becomes empty (dead-end detected)
        """
        for neighbor in self.neighbors[var]:
            if neighbor in assignment:
                continue

            values_to_remove = []
            for neighbor_value in self.domains[neighbor]:
                # Check if this value would be consistent with current assignment
                temp_assignment = assignment.copy()
                temp_assignment[neighbor] = neighbor_value

                consistent = True
                for constraint in self.constraints:
                    if (
                        var in constraint["variables"]
                        and neighbor in constraint["variables"]
                    ):
                        if not self._check_constraint(constraint, temp_assignment):
                            consistent = False
                            break

                if not consistent:
                    values_to_remove.append(neighbor_value)

            # Remove inconsistent values
            for val in values_to_remove:
                self.domains[neighbor].remove(val)

            # Domain wipeout - dead end detected
            if len(self.domains[neighbor]) == 0:
                return False

        return True

    # ==================== STOCHASTIC SEARCH METHODS ====================

    def solve_min_conflicts(
        self, max_steps: int = 10000, verbose: bool = False
    ) -> Optional[Dict[Any, Any]]:
        """
        Min-Conflicts: Start with complete random assignment, iteratively fix conflicts
        This is a stochastic local search method that works well for large problems

        Args:
            max_steps: Maximum number of iterations before giving up
        """
        import random

        self.reset_stats()
        self.reset_domains()
        start_time = time.time()

        if verbose:
            print(f"  Starting min-conflicts (max {max_steps} steps)...")

        # Generate initial complete random assignment
        assignment = {}
        for var in self.variables:
            assignment[var] = random.choice(self.original_domains[var])

        for step in range(max_steps):
            self.stats.nodes_visited += 1

            if verbose and step % 1000 == 0:
                conflicts = self._count_conflicts(assignment)
                print(f"  Step {step}/{max_steps}, Conflicts: {conflicts}")

            # Check if current assignment satisfies all constraints
            if self._is_complete_and_consistent(assignment):
                if verbose:
                    print(f"  Solution found at step {step}!")
                self.stats.time_elapsed = time.time() - start_time
                self.stats.solution_found = True
                return assignment

            # Select a variable that is in conflict
            conflicted_var = self._select_conflicted_variable(assignment)
            if conflicted_var is None:
                # No conflicts found
                self.stats.time_elapsed = time.time() - start_time
                self.stats.solution_found = True
                return assignment

            # Choose value that minimizes conflicts
            best_value = self._min_conflicts_value(conflicted_var, assignment)
            assignment[conflicted_var] = best_value
            self.stats.backtracks += 1

        if verbose:
            conflicts = self._count_conflicts(assignment)
            print(f"  Max steps reached. Final conflicts: {conflicts}")

        self.stats.time_elapsed = time.time() - start_time
        self.stats.solution_found = False
        return None

    def _is_complete_and_consistent(self, assignment: Dict[Any, Any]) -> bool:
        """Check if assignment is complete and satisfies all constraints"""
        if len(assignment) != len(self.variables):
            return False

        for constraint in self.constraints:
            self.stats.constraint_checks += 1
            if not self._check_constraint(constraint, assignment):
                return False

        return True

    def _count_conflicts(self, assignment: Dict[Any, Any]) -> int:
        """Count number of constraint violations in current assignment"""
        conflicts = 0
        for constraint in self.constraints:
            if not self._check_constraint(constraint, assignment):
                conflicts += 1
        return conflicts

    def _select_conflicted_variable(self, assignment: Dict[Any, Any]) -> Optional[Any]:
        """Select a variable that participates in a violated constraint"""
        import random

        conflicted_vars = set()

        for constraint in self.constraints:
            if not self._check_constraint(constraint, assignment):
                # Add all variables in this violated constraint
                conflicted_vars.update(constraint["variables"])

        if not conflicted_vars:
            return None

        # Return random conflicted variable
        return random.choice(list(conflicted_vars))

    def _min_conflicts_value(self, var: Any, assignment: Dict[Any, Any]) -> Any:
        """
        Return value for var that minimizes conflicts with other variables
        If there's a tie, choose randomly among best values
        """
        import random

        min_conflicts = float("inf")
        best_values = []

        for value in self.original_domains[var]:
            # Try this value
            assignment[var] = value

            # Count conflicts
            conflicts = 0
            for constraint in self.constraints:
                if var in constraint["variables"]:
                    self.stats.constraint_checks += 1
                    if not self._check_constraint(constraint, assignment):
                        conflicts += 1

            # Update best values
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_values = [value]
            elif conflicts == min_conflicts:
                best_values.append(value)

        # Return random best value (for variety)
        return (
            random.choice(best_values) if best_values else self.original_domains[var][0]
        )

    # ==================== BACKTRACKING METHOD ====================

    def solve_backtracking(self, verbose: bool = False) -> Optional[Dict[Any, Any]]:
        """Simple backtracking search - baseline algorithm"""
        self.reset_stats()
        self.reset_domains()
        start_time = time.time()

        if verbose:
            print("  Starting backtracking...")

        assignment = {}
        result = self._backtrack(assignment, verbose)

        self.stats.time_elapsed = time.time() - start_time
        self.stats.solution_found = result is not None
        return result

    def _backtrack(
        self, assignment: Dict[Any, Any], verbose: bool = False
    ) -> Optional[Dict[Any, Any]]:
        """Recursive backtracking"""
        self.stats.nodes_visited += 1

        # Progress indicator
        if verbose and self.stats.nodes_visited % 5000 == 0:
            print(
                f"  Nodes: {self.stats.nodes_visited}, Depth: {len(assignment)}/{len(self.variables)}, Backtracks: {self.stats.backtracks}"
            )

        # Check if assignment is complete
        if len(assignment) == len(self.variables):
            if verbose:
                print(f"  Solution found at node {self.stats.nodes_visited}!")
            return assignment

        # Select next unassigned variable
        var = self._select_unassigned_variable(assignment)

        # Try each value in domain
        for value in self.domains[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value

                result = self._backtrack(assignment, verbose)
                if result is not None:
                    return result

                # Backtrack
                del assignment[var]
                self.stats.backtracks += 1

        return None

    def _select_unassigned_variable(self, assignment: Dict[Any, Any]) -> Any:
        """Select next unassigned variable (simple: first unassigned)"""
        for var in self.variables:
            if var not in assignment:
                return var
        return None

    def print_stats(self, method_name: str):
        """Print solver statistics"""
        print(f"\n=== {method_name} Statistics ===")
        print(f"Solution found: {self.stats.solution_found}")
        print(f"Nodes visited: {self.stats.nodes_visited}")
        print(f"Backtracks: {self.stats.backtracks}")
        print(f"Constraint checks: {self.stats.constraint_checks}")
        print(f"Time elapsed: {self.stats.time_elapsed:.4f} seconds")

    def print_domain_info(self, label: str = ""):
        """Print information about current domain sizes"""
        total_values = sum(len(domain) for domain in self.domains.values())
        avg_domain_size = total_values / len(self.variables) if self.variables else 0
        min_domain = (
            min(len(domain) for domain in self.domains.values()) if self.domains else 0
        )
        max_domain = (
            max(len(domain) for domain in self.domains.values()) if self.domains else 0
        )

        print(f"\n=== Domain Info{' - ' + label if label else ''} ===")
        print(f"Total domain values: {total_values}")
        print(f"Average domain size: {avg_domain_size:.2f}")
        print(f"Min domain size: {min_domain}")
        print(f"Max domain size: {max_domain}")

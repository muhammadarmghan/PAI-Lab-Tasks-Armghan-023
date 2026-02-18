
def solve_water_jug_dfs(capacity_a, capacity_b, target_amount):
    stack = []
    explored = set()

    initial_state = (0, 0)
    stack.append((initial_state, []))

    print(f"Solving Water Jug Problem using DFS")
    print(f"Jug A: {capacity_a}L, Jug B: {capacity_b}L, Target: {target_amount}L")

    while stack:
        (a, b), path = stack.pop()

        if a == target_amount or b == target_amount:
            print("\nTarget reached successfully!")
            final_path = path + [(a, b)]
            for step_no, state in enumerate(final_path):
                print(f"Step {step_no}: {state}")
            return True

        if (a, b) in explored:
            continue

        explored.add((a, b))

        next_states = []

        # Fill jug A
        if a < capacity_a:
            next_states.append((capacity_a, b))

        # Fill jug B
        if b < capacity_b:
            next_states.append((a, capacity_b))

        # Empty jug A
        if a > 0:
            next_states.append((0, b))

        # Empty jug B
        if b > 0:
            next_states.append((a, 0))

        # Pour A -> B
        if a > 0 and b < capacity_b:
            pour = min(a, capacity_b - b)
            next_states.append((a - pour, b + pour))

        # Pour B -> A
        if b > 0 and a < capacity_a:
            pour = min(b, capacity_a - a)
            next_states.append((a + pour, b - pour))

        for state in next_states:
            if state not in explored:
                stack.append((state, path + [(a, b)]))

    print("No solution found.")
    return False


# Input values
jug_a = 4
jug_b = 3
goal = 2

solve_water_jug_dfs(jug_a, jug_b, goal)

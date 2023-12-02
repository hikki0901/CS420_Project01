import random

def generate_map(rows, cols):
    # Create an empty grid with 0s
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Place walls randomly
    place_walls(grid, rows, cols)
    
    # Place the agent and the goal randomly
    place_agent_and_goal(grid, rows, cols)
    
    return grid

def place_walls(grid, rows, cols):
    # Calculate the number of walls (adjust this as needed)
    num_walls = int(0.2 * rows * cols)
    
    for _ in range(num_walls):
        row, col = random.randint(0, rows-1), random.randint(0, cols-1)
        # Ensure the cell is empty (not already a wall or agent or goal)
        if grid[row][col] == 0:
            grid[row][col] = -1  # Place a wall

def place_agent_and_goal(grid, rows, cols):
    # Place the agent
    agent_row, agent_col = random.randint(0, rows-1), random.randint(0, cols-1)
    while grid[agent_row][agent_col] != 0:
        agent_row, agent_col = random.randint(0, rows-1), random.randint(0, cols-1)
    grid[agent_row][agent_col] = "A1"
    
    # Place the goal
    goal_row, goal_col = random.randint(0, rows-1), random.randint(0, cols-1)
    while grid[goal_row][goal_col] != 0 or (goal_row == agent_row and goal_col == agent_col):
        goal_row, goal_col = random.randint(0, rows-1), random.randint(0, cols-1)
    grid[goal_row][goal_col] = "T1"

def export_to_file(grid, filename="output_level1.txt"):
    with open(filename, "w") as file:
        for row in grid:
            row_str = ",".join(map(str, row))
            file.write(row_str + "\n")

# Example usage
rows, cols = 50, 50  # Adjust the grid size as needed
grid = generate_map(rows, cols)
export_to_file(grid)
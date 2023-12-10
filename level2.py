from queue import PriorityQueue
import matplotlib.pyplot as plt
import pygame

pygame.init()

WIDTH = 600
HEIGHT= 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (15, 10, 222)
GREY = (128, 128, 128)
VSBLUE = (192,250,244)
IRISBLUE = (0, 181, 204)
PINK = (255, 105, 180)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move your step")
font = pygame.font.Font('freesansbold.ttf', 18)
tile_font = pygame.font.Font('freesansbold.ttf', 10)
Error_area = pygame.Rect(WIDTH // 4-50, HEIGHT//2 -35, 400, 120)

class Button:
    def __init__(self, x, y, text, click):
        self.x = x
        self.y = y
        self.text = text
        self.click = click
        self.draw()
        
    def draw(self):
        text_button = font.render(self.text, True, BLACK)
        button = pygame.rect.Rect((self.x, self.y), (120, 50))
        if self.click:
            pygame.draw.rect(window, GREEN, button, 0,5)
        else:
            pygame.draw.rect(window, IRISBLUE, button, 0,5)
        window.blit(text_button,(self.x +20, self.y + 15))
    
    def is_click(self) -> bool:
        mouse = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button = pygame.rect.Rect(self.x, self.y, 120, 50)
        if(left_click and button.collidepoint(mouse)):
            return True
        else:
            return False
        
    def set_click(self):
        self.click = True
        
    def remove_click(self):
        self.click = False
        
    def return_click(self) -> bool:
        return self.click

class Node:
    def __init__(self, irow, jcol, width, height, total_row, total_col) -> None:
        self.color = WHITE
        self.neighbor=[]
        self.total_row = total_row
        self.x = irow
        self.y = jcol
        self.width = width
        self.height = height
        self.visited =[]
        self.total_col = total_col
        self.text = ""
        self.is_door = False
        self.visit_count = 0
        
    def increment_visit_count(self):
        self.visit_count +=1
    
    def set_heatmap_color(self):
        intensity = min(192, int(self.visit_count * 36))
        self.color = (192-intensity,250-intensity,244-intensity)
    
    def get_pos(self):
        return self.x, self.y
        
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.y * self.width, self.x * self.height + 100, self.width, self.height + 100))
        text_surface = tile_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=((self.y * self.width) + self.width // 2, (self.x * self.height + 100) + self.height // 2))
        window.blit(text_surface, text_rect)

    def set_barrier_color(self):
        self.color = BLACK
    
    def set_end_color(self):
        self.color = BLUE
        
    def set_start_color(self):
        self.color = RED
    
    def set_nodeOpen_color(self):
        self.color = GREEN
        
    def set_nodeVisited_color(self):
        self.color = YELLOW
        
    def set_path_color(self):
        self.color = RED
    
    def set_unvisible(self):
        self.color =VSBLUE

    def set_key(self):
        self.color = PINK

    def set_door(self):
        self.color = GREY
        self.is_door = True
        
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == RED
    
    def is_end(self):
        return self.color == BLUE
    
    def neighbors(self, grid, collected_key, check_door):
        self.neighbor = []
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir in dir:
            new_x = self.x + dir[0]
            new_y = self.y + dir[1]
            check = True

            if (0 <= new_x < self.total_row and 0 <= new_y < self.total_col):
                if abs(dir[0]) == abs(dir[1]):
                    if grid[self.x][new_y].is_barrier() or grid[new_x][self.y].is_barrier() or grid[new_x][new_y].is_barrier():
                        check = False
                    
                    if check_door ==True:
                        if grid[new_x][self.y].is_door:
                            key = "K" + str(grid[new_x][self.y].text[1])
                            if key not in collected_key:
                                check = False

                        if grid[self.x][new_y].is_door:
                            key = "K" + str(grid[self.x][new_y].text[1])
                            if key not in collected_key:
                                check = False
                        
                        if grid[new_x][new_y].is_door:
                            key = "K" + str(grid[new_x][new_y].text[1])
                            if key not in collected_key:
                                check = False

                else:
                    if grid[new_x][new_y].is_barrier():
                        check = False
                    
                    if check_door == True:
                        if grid[new_x][new_y].is_door:
                            key = "K" + str(grid[new_x][new_y].text[1])
                            if key not in collected_key:
                                check = False

            else: check = False

            if check == True:
                if grid[new_x][new_y] not in self.neighbor:
                    self.neighbor.append(grid[new_x][new_y])

    def __lt__(self, other):
        return False

# export to file png (heatmap + path)  
def save_heatmap_image(file_path, grid):
    colors = [[node.color for node in row] for row in grid]
    plt.imshow(colors, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.savefig(file_path)
    plt.show()

#pop up "Not Path Found" if agent does not find path
def draw_no_path_message(window,file_path):
    pygame.draw.rect(window,RED, Error_area,0,50)
    font1 = pygame.font.Font('freesansbold.ttf', 54)
    text = font1.render('Level 2', True, YELLOW)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    font2 = pygame.font.Font('freesansbold.ttf', 42)
    text_level = font2.render('No Path Found', True, YELLOW)
    text_level_rect = text_level.get_rect(center=(WIDTH // 2, HEIGHT // 2+54))
    window.blit(text, text_rect)
    window.blit(text_level, text_level_rect)
    
    pygame.display.update()
    pygame.time.delay(2000)
    
    # Save the screen with the pop-up message
    pygame.image.save(window, file_path)

#read data from file
def read_grid_from_file(file_path):
    grid = []
    with open(file_path,'r') as file:
        row , coloumn = map(int, file.readline().strip().split(','))
        
        floor = file.readline().strip().split(',')
        
        for i in range(row):
            data = file.readline().strip().split(',')
            grid.append(data)
            
    return row, coloumn, floor, grid

#draw each node of grid
def make_grid_color(row, col, width, height, grid):
    grid_color = []
    start = None
    end = None
    for i in range(row):
        grid_color.append([])
        for j in range(col):
            node = Node(i, j, width // col, height // row, row, col)

            if(grid[i][j] == "A1"):
                node.set_start_color()
                start = node

            if(grid[i][j] == "T1"):
                node.set_end_color()
                end = node

            if(grid[i][j] == "-1"):
                node.set_barrier_color()

            if(grid[i][j].startswith("K")):
                node.set_key()
                node.text = str(grid[i][j])

            if(grid[i][j].startswith("D")):
                node.set_door()
                node.text = str(grid[i][j])
                
            grid_color[i].append(node)
            
    return grid_color, start, end 

def draw_grid_line(window, rows, cols, width, height):
    gap1 = height // rows
    gap2 = width // cols
        
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap1 + 100), (width, i * gap1 +100))
        for j in range(cols):
            pygame.draw.line(window, GREY, (j * gap2, 100), (j * gap2, height+100))

def draw_update(window, grid, rows, cols, width, height):   
    for i in grid:
        for node in i:
            node.draw(window)
            
    draw_grid_line(window, rows, cols, width, height)
    pygame.display.update()

def draw_solution(come, current, draw, start):
    path = {}
    while current in come:   
        path[come[current]] = current
        current = come[current]

    while start in path:
        pygame.time.delay(100)
        start.set_unvisible()
        start.increment_visit_count()
        start.set_heatmap_color()
        start = path[start]
        start.set_path_color()
        draw()

def heuristic(start, end):
    x1, y1 = start.get_pos()
    x2, y2 = end.get_pos()
    penalty = 0
    if start.text.startswith("D"):
        penalty = 1
    return abs(x1 - x2) + abs(y1 - y2) + penalty * 100

def astar_algorithm(draw, grid, start, end):
    count = 0
    frontier = PriorityQueue()
    frontier.put((0, count, start))
    come = {}

    g_cost ={node: float("inf") for i in grid for node in i}
    g_cost[start] =0
    f_cost = {node: float("inf") for i in grid for node in i}
    f_cost[start] = heuristic(start, end)
    explored = {start}

    while not frontier.empty():
        current_node = frontier.get()[2]
        
        explored.remove(current_node)

        if current_node == end:
            #draw_solution(come,end,draw,start)
            path = {}
            while end in come:   
                path[come[end]] = end
                end = come[end]
            return path
        
        for neighbor in current_node.neighbor:
            temp_g_cost = g_cost[current_node] + 1
            if temp_g_cost < g_cost[neighbor]:
                come[neighbor] = current_node
                
                g_cost[neighbor] = temp_g_cost
                f_cost[neighbor] = temp_g_cost + heuristic(neighbor, end)
                if neighbor not in explored:
                    count += 1
                    frontier.put((f_cost[neighbor], count, neighbor))
                    explored.add(neighbor)
                    #neighbor.set_nodeOpen_color()
        # draw()
        # if(current_node != start):
        #    current_node.set_nodeVisited_color()

    return False

def astar_algorithm_with_checkpoints(draw, grid, checklist, collected_key, final_path):
    collected_key.clear()
    for i in range(len(checklist) - 1):
        start = checklist[i]
        end = checklist[i + 1]
        count = 0
        frontier = PriorityQueue()
        frontier.put((0, count, start))
        come = {}

        g_cost ={node: float("inf") for i in grid for node in i}
        g_cost[start] =0
        f_cost = {node: float("inf") for i in grid for node in i}
        f_cost[start] = heuristic(start, end)
        
        explored = {start}
        
        while not frontier.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current_node = frontier.get()[2]

            if current_node == start and current_node.text.startswith("K"):
                key = "K" + str(current_node.text[1])
                collected_key.add(key)
            explored.remove(current_node)  
            current_node.neighbors(grid, collected_key, True)
                
            if current_node == end:
                draw_solution(come, end, draw, start)
                path = {}
                tmp = []
                while end in come:   
                    path[come[end]] = end
                    end = come[end]
                for i in path:
                    tmp.append(i)
                tmp.reverse()
                final_path.extend(tmp)
                continue
     
            for neighbor in current_node.neighbor:
                temp_g_cost = g_cost[current_node] + 1
                
                if temp_g_cost < g_cost[neighbor]:
                    come[neighbor] = current_node
                    
                    g_cost[neighbor] = temp_g_cost
                    f_cost[neighbor] = temp_g_cost + heuristic(neighbor, end)
                    if neighbor not in explored:
                        count += 1
                        frontier.put((f_cost[neighbor], count, neighbor))
                        explored.add(neighbor)
            # draw()

def set_recursive_limit (grid):
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j].text.startswith("D") or grid[i][j].text.startswith("K"):
                count += 1
    return count * 2                

def recursive (draw, grid, start, end, goal_list, all_keys, count, limit):
    if count == limit:
        print ("No path, limit reached")
        return False
    
    path = astar_algorithm (draw, grid, start, end)

    if not path:
        print ("No path")
        return False
    
    for step in path:
        if step.text.startswith("D"):
            if step in goal_list:
                goal_list.remove(step)
            goal_list.append(step)
            key = "K" + str(step.text)[1]
            for node in all_keys:
                if node.text == key:
                    if node in goal_list:
                        goal_list.remove(node)
                    goal_list.append(node)
                    result = recursive (draw, grid, start, node, goal_list, all_keys, count + 1, limit)
                    
                    if not result:
                        return False
    return True



                    
def main(window, width, height):
    file = './input/level2/input5-level2.txt'
    file_num = file[20]
    row, col, floor, temp_grid = read_grid_from_file(file)
    grid, start, end = make_grid_color(row,col,width,height,temp_grid)
    goal_list = []
    all_keys = []
    final_path = []
    click1 = False
    click4 = False
    one_press = True
    collected_key = set()
    count = 0

    run = True
    while run:
        window.fill(WHITE)
        astar_button = Button(10, 10, "Go", click1)
        clear_button = Button(400, 10, "Clear", click4)
        draw_update(window,grid,row,col,width,height)     
        
        if(pygame.mouse.get_pressed()[0]) and one_press:
            one_press = False             
            if(astar_button.is_click()):
                click1 = True
                click4 = False
                clear_button.remove_click()
                clear_button.draw()
                
            if(clear_button.is_click()):
                click4 = True
                click1 = False
                goal_list.clear()
                astar_button.remove_click()
                astar_button.draw()
                all_keys.clear()
                collected_key.clear()
                count = 0
                grid, start, end = make_grid_color(row, col, width, height, temp_grid)
            
            if((click1)):
                for i in grid:
                    for node in i:
                        node.neighbors(grid, collected_key, False)
                        if node.text.startswith("K"):
                            all_keys.append(node)
                
                recursive_limit = set_recursive_limit(grid)

                astar_button.set_click()
                astar_button.draw()
                check = recursive(lambda: draw_update(window, grid, row, col, width, height), grid, start, end, goal_list, all_keys, count, recursive_limit)
                if check: 
                #astar_algorithm(lambda: draw_update(window, grid, row, col, width, height), grid, start, end)  
                    goal_list.reverse() 
                    goal_list.insert(0, start)
                    goal_list.append(end)
                    #for i in final_path:
                    #    x, y = i.get_pos()
                    #    print(i, end=" ")
                        #print (i.text, end = " ")    
                    astar_algorithm_with_checkpoints(lambda: draw_update(window, grid, row, col, width, height), grid, goal_list, collected_key, final_path)
                    for i in range(len(final_path) - 1, 0, -1):
                        if final_path[i] == final_path[i - 1]:
                            del final_path[i]
                    for i in final_path:
                        x, y = i.get_pos()
                        print((x, y), end=" ")
                    pygame.image.save(window, "./output/level2/output"+str(file_num)+"_level2_screen.png")
                else:
                    draw_no_path_message(window,"./output/level2/output"+str(file_num)+"_level2_NotFound.png")
        if(not pygame.mouse.get_pressed()[0]) and not one_press:
            one_press = True
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
    pygame.quit()
    
if __name__ == "__main__":
    main(window, WIDTH,HEIGHT-100)

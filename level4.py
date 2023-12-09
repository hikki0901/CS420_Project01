import cProfile
import copy
from queue import PriorityQueue
import pygame
from os.path import exists
import random


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
IRISBLUE = (0, 181, 204)
PINK = (255, 105, 180)
LIGHTGREEN = (208,242,136)
LIGHTPUR = (255,245,194)
ERROR_AREA_COLOR = (120, 124, 198)

C0 = (255, 181, 181)
C1 = (255, 181, 216)
C2 = (255, 181, 251)
C3 = (201, 181, 255)
C4 = (181, 255, 253)
C5 = (246, 255, 181)
C6 = (255, 238, 181)
C7 = (255, 206, 181)
C8 = (255, 196, 181)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move your step")
font = pygame.font.Font('freesansbold.ttf', 18)
tile_font = pygame.font.Font('freesansbold.ttf', 10)
fill_area_rect = pygame.Rect(0, 100, WIDTH, HEIGHT-100)
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
            pygame.draw.rect(WINDOW, GREEN, button, 0,5)
        else:
            pygame.draw.rect(WINDOW, IRISBLUE, button, 0,5)
        WINDOW.blit(text_button,(self.x +20, self.y + 15))
    
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
    def __init__(self, irow, jcol, width, height, total_row, total_col,floor: int) -> None:
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
        self.floor = floor
        self.is_door = False
        self.visit_count = 0
    
    def increment_visit_count(self):
        self.visit_count +=1

    def set_heatmap_color(self):
        x, y, z = self.color
        intensity = min(x, y, z, int(self.visit_count * 36))
        self.color = (x - intensity, y - intensity, z - intensity)
    
    def get_floor(self):
        return self.floor
    
    def set_floor(self, f):
        self.floor = f
    
    def get_pos(self):
        return self.x, self.y
        
    def draw(self, window,cur_floor):
        if(self.floor == cur_floor):
            pygame.draw.rect(window, self.color, (self.y * self.width, self.x * self.height + 100, self.width, self.height + 100))
            if(self.text != "-1"):
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

    def set_path_color_aux(self):
        self.color = GREEN
    
    def set_node_null(self):
        self.color =WHITE
    
    def set_unvisible(self, i):
        if i == 0: self.color = C0
        if i == 1: self.color = C1
        if i == 2: self.color = C2
        if i == 3: self.color = C3
        if i == 4: self.color = C4
        if i == 5: self.color = C5
        if i == 6: self.color = C6
        if i == 7: self.color = C7
        if i == 8: self.color = C8
        
    def set_key(self):
        self.color = PINK

    def set_door(self):
        self.color = GREY
        self.is_door = True
        
    def set_UP(self):
        self.color = LIGHTGREEN
    
    def set_DO(self):
        self.color = LIGHTPUR
        
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == RED
    
    def is_end(self):
        return self.color == BLUE
    
    def is_UP(self):
        return self.color == LIGHTGREEN
    
    def is_DO(self):
        return self.color == LIGHTPUR
    
    def searchUP(self,grid,fl):
        for i in grid[fl+1]:
            for node in i:
                if(node.is_DO()):
                    return node
    
    def searchDO(self,grid,fl):
        for i in grid[fl-1]:
            for node in i:
                if(node.is_UP()):
                    return node
    
    def neighbors(self, grid, collected_key, check_door):
        cur_floor = self.floor
        self.neighbor = []
        direct = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir in direct:
            new_x = self.x + dir[0]
            new_y = self.y + dir[1]
            check = True
            
            if (0 <= new_x < self.total_row and 0 <= new_y < self.total_col):
                if abs(dir[0]) == abs(dir[1]):
                    if grid[cur_floor][self.x][new_y].is_barrier() or grid[cur_floor][new_x][self.y].is_barrier() or grid[cur_floor][new_x][new_y].is_barrier():
                        check = False                   
                    
                    if check_door ==True:
                        if grid[cur_floor][new_x][self.y].is_door:
                            key = "K" + str(grid[cur_floor][new_x][self.y].text[1:])
                            if key not in collected_key:
                                check = False

                        if grid[cur_floor][self.x][new_y].is_door:
                            key = "K" + str(grid[cur_floor][self.x][new_y].text[1:])
                            if key not in collected_key:
                                check = False
                        
                        if grid[cur_floor][new_x][new_y].is_door:
                            key = "K" + str(grid[cur_floor][new_x][new_y].text[1:])
                            if key not in collected_key:
                                check = False

                else:
                    if grid[cur_floor][new_x][new_y].is_barrier():
                        check = False
                    
                    if check_door == True:
                        if grid[cur_floor][new_x][new_y].is_door:
                            key = "K" + str(grid[cur_floor][new_x][new_y].text[1])
                            if key not in collected_key:
                                check = False

            else: check = False

            if check == True:
                if grid[cur_floor][new_x][new_y] not in self.neighbor:
                    #self.neighbor.append(grid[cur_floor][new_x][new_y])
                    if(grid[cur_floor][new_x][new_y].is_UP()):
                        temp_node = self.searchUP(grid,cur_floor)
                        if temp_node not in self.neighbor:
                            self.neighbor.append(temp_node)
                    elif grid[cur_floor][new_x][new_y].is_DO():
                        temp_node = self.searchDO(grid,cur_floor)
                        if temp_node not in self.neighbor:
                            self.neighbor.append(temp_node)
                    else:
                        self.neighbor.append(grid[cur_floor][new_x][new_y])

    def neighbors_check_agent(self, grid, collected_key, check_door, agent_current_pos):
        cur_floor = self.floor
        self.neighbor = []
        direct = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir in direct:
            new_x = self.x + dir[0]
            new_y = self.y + dir[1]
            check = True
            
            if (0 <= new_x < self.total_row and 0 <= new_y < self.total_col):
                if abs(dir[0]) == abs(dir[1]):
                    if grid[cur_floor][self.x][new_y].is_barrier() or grid[cur_floor][new_x][self.y].is_barrier() or grid[cur_floor][new_x][new_y].is_barrier():
                        check = False                   
                    
                    if check_door ==True:
                        if grid[cur_floor][new_x][self.y].is_door:
                            key = "K" + str(grid[cur_floor][new_x][self.y].text[1:])
                            if key not in collected_key:
                                check = False

                        if grid[cur_floor][self.x][new_y].is_door:
                            key = "K" + str(grid[cur_floor][self.x][new_y].text[1:])
                            if key not in collected_key:
                                check = False
                        
                        if grid[cur_floor][new_x][new_y].is_door:
                            key = "K" + str(grid[cur_floor][new_x][new_y].text[1:])
                            if key not in collected_key:
                                check = False
                    
                    if grid[cur_floor][new_x][self.y] in agent_current_pos:
                        check = False

                    if grid[cur_floor][self.x][new_y] in agent_current_pos:
                        check = False
                        
                    if grid[cur_floor][new_x][new_y] in agent_current_pos:
                        check = False

                else:
                    if grid[cur_floor][new_x][new_y].is_barrier():
                        check = False
                    
                    if grid[cur_floor][new_x][new_y] in agent_current_pos:
                        check = False
                    
                    if check_door == True:
                        if grid[cur_floor][new_x][new_y].is_door:
                            key = "K" + str(grid[cur_floor][new_x][new_y].text[1])
                            if key not in collected_key:
                                check = False

            else: check = False

            if check == True:
                if grid[cur_floor][new_x][new_y] not in self.neighbor:
                    #self.neighbor.append(grid[cur_floor][new_x][new_y])
                    if(grid[cur_floor][new_x][new_y].is_UP()):
                        temp_node = self.searchUP(grid,cur_floor)
                        if temp_node not in self.neighbor:
                            self.neighbor.append(temp_node)
                    elif grid[cur_floor][new_x][new_y].is_DO():
                        temp_node = self.searchDO(grid,cur_floor)
                        if temp_node not in self.neighbor:
                            self.neighbor.append(temp_node)
                    else:
                        self.neighbor.append(grid[cur_floor][new_x][new_y])

    def __lt__(self, other):
        return False


def read_grid_from_file(file):
    grid = []
    max_floor = 0

    if not exists(file):
        print("File does not exist")
        return

    with open(file, 'r') as file:
        row, column = map(int, file.readline().strip().split(','))
        line = file.readline()
        while line:
            if(not line):
                print("end of line")
                return
            floor = line.strip().replace("[", "").replace("]", "")
            if not floor.startswith("floor"):
                continue  # Skip lines that are not floor data
            
            i = int(floor[5])
            
            if i > max_floor:
                max_floor = i
                grid.append([[0] * column for _ in range(row)])
            
            
            
            for j in range(row):
                line = file.readline()
                data = line.strip().split(',')
                grid[i-1][j] = data
                
            line = file.readline()
                
    return row, column, max_floor, grid

#reset node color
def reset_node_color(path_list_agent):
    path_list = copy.copy(path_list_agent)
    for i in range(len(path_list)):
        for node in path_list[i]:
            if(node.text.startswith("A")):
                if (node.text.startswith("A1")):
                        node.set_start_color()
                else: node.set_path_color_aux()

            if(node.text.startswith("T")):
                node.set_end_color()
            if(node.text.startswith("K")):
                node.set_key()
            if(node.text.startswith("UP")):
                node.set_UP()
            if(node.text != "DO" and node.text.startswith("D")):
                node.set_door()
            if(node.text.startswith("DO")):
                node.set_DO()
            if(node.text =="-1"):
                node.set_barrier_color()
            if(node.text ==""):
                node.set_node_null()
    return path_list

def reset_grid(grid,row,col,floor):
    for k in range(floor):
        for i in range(row):
            for j in range(col):
                if(grid[k][i][j].text.startswith("A")):
                    if (grid[k][i][j].text.startswith("A1")):
                            grid[k][i][j].set_start_color()
                    else: grid[k][i][j].set_path_color_aux()

                if(grid[k][i][j].text.startswith("T")):
                        grid[k][i][j].set_end_color()
                if(grid[k][i][j].text.startswith("K")):
                        grid[k][i][j].set_key()
                if(grid[k][i][j].text.startswith("UP")):
                        grid[k][i][j].set_UP()
                if(grid[k][i][j].text != "DO" and grid[k][i][j].text.startswith("D")):
                        grid[k][i][j].set_door()
                if(grid[k][i][j].text.startswith("DO")):
                        grid[k][i][j].set_DO()
                if(grid[k][i][j].text =="-1"):
                    grid[k][i][j].set_barrier_color()
                if(grid[k][i][j].text==""):
                    grid[k][i][j].set_node_null()
    return grid

#export screen image 
def export_screen(grid_export,path_list,row,col,width,height,floor,end,file_num):
    
    limit_move = len(path_list[0]) - 1
    
    for k in range(len(path_list)):
        capture_surface = pygame.Surface((WIDTH, HEIGHT))
        capture_surface.fill(WHITE)
        grid_agent = reset_grid(grid_export,row,col,floor)
        path_list_agent = reset_node_color(path_list)
        name_agent = path_list_agent[k][0].text
        for i in range(len(path_list_agent[k])-1):
            if( i > limit_move):
                break
            pygame.draw.rect(capture_surface, WHITE, fill_area_rect)
            draw_update(capture_surface, grid_agent, row, col, width, height, path_list_agent[k][i].get_floor())
            path_list_agent[k][i].set_unvisible(k)
            path_list_agent[k][i].increment_visit_count()
            path_list_agent[k][i].set_heatmap_color()
            if k == 0: path_list_agent[k][i+1].set_path_color()
            else:
                if (i) < limit_move - 1:
                    path_list_agent[k][i+1].set_path_color_aux()
            draw_update(capture_surface, grid_agent, row, col, width, height, path_list_agent[k][i].get_floor())
        end.set_start_color()
        draw_update(capture_surface,grid_agent,row,col,width,height,end.get_floor())
        
        for ifloor in range(floor):
            capture_surface = pygame.Surface((WIDTH, HEIGHT))
            capture_surface.fill(WHITE)
            pygame.draw.rect(capture_surface, WHITE, fill_area_rect)
            draw_update(capture_surface,grid_agent,row,col,width,height,ifloor)
            pygame.image.save(capture_surface, "./output/level4/output"+str(file_num)+"_level4"+name_agent+"_floor"+str(ifloor+1)+".png")
    return False

def pop_up_extract(window):
    pygame.draw.rect(window,RED, Error_area,0,50)
    font1 = pygame.font.Font('freesansbold.ttf', 54)
    text = font1.render('Level 4', True, YELLOW)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    font2 = pygame.font.Font('freesansbold.ttf', 42)
    text_level = font2.render('Extract...', True, YELLOW)
    text_level_rect = text_level.get_rect(center=(WIDTH // 2, HEIGHT // 2+54))
    window.blit(text, text_rect)
    window.blit(text_level, text_level_rect)
    
    pygame.display.update()

   
def draw_no_path_message(window,file_path):
    pygame.draw.rect(window,RED, Error_area,0,50)
    font1 = pygame.font.Font('freesansbold.ttf', 54)
    text = font1.render('Level 4', True, YELLOW)
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

def make_grid_color(row, col, width, height, grid,floor):
    grid_color = []
    start = None
    end = None
    for k in range(floor):
        grid_color.append([[0] * col for _ in range(row)])
        for i in range(row):
            for j in range(col):
                node = Node(i, j, width // col, height // row, row, col,k)

                if(grid[k][i][j].startswith("A")):
                    if (grid[k][i][j].startswith("A1")):
                        node.set_start_color()
                    else: node.set_path_color_aux()
                    node.text = str(grid[k][i][j])
                    if (grid[k][i][j].startswith("A1")):
                        start = node

                if(grid[k][i][j].startswith("T")):
                    node.set_end_color()
                    node.text = str(grid[k][i][j])
                    if (grid[k][i][j].startswith("T1")):
                        end = node

                if(grid[k][i][j] == "-1"):
                    node.text = str(grid[k][i][j])
                    node.set_barrier_color()
                
                if(grid[k][i][j] == "0"):
                    node.set_node_null()

                if(grid[k][i][j].startswith("K")):
                    node.set_key()
                    node.text = str(grid[k][i][j])
                if(grid[k][i][j].startswith("UP")):
                    node.set_UP()
                    node.text = str(grid[k][i][j])
                if(grid[k][i][j] != "DO" and grid[k][i][j].startswith("D")):
                    node.set_door()
                    node.text = str(grid[k][i][j])
                if(grid[k][i][j].startswith("DO")):
                    node.set_DO()
                    node.text = str(grid[k][i][j])
                    
                grid_color[k][i][j]=node
                   
    return grid_color, start, end 

def draw_grid_line(window, rows, cols, width, height):
    gap1 = height // rows
    gap2 = width // cols
 
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap1 + 100), (width-(width-cols*gap2), i * gap1 +100))
        for j in range(cols):
            pygame.draw.line(window, GREY, (j * gap2, 100), (j * gap2, height+100))
    
    pygame.draw.line(window, GREY, (cols * gap2, 100), (cols * gap2, height+100))

def update_floor_text(window,floor):
    font_size =54
    font_top = pygame.font.Font('freesansbold.ttf', font_size)
    text_surface = font_top.render("Floor"+str(floor+1), True, PINK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = WIDTH // 2 - 10
    text_rect.y = 20 
    window.fill(WHITE, text_rect)
    # Blit the text surface onto the screen
    window.blit(text_surface, text_rect)
    pygame.display.flip()

def draw_update(window, grid, rows, cols, width, height,cur_floor): 
    for i in grid[cur_floor]:
        for node in i:
            if(node.text == "DO"):
                node.set_DO()
            if(node.text == "UP"):
                node.set_UP()
            node.draw(window,cur_floor)
            
    draw_grid_line(window, rows, cols, width, height)
    update_floor_text(window,cur_floor)

def draw_solution(window,come, current,row, col, width, height, start, grid,floor):
    path = {}
    while current in come:   
        path[come[current]] = current
        current = come[current]

    while start in path:
        pygame.draw.rect(window, WHITE, fill_area_rect)
        draw_update(window,grid,row, col, width, height,start.get_floor())
        pygame.time.delay(100)
        start.set_unvisible()
        start = path[start]
        start.set_path_color()
        draw_update(window,grid,row, col, width, height,start.get_floor())

def heuristic(start, end, start_floor, end_floor):
    x1, y1 = start.get_pos()
    x2, y2 = end.get_pos()
    penalty = 0
    if start.text.startswith("D"):
        penalty = 1
    return abs(x1 - x2) + abs(y1 - y2) + abs(start_floor-end_floor) + penalty * 100

def astar_algorithm(window,row, col, width, height, grid, start, end, floor):
    count = 0
    frontier = PriorityQueue()
    frontier.put((0, count, start))
    come = {}
    g_cost ={node: float("inf") for k in range(floor) for i in grid[k] for node in i}
    g_cost[start] =0
    f_cost = {node: float("inf") for k in range(floor) for i in grid[k] for node in i}
    f_cost[start] = heuristic(start, end, start.get_floor(), end.get_floor())
    explored = {start}

    while not frontier.empty():
        current_node = frontier.get()[2]
        
        explored.remove(current_node)

        if current_node == end:
            #draw_solution(window,come,end,draw,row, col, width, height,start,grid,start.get_floor())
            path = {}
            while end in come:   
                path[come[end]] = end
                end = come[end]
            return path
        for neighbor in current_node.neighbor:
            temp_g_cost = g_cost[current_node]+1
            if temp_g_cost < g_cost[neighbor]:
                come[neighbor] = current_node
                
                g_cost[neighbor] = temp_g_cost
                f_cost[neighbor] = temp_g_cost + heuristic(neighbor, end,neighbor.get_floor(),end.get_floor())
                if neighbor not in explored:
                    count += 1
                    frontier.put((f_cost[neighbor], count, neighbor))
                    explored.add(neighbor)
                    #neighbor.set_nodeOpen_color()
        #draw()
        #if(current_node != start):
        #    current_node.set_nodeVisited_color()

    return False

def astar_algorithm_with_checkpoints(window,row, col, width, height, grid, checklist, collected_key,floor,final_path):
    collected_key.clear()
    for i in range(len(checklist) - 1):
        start = checklist[i]
        end = checklist[i + 1]
        count = 0
        frontier = PriorityQueue()
        frontier.put((0, count, start))
        come = {}

        g_cost ={node: float("inf") for k in range(floor) for i in grid[k] for node in i}
        g_cost[start] =0
        f_cost = {node: float("inf") for k in range(floor) for i in grid[k] for node in i}
        f_cost[start] = heuristic(start, end, start.get_floor(), end.get_floor())
        
        explored = {start}
        
        while not frontier.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current_node = frontier.get()[2]

            if current_node == start and current_node.text.startswith("K"):
                key = "K" + str(current_node.text[1:])
                collected_key.add(key)
            explored.remove(current_node)  
            current_node.neighbors(grid, collected_key, True)
                
            if current_node == end:
                # draw_solution(window,come, end,row, col, width, height, start,grid,start.get_floor())
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
                    f_cost[neighbor] = temp_g_cost + heuristic(neighbor, end,neighbor.get_floor(),end.get_floor())
                    if neighbor not in explored:
                        count += 1
                        frontier.put((f_cost[neighbor], count, neighbor))
                        explored.add(neighbor)
            #draw()

def set_recursive_limit (grid):
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for k in range(len(grid[0][0])):
                if grid[i][j][k].text.startswith("D") or grid[i][j][k].text.startswith("K"):
                    count += 1
    return count * 2       

def recursive (window,row, col, width, height, grid, start, end, goal_list, all_keys,floor, count, limit):
    if count == limit:
        print ("No path, limit reached")
        return False
    
    path = astar_algorithm(window,row, col, width, height, grid, start, end,floor)
    if not path:
        print ("No path")
        return
    
    if(path):
        for step in path:
            if step.text != "DO" and step.text.startswith("D"):
                if step in goal_list:
                    goal_list.remove(step)
                goal_list.append(step)
                key = "K" + str(step.text)[1]
                for node in all_keys:
                    if node.text == key:
                        if node in goal_list:
                            goal_list.remove(node)
                        goal_list.append(node)
                        result = recursive (window,row, col, width, height, grid, start, node, goal_list, all_keys, floor, count +1, limit)

                        if not result:
                            return False
    return True


def define_agent(grid):
    agent_list = []
    for k in range(len(grid)):
        for i in range(len(grid[0])):
            for j in range(len(grid[0][0])):
                if grid[k][i][j].text.startswith("A1"):
                    agent_list.insert(0,grid[k][i][j])
                elif grid[k][i][j].text.startswith("A"):
                    agent_list.append(grid[k][i][j])

    return agent_list

def define_target(agent, grid):
    for k in range(len(grid)):
            for i in range(len(grid[0])):
                for j in range(len(grid[0][0])):
                    if grid[k][i][j].text.startswith("T"):
                        if grid[k][i][j].text[1] == agent.text[1]:
                            target = (grid[k][i][j])
                            return target
    
def get_all_path(agent_list, path_list, main_path, grid, collected_key):
    fake_key = []
    agent_cur_pos = []

    save_path = []
    for pos in main_path:
        save_path.append(pos)

    for agent in agent_list:
        tmp_path = []
        tmp_path.append(agent)
        agent_cur_pos.append(agent)
        path_list.append(tmp_path)

    end = main_path[-1]

    i = 1
    k = 0
    check = False
    h = []
    for agent in agent_list:
        h.append(0)

    while main_path[i - 1] != end:
        j = 0
        main_path[i].neighbors(grid, collected_key, False)
        for path in path_list:
            if j == 0:
                if main_path[i] in agent_cur_pos:
                    path.append(path[i - 1])
                    main_path.insert(i, main_path[i - 1])
                    k += 1
                else:
                    path.append(main_path[i])
                    agent_cur_pos[j] = main_path[i]
                    k = 0
            else:
                agent_cur_pos[j].neighbors_check_agent(grid, fake_key, True, agent_cur_pos)
                if len(agent_cur_pos[j].neighbor) != 0:
                    h[j] = 0
                    tmp_neighbor = random.choice(agent_cur_pos[j].neighbor)
                    if tmp_neighbor in main_path[i].neighbor or tmp_neighbor == main_path[i] or tmp_neighbor is None:
                        path.append(path[i - 1])
                    else:
                        path.append(tmp_neighbor)
                        agent_cur_pos[j] = tmp_neighbor
                else: 
                    path.append(path[i - 1])
                    h[j] += 1
            j += 1
        i += 1
        if k > 10 or h[j - 1] > 10:
            check = True
            break
    
    if k > 10 or check == True:
        path_list.clear
        main_path.clear
        for pos in save_path:
            main_path.append(pos)
        get_all_path(agent_list, path_list, main_path, grid, collected_key)
            

'''
def get_all_path (agent_list, path_list, grid, collected_key):
    fake_key = []
    main_path = list(path_list[0])

    agent_current_pos = []
    for agent in agent_list:
        if not agent.text.startswith("A1"):
            tmp_path = []
            tmp_path.append(agent)
            agent_current_pos.append(agent)
            path_list.append(tmp_path)

    for i in range(1, len(path_list[0]) - 1):
        main_path[i].neighbors(grid, collected_key, False)
        j = 0
        for path in path_list:
            if j != 0:
                agent_current_pos[j - 1].neighbors_check_agent(grid, fake_key, True, agent_current_pos)
                tmp_neighbor = random.choice(agent_current_pos[j - 1].neighbor)
                if tmp_neighbor in main_path[i].neighbor or tmp_neighbor == main_path[i] or tmp_neighbor is None:
                    path.append(path[i - 1])
                else:
                    path.append(tmp_neighbor)
                    agent_current_pos[j - 1] = tmp_neighbor
            j += 1
'''   
            

def main(window, width, height):
    file = './input/level4/input1-level4.txt'
    file_num = file[20]
    agent_target = []
    row, col, floor, temp_grid = read_grid_from_file(file)
    grid, start, end = make_grid_color(row,col,width,height,temp_grid,floor)
    grid_export = grid
    goal_list = []
    all_keys = []
    click1 = False
    click4 = False
    one_press = True
    collected_key = set()
    current_floor = start.get_floor()
    run = True
    done = False
    count = 0
    path_temp = []
    while run:
        window.fill(WHITE)
        
        astar_button = Button(10, 20, "Go", click1)
        clear_button = Button(450, 20, "Clear", click4)
        if(done == False):
            draw_update(window,grid,row,col,width,height,current_floor)
        else:
            draw_update(window,grid,row,col,width,height,end.get_floor())
        # for k in range(floor):
        #     for i in grid[k]:
        #         for node in i:
        #             node.neighbors(grid,collected_key,False)     
        #astar_algorithm(lambda: draw_update(window, grid, row, col, width, height,current_floor),row, col, width, height, grid,start,end,floor)
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
                agent_target.clear()
                done =False
                count = 0
                export = True
                while(export):
                    pop_up_extract(window)
                    export = export_screen(grid_export,path_temp,row,col,width,height,floor,end,file_num)
                    
                
                grid, start, end = make_grid_color(row, col, width, height, temp_grid,floor)
            
            if((click1)):
                path_list = []
                for tfloor in range(floor):
                    for i in grid[tfloor]:
                        for node in i:
                            node.neighbors(grid, collected_key, False)
                            if node.text.startswith("K"):
                                all_keys.append(node)
                
                recursive_limit = set_recursive_limit(grid)
                agent_list = define_agent(grid)
                
                astar_button.set_click()
                astar_button.draw()
                path = []
                for agent in agent_list:
                    if agent.text.startswith("A1"):
                        target = define_target(agent,grid)
                        check = recursive(window,row, col, width, height, grid, agent, target, goal_list, all_keys, floor, count, recursive_limit)
                        if check:
                            goal_list.reverse() 
                            goal_list.insert(0, agent)
                            goal_list.append(target)
                            astar_algorithm_with_checkpoints(window,row, col, width, height, grid, goal_list, collected_key,floor, path)
                            #path_list.append(path)
                            break
                
                
                
                if path:            
                    # for path in path_list:
                    #     print (len(path))
                    get_all_path(agent_list, path_list, path, grid,collected_key)
                    draw_path = []
                    path_num = []
                    for i in range(len(path_list[0]) - 1):
                        j = 0
                        for path in path_list:
                            draw_path.append(path[i])
                            path_num.append(j)
                            j += 1 
                    #for i in path_num:
                    #    print(i, '\n')
                    print(len(path_list))
                    path_temp = path_list
                    for i in range(len(path_list[0]) - 1):
                        j = 0
                        for path in path_list:
                            pygame.draw.rect(window, WHITE, fill_area_rect)
                            draw_update(window, grid, row, col, width, height, path[i].get_floor())
                            pygame.time.delay(1)
                            path[i].set_unvisible(j)
                            path[i].increment_visit_count()
                            path[i].set_heatmap_color()
                            if j == 0: path[i + 1].set_path_color()
                            else:
                                if i < len(path_list[0]) - 2:
                                    path[i + 1].set_path_color_aux()
                            j += 1
                            draw_update(window, grid, row, col, width, height, path[i].get_floor())
                        
                        
                    '''
                    i = 0
                    for coord in draw_path:
                        pygame.draw.rect(window, WHITE, fill_area_rect)
                        draw_update(window, grid, row, col, width, height, coord.get_floor())
                        pygame.time.delay(1000)
                        coord.set_unvisible(path_num[i])
                        coord.increment_visit_count()
                        coord.set_heatmap_color()
                        i += 1
                        draw_path[i].set_path_color()
                        draw_update(window, grid, row, col, width, height, coord.get_floor())
                    '''
                    done = True
                    end.set_start_color()
                    draw_update(window,grid,row,col,width,height,end.get_floor()) 
                else:
                    draw_no_path_message(window,"./output/level4/output"+str(file_num)+"_level4_NotFound.png")
          
        if(not pygame.mouse.get_pressed()[0]) and not one_press:
            one_press = True
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
    pygame.quit()
    
if __name__ == "__main__":
    main(WINDOW, WIDTH,HEIGHT-100)
    


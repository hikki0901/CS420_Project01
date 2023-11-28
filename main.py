from queue import PriorityQueue
from queue import Queue
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
IRISBLUE = (0,181,204)
PINK = (255,105,180)

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Move your step")
font = pygame.font.Font('freesansbold.ttf',18)
key_image = pygame.image.load("./images/key.png")
tile_font = pygame.font.Font('freesansbold.ttf',10)

# draw button to click algorithm
class Button:
    def __init__(self, x,y, text,click):
        self.x = x
        self.y = y
        self.text = text
        self.click = click
        self.draw()
        
    def draw(self):
        text_button = font.render(self.text,True,BLACK)
        button = pygame.rect.Rect((self.x,self.y),(120,50))
        if self.click:
            pygame.draw.rect(window,GREEN,button,0,5)
        else:
            pygame.draw.rect(window,IRISBLUE,button,0,5)
        window.blit(text_button,(self.x +20, self.y + 15))
    
    def is_click(self) -> bool:
        mouse = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button = pygame.rect.Rect(self.x,self.y,120,50)
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
    def __init__(self,irow,jcol, width, height, total_row, total_col) -> None:
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
    
    def get_pos(self):
        return self.x,self.y
        
    def draw(self, window):
        pygame.draw.rect(window,self.color,(self.y * self.width,self.x*self.height+100,self.width,self.height+100))
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
        self.color =IRISBLUE

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
    
    def neighbors(self,grid):
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
                    '''
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
                    '''                
                else:
                    if grid[new_x][new_y].is_barrier():
                        check = False
                    '''
                    if grid[new_x][new_y].is_door:
                        key = "K" + str(grid[new_x][new_y].text[1])
                        if key not in collected_key:
                            check = False
                    '''
            else: check = False

            if check == True:
                if grid[new_x][new_y] not in self.neighbor:
                    self.neighbor.append(grid[new_x][new_y])

    def neighbors_door_valid(self,grid, collected_key):
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
                    
                    if grid[new_x][new_y].is_door:
                        key = "K" + str(grid[new_x][new_y].text[1])
                        if key not in collected_key:
                            check = False
                    
            else: check = False

            if check == True:
                if grid[new_x][new_y] not in self.neighbor:
                    self.neighbor.append(grid[new_x][new_y])
    
    def __lt__(self,other):
        return False


def read_grid_from_file(file_path):
    grid = []
    with open(file_path,'r') as file:
        row , coloumn = map(int, file.readline().strip().split(','))
        
        floor = file.readline().strip().split(',')
        

        for i in range(row):
            data = file.readline().strip().split(',')
            grid.append(data)
            
    return row, coloumn,floor, grid
    
def make_grid_color(row,col,width,height, grid):
    grid_color =[]
    start = None
    end =None
    for i in range(row):
        grid_color.append([])
        for j in range(col):
            node = Node(i,j,width//col,height//row,row,col)

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
            
    return grid_color,start,end 

def draw_grid_line(window,rows, cols,width, height):
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
            
    draw_grid_line(window,rows,cols,width,height)
    pygame.display.update()

def draw_solution(come,current,draw,start):
    path = {}
    while current in come:   
        path[come[current]] = current
        current = come[current]

    while start in path:
        pygame.time.delay(100)
        start.set_unvisible()
        start = path[start]
        start.set_path_color()
        draw()

# support for A* algorithm
def heuristic(start,end):
    x1,y1 = start
    x2,y2 = end
    # distance_to_key = set()
    # for i in grid:
    #     for node in i:
    #         if node.text.startswith("K"):
    #             dis = abs(x1 - node.x) + abs(y1 - node.y)
    #             distance_to_key.add(dis)
    return abs(x1-x2) + abs(y1-y2)

def astar_algorithm(draw, grid, start,end):
    count = 0
    frontier = PriorityQueue()
    frontier.put((0,count,start))
    come = {}
    g_cost ={node: float("inf") for i in grid for node in i}
    g_cost[start] =0
    f_cost = {node: float("inf") for i in grid for node in i}
    f_cost[start] = heuristic(start.get_pos(), end.get_pos())
    explored = {start}
    while not frontier.empty():
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        '''
        #collected_key.clear()
        current_node = frontier.get()[2]
        
        # current = current_node
        # while current in come:   
        #     if current.text.startswith("K"):
        #         key = str(current.text)
        #         if key not in collected_key:
        #             collected_key.add(key)    
        #     current = come[current]
        explored.remove(current_node)
        # current_node.neighbors(grid)
        # check current node is an end => draw
        if current_node == end:
            #draw_solution(come,end,draw,start)
            path = {}
            while end in come:   
                path[come[end]] = end
                end = come[end]
            return path
            # print("collected key: ",collected_key)  
            # start.set_start_color()
            # end.set_end_color()
        
        for neighbor in current_node.neighbor:
            temp_g_cost = g_cost[current_node] +1
            if temp_g_cost < g_cost[neighbor]:
                come[neighbor] = current_node
                
                g_cost[neighbor] = temp_g_cost
                f_cost[neighbor] = temp_g_cost + heuristic(neighbor.get_pos(),end.get_pos())
                if neighbor not in explored:
                    count+=1
                    frontier.put((f_cost[neighbor], count, neighbor))
                    explored.add(neighbor)
                    # neighbor.set_nodeOpen_color()
        draw()
        
        # if(current_node != start):
        #     current_node.set_nodeVisited_color()

    # print("collected key: ",collected_key)  
    return False

def astar_algorithm_with_checkpoints(draw, grid, checklist, collected_key):
    total_path = {}
    collected_key.clear()
    for i in range(len(checklist) - 1):
        start = checklist[i]
        end = checklist[i + 1]
        count = 0
        frontier = PriorityQueue()
        frontier.put((0,count,start))
        come = {}

        g_cost ={node: float("inf") for i in grid for node in i}
        g_cost[start] =0
        f_cost = {node: float("inf") for i in grid for node in i}
        f_cost[start] = heuristic(start.get_pos(), end.get_pos())
        
        explored = {start}
        
        while not frontier.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            #collected_key.clear()
            current_node = frontier.get()[2]
            
            current = current_node
            while current in come:   
                if current.text.startswith("K"):
                    key = str(current.text)
                    if key not in collected_key:
                        collected_key.add(key)    
                current = come[current]
            
            if current_node == start and current_node.text.startswith("K"):
                key = "K" + str(current_node.text[1])
                collected_key.add(key)
            explored.remove(current_node)
            #if start.text.startswith("K"):
            #    key = str(current_node.text)
            #    if key not in collected_key:
            #        collected_key.add(key)   
            current_node.neighbors_door_valid(grid, collected_key)
                
            if current_node == end:
                draw_solution(come,end,draw,start)
                path = {}
                while end in come:   
                    path[come[end]] = end
                    end = come[end]
                total_path.update(path)
                continue
                #return path
     
            for neighbor in current_node.neighbor:
                temp_g_cost = g_cost[current_node] +1
                
                if temp_g_cost < g_cost[neighbor]:
                    come[neighbor] = current_node
                    
                    g_cost[neighbor] = temp_g_cost
                    f_cost[neighbor] = temp_g_cost + heuristic(neighbor.get_pos(),end.get_pos())
                    if neighbor not in explored:
                        count+=1
                        frontier.put((f_cost[neighbor], count, neighbor))
                        explored.add(neighbor)
                        # neighbor.set_nodeOpen_color()
            draw()
            
            # if(current_node != start):
            #     current_node.set_nodeVisited_color()

        #return False
    draw_solution(total_path, checklist[len(checklist) - 1], draw, checklist[0])
    return total_path

def recursive (draw, grid, start,end, goal_list):
    path = astar_algorithm (draw, grid, start, end)
    for step in path:
        if step.text.startswith("D"):
            goal_list.append(step)
            key = "K" +str(step.text)[1]
            for i in grid:
                for node in i:
                    if node.text == key:
                        goal_list.append(node)
                        return recursive (draw, grid, start, node, goal_list)
    # for node in path:
    #     print (node.x, node.y)
    # print("goal list: ",goal_list)



def main(window, width, height):
    file = 'grid.txt'
    row, col,floor, temp_grid = read_grid_from_file(file)
    grid,start,end = make_grid_color(row,col,width,height,temp_grid)
    goal_list = []
    click1 = False
    click4 = False
    one_press = True
    collected_key = set()

    run = True
    while run:
        window.fill(WHITE)
        astar_button = Button(10, 10,"Go",click1)
        clear_button = Button(400, 10,"Clear",click4)
        draw_update(window,grid,row,col,width,height)     
        
        if(pygame.mouse.get_pressed()[0]) and one_press:
            one_press = False             
            if(astar_button.is_click()):
                click1 = True
                click4 =False
                clear_button.remove_click()
                clear_button.draw()
                
            if(clear_button.is_click()):
                click4 = True
                click1 = False
                goal_list.clear()
                astar_button.remove_click()
                astar_button.draw()
                grid,start,end = make_grid_color(row,col,width,height,temp_grid)
            
            if((click1)):
                for i in grid:
                    for node in i:
                        node.neighbors(grid)
                astar_button.set_click()
                astar_button.draw()
                recursive(lambda: draw_update(window, grid, row, col,width,height), grid, start, end, goal_list)
                goal_list.reverse() 
                goal_list.insert(0, start)
                goal_list.append(end)
                for i in goal_list:
                    print (i.text, end = " ")
                path = astar_algorithm_with_checkpoints(lambda: draw_update(window, grid, row, col,width,height), grid, goal_list, collected_key)
                # for i in range (len(goal_list) -1):
                #     path = astar_algorithm(lambda: draw_update(window, grid, row, col,width,height),grid,goal_list[i],goal_list[i+1])
                #     draw_update(window, grid, row, col, width, height)
                    
                # path = astar_algorithm_with_checkpoints(lambda: draw_update(window, grid, row, col,width,height),grid,goal_list)
                # draw_solution ()
                #for i in range(len(goal_list)):
                    #print(goal_list[i].get_pos())
                    #astar_algorithm(lambda: draw_update(window, grid, row, col,width,height), grid, goal_list[i], goal_list[i+1])
                #print(goal_list[0].text)

            
        if(not pygame.mouse.get_pressed()[0]) and not one_press:
            one_press =True
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        

    pygame.quit()
    
if __name__ == "__main__":
    main(window, WIDTH,HEIGHT-100)

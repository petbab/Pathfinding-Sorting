import pygame as py
import sys
from node_class import Node
from a_star import ASNode
from dijkstra import DijNode
from menu_node_class import MenuNode
from setup import block, sw, sh, screen, START, FINISH, font, s, screen_color, text_color, clock, fps
from button_class import Button
from file_class import File, algorithms, algorithms_cycle
from database_functions import update_database, read_database

py.init()

# create see-through background for menu
s.set_alpha(100)


# associate mouse position with node in Node.nodes
def mouse_in_block(mouse):
    if sw * block > mouse[0] > sw * block / 2 and mouse[1] < len(ASNode.nodes[0]) * block:
        return [True, DijNode.nodes[int(mouse[0] / block - sw / 2)][int(mouse[1] / block)]]
    elif sw * block / 2 > mouse[0] > 0 and mouse[1] < len(ASNode.nodes[0]) * block:
        return [True, ASNode.nodes[int(mouse[0] / block)][int(mouse[1] / block)]]
    else:
        return [False, False]


############################################### main search function ###################################################


def search(START, FINISH):
    DijNode.generate_nodes()
    ASNode.generate_nodes()

    start = False
    start_node_up = False
    finish_node_up = False

    buttons = []
    start_button = Button('START', 1)
    restart_button = Button('RESTART', 1)
    mirror_button = Button('MIRROR', 1)
    buttons.append(start_button)
    buttons.append(restart_button)
    buttons.append(mirror_button)
    Button.align_buttons(buttons, (0, (sh - 9) * block, sw * block, 9 * block))

    a_star_heuristic_button = Button(ASNode.heuristic_method, 1)
    a_star_heuristic_button.w = 200
    a_star_heuristic_button.x = sw * block / 2 - 310
    a_star_heuristic_button.y = start_button.y
    buttons.append(a_star_heuristic_button)

    mirror_mode = False
    last_interaction = 'a_star'

    weight_mode = 2

    # main loop
    while True:
        # clock.tick(fps)

        mouse = py.mouse.get_pos()
        pointer_block = mouse_in_block(mouse)[1]

        # loop through user input
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            elif event.type == py.KEYDOWN:
                # go to menu
                if event.key == py.K_ESCAPE:
                    Node.reset_nodes()
                    ASNode.reset_nodes()
                    DijNode.reset_nodes()
                    menu()
                # change weight mode
                elif event.key == py.K_1 or event.key == py.K_KP1:
                    weight_mode = 2
                elif event.key == py.K_2 or event.key == py.K_KP2:
                    weight_mode = 5
                elif event.key == py.K_3 or event.key == py.K_KP3:
                    weight_mode = 10
            elif event.type == py.MOUSEBUTTONDOWN:
                if start_button.in_button(mouse):
                    start = True
                elif restart_button.in_button(mouse):
                    Node.reset_nodes()
                    ASNode.reset_nodes()
                    DijNode.reset_nodes()
                    search(START, FINISH)
                elif mirror_button.in_button(mouse):
                    if mirror_mode:
                        mirror_mode = False
                    else:
                        mirror_mode = True
                        for i in range(len(ASNode.nodes)):
                            for j in range(len(ASNode.nodes[0])):
                                if last_interaction == 'a_star':
                                    DijNode.nodes[i][j].state = ASNode.nodes[i][j].state
                                    if DijNode.nodes[i][j].state == 'start':
                                        DijNode.open_set = [DijNode.nodes[i][j]]
                                    elif DijNode.nodes[i][j].state == 'finish':
                                        DijNode.final_set = [DijNode.nodes[i][j]]
                                else:
                                    ASNode.nodes[i][j].state = DijNode.nodes[i][j].state
                                    if ASNode.nodes[i][j].state == 'start':
                                        ASNode.open_set = [ASNode.nodes[i][j]]
                                    elif ASNode.nodes[i][j].state == 'finish':
                                        ASNode.final_set = [ASNode.nodes[i][j]]
                # cycle through a_star heuristics
                elif a_star_heuristic_button.in_button(mouse):
                    ASNode.change_heuristic()
                    a_star_heuristic_button.text = ASNode.heuristic_method
                # pick up and put down start and finish nodes
                elif not start and mouse_in_block(mouse)[0]:
                    if not start_node_up and pointer_block.state == 'start':
                        if mirror_mode:
                            DijNode.nodes[pointer_block.x][pointer_block.y].state = ''
                            ASNode.nodes[pointer_block.x][pointer_block.y].state = ''
                        else:
                            pointer_block.state = ''
                            last_interaction = pointer_block.algo
                        start_node_up = True
                    elif not finish_node_up and pointer_block.state == 'finish':
                        if mirror_mode:
                            DijNode.nodes[pointer_block.x][pointer_block.y].state = ''
                            ASNode.nodes[pointer_block.x][pointer_block.y].state = ''
                        else:
                            pointer_block.state = ''
                            last_interaction = pointer_block.algo
                        finish_node_up = True
                    elif start_node_up and pointer_block.state == '':
                        if mirror_mode:
                            DijNode.nodes[pointer_block.x][pointer_block.y].state = 'start'
                            ASNode.nodes[pointer_block.x][pointer_block.y].state = 'start'
                            DijNode.open_set = [DijNode.nodes[pointer_block.x][pointer_block.y]]
                            ASNode.open_set = [ASNode.nodes[pointer_block.x][pointer_block.y]]
                        else:
                            pointer_block.state = 'start'
                            last_interaction = pointer_block.algo
                            if pointer_block.algo == 'dijkstra':
                                DijNode.open_set = [pointer_block]
                            else:
                                ASNode.open_set = [pointer_block]
                        start_node_up = False
                    elif finish_node_up and pointer_block.state == '':
                        if mirror_mode:
                            DijNode.nodes[pointer_block.x][pointer_block.y].state = 'finish'
                            ASNode.nodes[pointer_block.x][pointer_block.y].state = 'finish'
                            DijNode.final_set = [DijNode.nodes[pointer_block.x][pointer_block.y]]
                            ASNode.final_set = [ASNode.nodes[pointer_block.x][pointer_block.y]]
                        else:
                            pointer_block.state = 'finish'
                            last_interaction = pointer_block.algo
                            if pointer_block.algo == 'dijkstra':
                                DijNode.final_set = [pointer_block]
                            else:
                                ASNode.final_set = [pointer_block]
                        finish_node_up = False

        # create and destroy walls
        if not start and mouse_in_block(mouse)[0] and not (start_node_up or finish_node_up):
            x = pointer_block.x
            y = pointer_block.y
            if py.mouse.get_pressed(5)[0]:
                if pointer_block.state == '':
                    if py.key.get_mods() & py.KMOD_SHIFT:
                        # create weighted nodes
                        if mirror_mode:
                            DijNode.nodes[pointer_block.x][pointer_block.y].weight = weight_mode
                            ASNode.nodes[pointer_block.x][pointer_block.y].weight = weight_mode
                            DijNode.nodes[pointer_block.x][pointer_block.y].tick = 0
                            ASNode.nodes[pointer_block.x][pointer_block.y].tick = 0
                        else:
                            if pointer_block.weight != weight_mode:
                                pointer_block.tick = 0
                            pointer_block.weight = weight_mode
                            last_interaction = pointer_block.algo
                    else:
                        if mirror_mode:
                            DijNode.nodes[pointer_block.x][pointer_block.y].state = 'wall'
                            ASNode.nodes[pointer_block.x][pointer_block.y].state = 'wall'
                            DijNode.nodes[pointer_block.x][pointer_block.y].tick = 0
                            ASNode.nodes[pointer_block.x][pointer_block.y].tick = 0
                        else:
                            pointer_block.tick = 0
                            pointer_block.state = 'wall'
                            last_interaction = pointer_block.algo
            elif py.mouse.get_pressed(5)[2]:
                if x != 0 and x != int(sw / 2) and x != int(sw / 2 - 1) \
                        and y != 0 and y != sh - 10:
                    if pointer_block.state == 'wall':
                        if mirror_mode:
                            DijNode.nodes[pointer_block.x][pointer_block.y].state = ''
                            ASNode.nodes[pointer_block.x][pointer_block.y].state = ''
                            DijNode.nodes[pointer_block.x][pointer_block.y].tick = 0
                            ASNode.nodes[pointer_block.x][pointer_block.y].tick = 0
                        else:
                            pointer_block.tick = 0
                            pointer_block.state = ''
                            last_interaction = pointer_block.algo
                    elif pointer_block.weight != 1:
                        if mirror_mode:
                            DijNode.nodes[pointer_block.x][pointer_block.y].weight = 1
                            ASNode.nodes[pointer_block.x][pointer_block.y].weight = 1
                            DijNode.nodes[pointer_block.x][pointer_block.y].tick = 0
                            ASNode.nodes[pointer_block.x][pointer_block.y].tick = 0
                        else:
                            pointer_block.tick = 0
                            pointer_block.weight = 1
                            last_interaction = pointer_block.algo

        if start:
            DijNode.solve()
            ASNode.solve()

        # redraw background
        screen.fill(screen_color)

        # draw buttons and react to mouse
        for b in buttons:
            if b.text == 'MIRROR':
                if mirror_mode:
                    if b.in_button(mouse):
                        b.show((50, 255, 150))
                    else:
                        b.show((125, 255, 175))
                else:
                    if b.in_button(mouse):
                        b.show((255, 100, 75))
                    else:
                        b.show((255, 125, 75))
            else:
                if b.in_button(mouse):
                    b.show((50, 150, 255))
                else:
                    b.show((125, 175, 255))

        # get path length
        dij_path_length = DijNode.final_set[0].step
        dij_visited_nodes = len(DijNode.closed_set)
        a_star_path_length = ASNode.final_set[0].step
        a_star_visited_nodes = len(ASNode.closed_set)

        # draw text with path length and algorithm names
        dij_pl_text = font.render(f'Path Length: {dij_path_length}', True, text_color)
        dij_vn_text = font.render(f'Visited Nodes: {dij_visited_nodes}', True, text_color)
        screen.blit(dij_pl_text, (sw * block / 2 + 180, mirror_button.y + 6))
        screen.blit(dij_vn_text, (sw * block / 2 + 180, restart_button.y + 6))

        a_star_pl_text = font.render(f'Path Length: {a_star_path_length}', True, text_color)
        a_star_vn_text = font.render(f'Visited Nodes: {a_star_visited_nodes}', True, text_color)
        screen.blit(a_star_pl_text, (sw * block / 2 - 385, mirror_button.y + 6))
        screen.blit(a_star_vn_text, (sw * block / 2 - 385, restart_button.y + 6))

        dijkstra = font.render('Dijkstra', True, (125, 175, 255))
        a_star = font.render('A-Star', True, (125, 175, 255))
        screen.blit(dijkstra, (sw * block / 2 + 180, start_button.y + 6))
        screen.blit(a_star, (sw * block / 2 - 400, start_button.y + 6))

        # draw all nodes
        DijNode.show_nodes()
        ASNode.show_nodes()

        # draw picked up start and finish nodes
        if start_node_up:
            py.draw.circle(screen, (0, 255, 0), mouse, block / 2)
        elif finish_node_up:
            py.draw.circle(screen, (255, 0, 0), mouse, block / 2)

        py.display.update()


################################################ main sort function ####################################################


def sort(algo):
    start = False
    cycles = 0
    # variable for updating database once
    run_once = 0
    algo_choice = 0

    # generate all files
    File.reset()
    File.generate_files()
    for i in algorithms_cycle:
        algorithms[i].reset()
        algorithms[i].files = File.files

    buttons = []
    algo_button = Button(algo.upper(), 1)
    buttons.append(algo_button)
    start_button = Button('START', 1)
    buttons.append(start_button)
    restart_button = Button('RESTART', 1)
    buttons.append(restart_button)
    step_button = Button('STEP BY STEP', 1)
    buttons.append(step_button)
    step_mode = False
    Button.align_buttons(buttons, (0, (sh - 9) * block, sw * block, 9 * block))

    color_mode_button = Button(File.color_modes[File.color], 1)
    Button.align_buttons([color_mode_button], (0, (sh - 9) * block, sw * block / 2, 9 * block))
    buttons.append(color_mode_button)

    # get data from database
    data = read_database()

    # main loop
    while True:
        # clock.tick(fps)

        # update average algorithm speed
        average_cycle = int(data[algorithms_cycle.index(algo)][0] / data[algorithms_cycle.index(algo)][1])

        mouse = py.mouse.get_pos()

        # loop through user input
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            elif event.type == py.KEYDOWN:
                # go to menu
                if event.key == py.K_ESCAPE:
                    menu()
                elif event.key == py.K_r:
                    run_once = 0
                    start = False
                    cycles = 0
                    File.reset()
                    File.generate_files()
                    for i in algorithms:
                        algorithms[i].reset()
                        algorithms[i].files = File.files
                elif event.key == py.K_s:
                    start = True
                elif event.key == py.K_RIGHT or event.key == py.K_LEFT:
                    if start:
                        run_once = 0
                        start = False
                        cycles = 0
                        File.reset()
                        File.generate_files()
                        for i in algorithms:
                            algorithms[i].reset()
                            algorithms[i].files = File.files
                    if event.key == py.K_RIGHT:
                        algo_choice += 1
                    else:
                        if algo_choice == 0:
                            algo_choice = len(algorithms_cycle)
                        algo_choice -= 1
                    algo = algorithms_cycle[algo_choice % len(algorithms_cycle)]
                    algo_button.text = algo.upper()
            elif event.type == py.MOUSEBUTTONDOWN:
                if start_button.in_button(mouse):
                    start = True
                elif restart_button.in_button(mouse):
                    run_once = 0
                    start = False
                    cycles = 0
                    File.reset()
                    File.generate_files()
                    for i in algorithms:
                        algorithms[i].reset()
                        algorithms[i].files = File.files
                # cycle through algorithms
                elif algo_button.in_button(mouse):
                    if start:
                        run_once = 0
                        start = False
                        cycles = 0
                        File.reset()
                        File.generate_files()
                        for i in algorithms:
                            algorithms[i].reset()
                            algorithms[i].files = File.files
                    algo_choice += 1
                    algo = algorithms_cycle[algo_choice % len(algorithms_cycle)]
                    algo_button.text = algo.upper()
                elif step_button.in_button(mouse):
                    if step_mode:
                        step_mode = False
                    else:
                        step_mode = True
                elif color_mode_button.in_button(mouse):
                    File.color = (File.color + 1) % len(File.color_modes)
                    color_mode_button.text = File.color_modes[File.color]
                    for file in File.files:
                        file.get_color()
                elif step_mode and start and not algorithms[algo].done:
                    algorithms[algo].sort()
                    cycles += 1

        if not algorithms[algo].done and start and not step_mode:
            algorithms[algo].sort()
            cycles += 1
        elif algorithms[algo].done:
            # update database
            if run_once == 0:
                data[algorithms_cycle.index(algo)][0] += cycles
                data[algorithms_cycle.index(algo)][1] += 1
                update_database(data)
                run_once += 1

        # draw background
        screen.fill(screen_color)

        # draw complexity and efficiency text
        cycle_counter = font.render(f'Cycles: {cycles}', True, text_color)
        screen.blit(cycle_counter, (sw * block / 2 + 180, restart_button.y + 20))
        average_cycle_text = font.render(f'Average cycles: {average_cycle}', True, text_color)
        screen.blit(average_cycle_text, (sw * block / 2 + 180, start_button.y + 20))
        complexity_text = font.render(f'Complexity: {algorithms[algo].complexity}', True, text_color)
        screen.blit(complexity_text, (sw * block / 2 + 180, algo_button.y + 20))

        # show buttons and react to mouse
        for b in buttons:
            if b.text == 'STEP BY STEP':
                if step_mode:
                    if b.in_button(mouse):
                        b.show((50, 255, 150))
                    else:
                        b.show((125, 255, 175))
                else:
                    if b.in_button(mouse):
                        b.show((255, 100, 75))
                    else:
                        b.show((255, 125, 75))
            else:
                if b.in_button(mouse):
                    b.show((50, 150, 255))
                else:
                    b.show((125, 175, 255))

        algorithms[algo].show_files(step_mode)

        py.display.update()


################################################ main menu function ####################################################


def menu():
    MenuNode.generate_menu_nodes()

    buttons = []
    search_button = Button('PATHFINDING', 1)
    sort_button = Button('SORTING', 1)
    buttons.append(search_button)
    buttons.append(sort_button)
    Button.align_buttons(buttons, (0, 0, sw * block, sh * block))

    # main loop
    while True:
        # clock.tick(fps)

        mouse = py.mouse.get_pos()

        # loop through user input
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                # run search function
                if search_button.in_button(mouse):
                    Node.reset_nodes()
                    DijNode.reset_nodes()
                    ASNode.reset_nodes()
                    MenuNode.reset_nodes()
                    search(START, FINISH)
                # run sort function
                elif sort_button.in_button(mouse):
                    sort('bubble')

        # draw background
        screen.fill(screen_color)
        s.fill(screen_color)

        MenuNode.solve()

        # draw menu nodes
        MenuNode.show_nodes()

        # draw see through background
        screen.blit(s, (0, 0))

        # draw buttons and react to mouse
        for b in buttons:
            if b.in_button(mouse):
                b.show((50, 150, 255))
            else:
                b.show((125, 175, 255))

        py.display.update()


if __name__ == '__main__':
    menu()

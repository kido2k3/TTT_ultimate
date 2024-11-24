from state import State, State_2
import time
from importlib import import_module
# import  logging

# Cấu hình # logging để ghi đè tệp log mỗi lần chạy
# logging.basicConfig(filename='game_log.txt', level=# logging.INFO, format='%(message)s', filemode='w')

def main(player_X, player_O, rule = 2):
    dict_player = {1: 'X', -1: 'O'}
    if rule == 1:
        cur_state = State()
    else:
        cur_state = State_2()
    turn = 1    

    limit = 81
    remain_time_X = 120
    remain_time_O = 120
    
    player_1 = import_module(player_X)
    player_2 = import_module(player_O)
    
    while turn <= limit:
        # logging.info("turn: %d\n", turn)
        if cur_state.game_over:
            # logging.info("winner: %s", dict_player[cur_state.player_to_move * -1])
            if dict_player[cur_state.player_to_move * -1] == 'X':
                count[0] += 1
            elif dict_player[cur_state.player_to_move * -1] == 'O':
                count[1] += 1
            
            break
        
        start_time = time.time()
        if cur_state.player_to_move == 1:
            new_move = player_1.select_move(cur_state, remain_time_X)
            elapsed_time = time.time() - start_time
            remain_time_X -= elapsed_time
        else:
            new_move = player_2.select_move(cur_state, remain_time_O)
            elapsed_time = time.time() - start_time
            remain_time_O -= elapsed_time
            
        if new_move is None:
            break
        
        if remain_time_X < 0 or remain_time_O < 0:
            # logging.info("out of time")
            print("out of time")
            # logging.info("winner: %s", dict_player[cur_state.player_to_move * -1])
            break
                
        if elapsed_time > 10.0:
            print("elapsed time: %f", elapsed_time)
            # logging.info("elapsed time: %f", elapsed_time)
            # logging.info("winner: %s", dict_player[cur_state.player_to_move * -1])
            break
        
        cur_state.act_move(new_move)
        # logging.info(cur_state)
        
        turn += 1
        
    # logging.info("X: %d", cur_state.count_X)
    # logging.info("O: %d", cur_state.count_O)
    # logging.info("remain_time_X: %d", remain_time_X)
    # logging.info("remain_time_O: %d", remain_time_O)


count = [0, 0]
for i in range (100) :
    main('random_agent', '_MSSV', 2)
    print("end game ", i)
    print (count[0], count[1])

print (count[0], count[1])
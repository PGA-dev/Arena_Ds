'''controller_instance'''
'''name, arena_level, damage, hp, to_hit, strength, ac'''


from game_pkg import c_r_u_d
from game_pkg import exceptions as mvc_exc
from game_pkg import arena_method as a_h_m
from game_pkg.game_controller import Game_Controller 
from game_pkg.game_model import ModelDataset
from game_pkg.game_view import Game_View





'''
Driver code Entry Point for Game
'''

def main():

    # Main Data List of Dictionaries
    opponents: list = [{"name": "Brute", "ac": 3, "damage": 75, "hp": 200, "to_hit": 15},
                       {"name": "Inside", "ac": 8, "damage": 45, "hp": 100, "to_hit": 65},
                       {"name": "Dodge", "ac": 15, "damage": 35, "hp": 75, "to_hit": 75},
                       {"name": "Right_Hook", "ac": 7, "damage": 50, "hp": 100, "to_hit": 35},
                       {"name": "Feet", "ac": 5, "damage": 60, "hp": 120, "to_hit": 25}]


    '''
    Practice area
    '''
    # insert_char(conn, 'DeathLaser', ac=7, damage=50, hp=175,to_hit=30, table_name='chars')
    # print(select_char(conn, 'Brute', table_name='chars'))
    # print(select_all(conn, table_name='chars'))

 
    '''
    Practice area
    '''
    # insert_char(conn, 'DeathLaser', ac=7, damage=50, hp=175,to_hit=30, table_name='chars')
    # print(select_char(conn, 'Brute', table_name='chars'))
    # print(select_all(conn, table_name='chars'))

    '''
    Game Driver Code
    '''
    opponent1 = Game_Controller(ModelDataset(opponents), Game_View())
    opponent1.show_chars()
    opponent2 = Game_Controller(ModelDataset(opponents), Game_View())
    opponent2.show_char('Brute')

    #battle = battle_cycle(opponent1, opponent2 )

if __name__ == '__main__':
    main()

import sqlite3
from time import time
from pathlib import Path
from classes import Game, Field, Cell
from settings import Settings as s


class Backup:
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent
    backup_file = project_root / 'data' / 'saved_data'
    other_backup_file = project_root / 'data' / 'saved_data_cruel'
    field_names = [
        'difficulty',
        'field',
        'current_record',
        'opened_cells',
        'flags',
        'mine_places'
        ]
    
    @staticmethod
    def __deserialize_field(ser_field):
        deser_field = []
        transmit_data = eval(ser_field)
        for row in transmit_data:
            deser_field.append([])
            for col in row:
                deser_field[-1].append(Cell(**col))
        return deser_field


    @classmethod
    def get_time(cls):
        conn = sqlite3.connect(f'{cls.backup_file}.db')
        cursor = conn.cursor()
        timer = cursor.execute('''SELECT CAST(time AS INTEGER) FROM GameData WHERE difficulty = ?;''', (s.current_difficulty,)).fetchall()[0][0]
        conn.close()
        return timer
    
    
    @classmethod
    def get_backup(cls):
        conn = sqlite3.connect(f'{cls.backup_file}.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS GameData (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    difficulty TEXT UNIQUE,
                    field TEXT,
                    current_record INTEGER,
                    opened_cells INTEGER,
                    flags INTEGER,
                    mine_places TEXT,
                    time INTEGER
                    );
                    ''')
        diff_data = [('easy',), ('medium',), ('hard',)]
        cursor.executemany('''INSERT OR IGNORE INTO GameData (difficulty) VALUES (?);''', diff_data)
        cursor.execute('''SELECT * FROM GameData WHERE difficulty = ?;''', (s.current_difficulty,))
        saved_game = cursor.fetchall()
        current_field = cls.__deserialize_field(saved_game[0][2]) if saved_game[0][2] else None
        zipped_field = Field(field=current_field, size=len(current_field), mines=s.field_params[s.current_difficulty][1]) if current_field else None
        conn.commit()
        conn.close()
        timer = cls.get_time()
        return Game(
                    dificulty=saved_game[0][1],
                    game_field=zipped_field,
                    current_record=int(saved_game[0][3]) if saved_game[0][3] is not None else 0,
                    opened_cells=int(saved_game[0][4]) if saved_game[0][4] is not None else 0,
                    flags=int(saved_game[0][5]) if saved_game[0][5] is not None else s.field_params[s.current_difficulty][1],
                    mine_places=eval(saved_game[0][6]) if saved_game[0][6] is not None else None,
                    expire_time=timer+time() if timer else None
                    )

    
    @classmethod
    def save_backup(cls, game, timer=None):
        conn = sqlite3.connect(f'{cls.backup_file}.db')
        cursor = conn.cursor()
        cursor.execute(f'''UPDATE GameData SET field=?,
                        current_record=?,
                        opened_cells=?,
                        flags=?,
                        mine_places=?
                        WHERE difficulty=?;''',
                        (str(game.game_field.field), game.record, game.opened_cells, game.flags, str(game.mine_places), s.current_difficulty)
        )
        if timer is not None:
            cursor.execute(f'''UPDATE GameData SET time=? WHERE difficulty=?''', (timer, s.current_difficulty))
        conn.commit()
        conn.close()
           
            
    @classmethod
    def swapmode(cls):
        cls.backup_file, cls.other_backup_file = cls.other_backup_file, cls.backup_file
        
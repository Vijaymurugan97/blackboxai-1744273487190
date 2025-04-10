import sqlite3
import pandas as pd
import os
import sys
from ensure_directories import ensure_app_directories

class Database:
    def __init__(self):
        # Get data directory from ensure_directories module
        data_dir, _ = ensure_app_directories()
        
        # Store database in data directory
        self.db_path = os.path.join(data_dir, "pdf_data.db")
        self.setup_database()

    def setup_database(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DROP TABLE IF EXISTS pdf_data')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS pdf_data (
                        ata TEXT,
                        task_number TEXT,
                        description TEXT,
                        mpn TEXT,
                        pn TEXT,
                        time_limit TEXT,
                        lir_type TEXT,
                        margin TEXT,
                        reference TEXT
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Database setup error: {str(e)}")

    def save_processed_data(self, df: pd.DataFrame):
        try:
            # Convert DataFrame to list of tuples
            data = df[["ATA", "Task Number", "Description", "MP/N", "PN", "Limit", "Type of LIR", "Margin", "Reference"]].values.tolist()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany('''
                    INSERT INTO pdf_data (
                        ata, task_number, description, mpn, pn, 
                        time_limit, lir_type, margin, reference
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)
                conn.commit()
        except Exception as e:
            print(f"Save data error: {str(e)}")

    def get_suggestions(self, column: str, partial_value: str, limit: int = 5):
        try:
            # Map column names
            column_map = {
                'ATA': 'ata',
                'Task Number': 'task_number',
                'Description': 'description',
                'MP/N': 'mpn',
                'PN': 'pn',
                'Limit': 'time_limit',
                'Type of LIR': 'lir_type',
                'Margin': 'margin',
                'Reference': 'reference'
            }
            db_column = column_map.get(column, column.lower())
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    SELECT DISTINCT {db_column}
                    FROM pdf_data 
                    WHERE {db_column} LIKE ?
                    LIMIT ?
                ''', (f'%{partial_value}%', limit))
                return [row[0] for row in cursor.fetchall() if row[0]]
        except Exception as e:
            print(f"Get suggestions error: {str(e)}")
            return []

import os
import pandas as pd
from results.models import Result

def parse_file(file_name):
    file, ext = os.path.splitext(file_name)
    match ext:
        case '.csv':
            parse_csv(file_name)
        case '.xlsx':
            parse_excel(file_name)
        case '.xls':
            parse_excel(file_name)
        case _:
            raise ValueError(f"Unsupported file type: {ext}")

def parse_excel(file_name):
    dfs = pd.read_excel(file_name)

    

def parse_csv(file_name):
    pass
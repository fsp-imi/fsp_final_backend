import pandas as pd
import os
import json

def results_parse(file_path, district_col, region_col, commands_col, results_col, output_file=None):
    file, ext = os.path.splitext(file_path)
    match ext:
        case '.csv':
            df = pd.read_csv(file_path)
        case '.xlsx' | '.xls':
            df = pd.read_excel(file_path)
        case _:
            raise ValueError(f"Unsupported file type: {ext}")

    parsed_df = df.iloc[:, [district_col, region_col, commands_col, results_col]]
    parsed_df.columns = ['District', 'Region', 'Commands', 'Results']  # Rename columns for clarity

    # Convert DataFrame to JSON array of objects
    result_json = parsed_df.to_dict(orient='records')

    # Save to a file if output_file is specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(result_json, file, ensure_ascii=False, indent=4)

    return result_json

# Parse the uploaded file and optionally save to a file
file_path = '../data/product_championship_result_1.xlsx'
output_file_path = '../data/parsed_results.json'

parsed_json = results_parse(file_path, 4, 5, 6, 7, output_file=output_file_path)

print(parsed_json)
# ChatCSV

This Python script uses the OpenAI API to translate the content of specific columns in a CSV file. It utilizes the GPT-3.5-turbo model for translation and saves the translated content in new columns within the output file.

Requirements
- Python 3
- pandas
- openai
- tqdm
- shelve

Setup
1. Install the required packages:
   ```
   pip install pandas openai tqdm shelve
   ```
2. Set your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY=<your_openai_api_key>
   ```

Usage
1. Update the `input_file` variable with the path to your input CSV file.
2. Define the columns you want to translate and the corresponding instructions in the `column_instructions` list.
3. Run the script with `python script_name.py`.

## How It Works
The script consists of several functions:

- split_text(): Splits the input text into smaller parts to fit within the OpenAI API character limit.
- log_request_and_response(): Logs API requests and responses to a file called api_log.txt.
- chatcsv(): Translates a single text using the GPT-3.5-turbo model.
- process_row(): Processes a single row of the input CSV file, applying the translation function to specified columns.

The script reads the input CSV file, processes each row according to the specified column instructions, and saves the results in a new CSV file called test_translated.csv.

The `column_instructions` list should be formatted as follows:

```
column_instructions = [
    ('column1', 'ignore', ''),
    ('column2', 'user message', 'system message'),
    ('column3', 'user message', 'system message'),
    ('column4', 'user message', 'system message'),
]
```

Each tuple in the list corresponds to a single column in the input CSV file.
The first element of the tuple is the column name.
The second element is the user message, which will be used to guide the translation model.
The third element is the system message, which sets the context for the translation model.

## Example
Given an input CSV file with columns 'column1', 'column2', 'column3', and 'column4', the script will create a new output file with additional columns containing translated content (e.g., 'column2_translated', 'column3_translated', 'column4_translated').

After configuring the script and running it, you will see the following message:

```
Verwerking voltooid. Verwerkte gegevens opgeslagen in test_translated.csv
```
This indicates that the script has successfully processed the input file, and the translated data is stored in the test_translated.csv file.

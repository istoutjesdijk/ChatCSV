import os
import openai
import pandas as pd
from tqdm import tqdm
import shelve

# Authenticeer en configureer de OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Functie om tekst op te splitsen in kleinere delen
def split_text(text, max_length):
    if len(text) <= max_length:
        return [text]

    parts = []
    while len(text) > max_length:
        split_index = text[:max_length].rfind('.')
        if split_index == -1:
            split_index = max_length
        parts.append(text[:split_index + 1].strip())
        text = text[split_index + 1:].strip()
    parts.append(text)
    return parts

# Logfunctie om API-aanvragen en -antwoorden vast te leggen
def log_request_and_response(request, response):
    with open("api_log.txt", "a") as log_file:
        log_file.write(f"Request: {request}\n")
        log_file.write(f"Response: {response}\n\n")

# Functie om een enkele tekst te vertalen
def chatcsv(text, instruction, system_message):  # Functienaam aangepast
    with shelve.open('translation_cache') as translation_cache:
        if instruction == 'ignore':
            return text

        max_length = 4000
        translated_parts = []

        text_parts = split_text(text, max_length)
        for part in text_parts:
            cache_key = f"{instruction}:{part}"

            if cache_key in translation_cache:
                translated_part = translation_cache[cache_key]
            else:
                messages = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"{instruction} {part}"}
                ]

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.2
                )

                translated_part = response.choices[0].message['content'].strip()
                translation_cache[cache_key] = translated_part

                # Log API-aanvraag en -antwoord
                log_request_and_response({"model": "gpt-3.5-turbo", "messages": messages, "temperature": 0.2}, response['choices'][0])

            translated_parts.append(translated_part)

        return ' '.join(translated_parts)

# Functie om een enkele rij te verwerken
def process_row(row, column_instructions):
    for column_name, instruction, system_message in column_instructions:
        translated_column_name = f"{column_name}_translated"
        row[translated_column_name] = chatcsv(row[column_name], instruction, system_message)  # Verwijzing aangepast
    return row

# Lees het CSV-bestand
input_file = 'test.csv'
df = pd.read_csv(input_file)

# Definieer de kolommen die u wilt vertalen en de bijbehorende instructies
column_instructions = [
    ('column1', 'ignore', ''),
    ('column2', 'user message', 'system message'),
    ('column3', 'user message', 'system message'),
    ('column4', 'user message', 'system message'),
]

# Voeg vertaalde kolommen toe aan het DataFrame
for column_name, _, _ in column_instructions:
    df[f"{column_name}_translated"] = ""

# Vertaal elke rij in het DataFrame en sla het resultaat op
output_file = 'test_translated.csv'
tqdm.pandas()
df.progress_apply(lambda row: process_row(row, column_instructions), axis=1).to_csv(output_file, index=False)

print(f"Verwerking voltooid. Verwerkte gegevens opgeslagen in {output_file}")
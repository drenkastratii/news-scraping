import ollama
import csv
import os

client = ollama.Client()

PATH = r'C:\Users\Dren\Desktop\rit-final\backend\db'
INPUT_FILE = 'news.csv'
OUTPUT_FILE = 'news_modified.csv'

input_path = os.path.join(PATH, INPUT_FILE)
output_path = os.path.join(PATH, OUTPUT_FILE)

model = 'llama3.2'

news_list = []

with open(input_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        news_list.append(row)

print(f"Loaded {len(news_list)} articles.")

for row in news_list:
    original_title = row["news_title"]

    prompt = f"""
                Rewrite the following news headline to be clearer, more engaging, and more professional.
                Return ONLY the improved headline and nothing else.

                Headline: {original_title}
            """

    response = client.generate(model=model, prompt=prompt)
    row["news_title"] = response.response.strip('"""',)

print("Headlines rewritten.")


with open(output_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=news_list[0].keys())
    writer.writeheader()
    writer.writerows(news_list)

print("Modified file saved successfully.")

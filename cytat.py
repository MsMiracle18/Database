import json
from pymongo import MongoClient

# Підключення до MongoDB
client = MongoClient('mongodb+srv://ms_miracle18:ryPanrIWBPIoqX0T@cluster0.d6hdlvu.mongodb.net/')
db = client['Cluster0']  # Замініть на вашу базу даних

# Завантаження авторів з JSON-файлу
with open('authors.json', 'r') as file:
    authors_data = json.load(file)

authors_collection = db['authors']
authors_collection.insert_many(authors_data)

# Завантаження цитат з JSON-файлу
with open('quotes.json', 'r') as file:
    quotes_data = json.load(file)

quotes_collection = db['quotes']
quotes_collection.insert_many(quotes_data)

while True:
    command = input("Введіть команду (наприклад, name: Steve Martin, tag: life, tags: life,live, exit): ")
    
    if command.startswith("name:"):
        # Пошук цитат за ім'ям автора
        author_name = command.split("name:")[1].strip()
        quotes = quotes_collection.find({"author": author_name})
        for quote in quotes:
            print(f'Цитата: {quote["text"]}')
        
    elif command.startswith("tag:"):
        # Пошук цитат за тегом
        tag = command.split("tag:")[1].strip()
        quotes = quotes_collection.find({"tags": tag})
        for quote in quotes:
            print(f'Цитата: {quote["text"]}')
        
    elif command.startswith("tags:"):
        # Пошук цитат за набором тегів
        tags = command.split("tags:")[1].strip().split(',')
        quotes = quotes_collection.find({"tags": {"$in": tags}})
        for quote in quotes:
            print(f'Цитата: {quote["text"]}')
        
    elif command == "exit":
        break
        
    else:
        print("Невідома команда. Спробуйте ще раз.")


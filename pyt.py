import os
from pathlib import Path

print("Рабочая директория:", os.getcwd())
print("Что лежит в data:", os.listdir("data") if os.path.isdir("data") else "папки data нет")
print("Файл существует:", Path("data/transactions_excel.xlsx").exists())

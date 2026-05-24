import os
from dotenv import load_dotenv
from langchain_gigachat.chat_models import GigaChat
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Инициализация модели
llm = GigaChat(
    credentials=os.getenv("GIGA_KEY"),
    verify_ssl_certs=False,
    temperature=0.2,
    max_tokens=1000
)

# Базовый промпт для извлечения количества людей
basic_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Проанализируй следующий текст заявки на аренду жилья и извлеки количество человек, которые будут проживать.

Текст заявки: {text}

Верни только число (целое число), соответствующее количеству проживающих.
Если количество не указано явно, постарайся определить его по контексту.

Количество человек:"""
)

# Создание цепочки
chain = basic_prompt | llm | StrOutputParser()

# Тестовые заявки
test_texts = [
    "Ищу квартиру для семьи из четырех человек на длительный срок",
    "Нужна студия для проживания одного человека рядом с метро",
    "Требуется двухкомнатная квартира для молодой пары",
    "Снимем жилье для троих студентов на учебный год",
    "Семья с двумя детьми ищет просторную квартиру"
]

for text in test_texts:
    result = chain.invoke({"text": text})
    print(f"Текст: {text}")
    print(f"Результат: {result}")
    print("---")

import pandas as pd

# Загрузка данных
df = pd.read_csv('rental/rental_28.csv', sep=';')
print(df.head())
print(df.dtypes)

# Прогоняем каждую заявку через модель
results = []
for _, row in df.iterrows():
    text = row["text"]
    try:
        result = chain.invoke({"text": text})
        results.append(result.strip())
    except Exception as e:
        results.append(f"ERROR: {e}")

# Сохраняем результаты
df["result"] = results
df.to_csv("rental_with_results.csv", index=False, encoding="utf-8-sig")
print("\nРезультаты сохранены!")
print(df[["text", "amount", "result"]].to_string())

# Считаем точность
df["result_num"] = pd.to_numeric(df["result"], errors='coerce')
correct = (df["result_num"] == df["amount"]).sum()
total = len(df)
accuracy = correct / total
print(f"\nВерных ответов: {correct} из {total}")
print(f"Точность: {accuracy:.1%}")
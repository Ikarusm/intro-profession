import os
import pandas as pd
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

# Базовый промпт
basic_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Проанализируй следующий текст заявки на аренду жилья и извлеки количество человек, которые будут проживать.

Текст заявки: {text}

Верни только число (целое число), соответствующее количеству проживающих.
Если количество не указано явно, постарайся определить его по контексту.

Количество человек:"""
)

chain = basic_prompt | llm | StrOutputParser()

# Загрузка данных
df = pd.read_csv('rental/rental_28.csv', sep=';')
print("Первые 5 строк:")
print(df.head())
print(f"\nВсего заявок: {len(df)}")

# Прогоняем через модель
results = []
for i, (_, row) in enumerate(df.iterrows()):
    text = row["text"]
    try:
        result = chain.invoke({"text": text})
        results.append(result.strip())
        print(f"Заявка {i+1}/{len(df)}: {result.strip()}")
    except Exception as e:
        results.append(f"ERROR: {e}")
        print(f"Заявка {i+1}/{len(df)}: ОШИБКА")

# Сохраняем результаты
df["result"] = results
df.to_csv("rental_with_results.csv", index=False, encoding="utf-8-sig")

# Считаем точность
df["result_num"] = pd.to_numeric(df["result"], errors='coerce')
correct = (df["result_num"] == df["amount"]).sum()
total = len(df)
errors = total - correct
accuracy = correct / total

print(f"\nВерных ответов: {correct} из {total}")
print(f"Ошибок: {errors}")
print(f"Точность: {accuracy:.1%}")
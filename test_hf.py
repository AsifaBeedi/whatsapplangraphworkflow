from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")
result = generator("Say hello!", max_length=20)
print(result)
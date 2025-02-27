# Source: 
import ollama

# Fonctions de base
ollama.list()
ollama.show('qwen2.5:3b')
ollama.pull('nomic-embed-text')

# Prompt simple
res1 = ollama.generate(
    model='qwen2.5:3b', 
    prompt='Quel langage de programmation fonctionnel choisir?'
    )

print(res1.response)

# Chat: prompt plus complexe
res2 = ollama.chat(
    model='qwen2.5:3b', 
    messages=[{'role': 'user', 'content': 'Qui es-tu?'}]
    )

print(res2.message.content)

# Embedding
texte = ["C'est un texte.", "Une phrase courte."]

embedding = ollama.embed(
    model = "bge-m3",
    input= texte
)

print(embedding.embeddings)
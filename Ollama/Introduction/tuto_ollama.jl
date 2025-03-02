# Source: https://juliapackages.com/p/promptingtools
using PromptingTools

const PT = PromptingTools
schema = PT.OllamaSchema()

# Chat
res = aigenerate(schema, "Quel langage de programmation fonctionnel choisir?"; model="qwen2.5:3b")

println(res)

# Embedding
texte = ["C'est un texte.", "Une phrase courte."]

embedding = aiembed(schema, texte, copy; model="qwen2.5:3b")

println(embedding.content)
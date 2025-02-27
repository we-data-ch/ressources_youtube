library(ollamar)

# Fonctions de base
list_models()
show('qwen2.5:3b')
pull('nomic-embed-text')

# Générer une réponse
res1 <- generate(
    model = 'qwen2.5:3b',
    prompt = 'Quel langage de programmation fonctionnel choisir?',
    output = "text"
)

res1

# Chat: prompt plus complexe
res2 <- chat(
    model = 'qwen2.5:3b',
    messages = list(list(role = 'user', content = 'Qui es-tu?')),
    output = "text"
)

res2

# Embedding
texte <- c("C'est un texte.", "Une phrase courte.")

embedding <- embed(
    model = "bge-m3",
    input = texte
)

embedding
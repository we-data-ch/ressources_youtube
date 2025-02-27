import llama_leap

let ollama = newOllamaAPI()

# Générer du code
var res = ollama.generate("qwen2.5", "Quel langage de programmation fonctionnel choisir?")
echo res

# Embedding
var embedding = ollama.generateEmbeddings("bge-m3", "Un texte")
echo embedding.embedding
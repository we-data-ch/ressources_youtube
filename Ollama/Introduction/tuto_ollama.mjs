// Source: 
import ollama from 'ollama'

// Fonctions de base
console.log(await ollama.list())
console.log(await ollama.show({model: 'qwen2.5:3b'}))
console.log(await ollama.pull({model: 'nomic-embed-text'}))

// Prompt simple
let res1 = await ollama.generate({
  model: 'qwen2.5:3b', 
  prompt: 'Quel langage de programmation fonctionnel choisir?'
  })

console.log(res1.response)

// Chat
let response = await ollama.chat({
    model: 'qwen2.5:3b',
    messages: [{ role: 'user', content: 'Qui es-tu?' }],
  })

console.log(response.message.content)
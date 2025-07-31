<template>
  <div class="flex flex-col items-center gap-4 p-8 bg-gray-100 min-h-screen">
    <h2 class="text-2xl font-bold">🎙️ Voice AI Assistant</h2>

    <button
      class="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600"
      @click="startListening"
    >
      Start Speaking
    </button>

    <div class="mt-4 w-full max-w-md bg-white p-4 rounded shadow">
      <p><strong>Question:</strong> {{ transcript }}</p>
      <p class="mt-2"><strong>JarvisAi:</strong> {{ aiResponse }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const transcript = ref('')
const aiResponse = ref('')

const startListening = () => {
  const recognition = new window.webkitSpeechRecognition()
  recognition.lang = 'en-US'
  recognition.interimResults = false
  recognition.maxAlternatives = 1

  recognition.onresult = async (event) => {
    transcript.value = event.results[0][0].transcript
    console.log('Voice input:', transcript.value)

    // Call backend (you can replace this with your actual fetch)
    const response = await fetch('http://localhost:8000/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: transcript.value }),
    })

    const data = await response.json()
    aiResponse.value = data.answer || 'No response from AI'

    speakText(aiResponse.value)
  }

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error)
  }

  recognition.start()
}

const speakText = (text) => {
  const synth = window.speechSynthesis
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'en-US'
  synth.speak(utterance)
}
</script>

<style scoped>
/* Optional styles */
</style>

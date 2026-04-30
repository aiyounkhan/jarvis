import edge_tts
import asyncio
import tempfile
import os
import threading
import queue
from playsound import playsound
import re

class Speaker:
    def __init__(self):
        self.voice = "en-GB-RyanNeural"
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _clean(self, text):
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = re.sub(r'`+', '', text)
        return text.strip()

    def _run(self):
        while True:
            text = self.queue.get()
            asyncio.run(self._speak(text))
            self.queue.task_done()

    async def _speak(self, text):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name

        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(tmp_path)
        playsound(tmp_path)
        os.remove(tmp_path)

    def speak(self, text):
        print(f"\nJARVIS: {text}\n")
        cleaned = self._clean(text)
        self.queue.put(cleaned)
        self.queue.join()
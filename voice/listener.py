import sounddevice as sd
import numpy as np
import whisper

class Listener:
    def __init__(self):
        print("Loading Whisper model...")
        self.model = whisper.load_model("base")
        self.sample_rate = 16000
        self.device = 1

    def listen(self):
        print("\nListening... (press Enter to stop)")
        
        audio_chunks = []
        
        def callback(indata, frames, time, status):
            audio_chunks.append(indata.copy())
        
        with sd.InputStream(samplerate=self.sample_rate, channels=1, 
                          callback=callback, device=self.device):
            input()
        
        if not audio_chunks:
            return ""
            
        audio = np.concatenate(audio_chunks, axis=0).flatten()
        
        if len(audio) < self.sample_rate:
            return ""
        
        print("Transcribing...")
        result = self.model.transcribe(audio, fp16=False)
        return result["text"].strip()
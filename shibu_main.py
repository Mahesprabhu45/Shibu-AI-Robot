from __future__ import annotations
import os, time, subprocess, warnings, sys
from typing import Optional
import speech_recognition as sr
import pyaudio

# ============================================================
#        SYSTEM AUDIO FIXES (REMOVE ALSA & JACK ERRORS)
# ============================================================
os.environ["PYAUDIO_USE_PULSE"] = "1"
os.environ["SDL_AUDIODRIVER"] = "pulse"
os.environ["PULSE_SERVER"] = "unix:/run/user/1000/pulse/native"
os.environ["AUDIODEV"] = "pulse"
os.environ["ALSA_LOGLEVEL"] = "none"
os.environ["JACK_NO_START_SERVER"] = "1"

warnings.filterwarnings("ignore")
sys.stderr = open(os.devnull, "w")

# ============================================================
#                      IMPORT LLM
# ============================================================
try:
    from llama_cpp import Llama
except Exception:
    Llama = None

# ============================================================
#                     OFFLINE TTS ENGINE
# ============================================================
try:
    import pyttsx3
    engine = pyttsx3.init()
except Exception:
    pyttsx3 = None
    engine = None


# ============================================================
#                       SHIBU CORE
# ============================================================
class ShibuCore:
    def __init__(self) -> None:
        self.recognizer: Optional[sr.Recognizer] = None
        self.mic: Optional[sr.Microphone] = None
        self.mic_index = 0

        # commands folder (auto-execute)
        self.commands_path = "./commands"

        # Load Local LLM
       # model_path = "./models/phi-2-q4.gguf"
        model_path = "./models/gemma3-1b-q4_k_m.gguf"
        self.llm = None

        if Llama and os.path.exists(model_path):
            try:
                print(f"[LLM] Loading model: {model_path}")
                self.llm = Llama(
                    model_path=model_path,
                    n_ctx=1024,
                    n_threads=4,
                    n_gpu_layers=0,
                    verbose=False,
                )
                print("[LLM] Model ready.")
            except Exception as e:
                print(f"[LLM Load Error] {e}")
        else:
            print("[LLM] Model not found.")

    # --------------------------------------------------
    # Initialize Microphone
    # --------------------------------------------------
    def initialize(self, mic_index=0):
        print("[Core] Booting Shibu...")
        time.sleep(1)

        self._detect_mics()
        self.mic_index = mic_index
        self._init_mic()

        self.speak("Hello sir, Shibu is online and ready to assist you sir.")

    def _detect_mics(self):
        p = pyaudio.PyAudio()
        try:
            count = p.get_device_count()
            print(f"[Audio] {count} audio devices found.")
            for i in range(count):
                info = p.get_device_info_by_index(i)
                if info.get("maxInputChannels", 0) > 0:
                    print(f" â Using mic: {info.get('name')} (index {i})")
                    self.mic_index = i
                    break
        finally:
            p.terminate()

    def _init_mic(self):
        try:
            self.recognizer = sr.Recognizer()
            self.mic = sr.Microphone(device_index=self.mic_index)
            print(f"[Audio] Microphone initialized (index={self.mic_index})")
        except Exception as e:
            print(f"[Mic Error] {e}")

    # --------------------------------------------------
    # SPEAK â€ OFFLINE TTS
    # --------------------------------------------------
    def speak(self, text: str):
        print(f"[Shibu] {text}")

        try:
            if engine:
                engine.say(text)
                engine.runAndWait()
                return
        except Exception as e:
            print(f"[TTS Error] {e}")

    # --------------------------------------------------
    # LISTEN USING MICROPHONE
    # --------------------------------------------------
    def listen(self, phrase_time_limit=5) -> Optional[str]:
        if not self.mic:
            self.speak("Microphone is not initialized sir.")
            return None

        with self.mic as source:
            self.speak("Listening sir...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)

            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=phrase_time_limit)
            except:
                self.speak("I heard nothing sir.")
                return None

        try:
            text = self.recognizer.recognize_google(audio)
            self.speak(f"You said {text}")
            return text.lower()
        except:
            self.speak("Sorry sir, I could not understand.")
            return None

    # ------------------------------------------------------
    # AUTO COMMAND MATCH â EXECUTE PYTHON FILE
    # ------------------------------------------------------
    def auto_detect_and_execute(self, text):
        if not os.path.exists(self.commands_path):
            self.speak("Commands folder missing sir.")
            return False

        for file in os.listdir(self.commands_path):
            if not file.endswith(".py"):
                continue

            cmd_name = file.replace(".py", "").lower()

            if cmd_name in text:
                script = os.path.join(self.commands_path, file)
                self.speak(f"Executing {cmd_name}, sir...")

                try:
                    subprocess.run(["python3", script])
                except Exception as e:
                    self.speak(f"Error executing {cmd_name}: {e}")

                return True

        return False

    # --------------------------------------------------
    # LLM THINKING (STRICT SHIBU PERSONALITY)
    # --------------------------------------------------
    def chat(self, user_text: str) -> str:
        if not self.llm:
            return "Local brain is not available sir."

        system_prompt = f"""
You are Shibu, an offline Raspberry Pi robot assistant. 

User message: {user_text}
"""



        try:
            result = self.llm(
                system_prompt,
                max_tokens=40,
                temperature=0.8,
            )
            reply = result["choices"][0]["text"].strip()
            return reply if reply else "I don't know sir."
        except Exception:
            return "I could not think sir."

    # --------------------------------------------------
    # MAIN LOOP (COMMANDS FIRST â THEN LLM)
    # --------------------------------------------------
    def run(self):
        while True:
            text = self.listen()
            if not text:
                continue

            if text in ["exit", "quit", "stop","bye","bye bye bye"]:
                self.speak("Goodbye sir, Shibu shutting down sir.")
                break

            # 1ï¸â£ FIRST PRIORITY â COMMAND EXECUTION
            if self.auto_detect_and_execute(text):
                continue

            # 2ï¸â£ IF NO COMMAND MATCH â USE LLM
            response = self.chat(text)
            self.speak(response)


# ============================================================
#                        START SHIBU
# ============================================================
if __name__ == "__main__":
    shibu = ShibuCore()
    shibu.initialize(mic_index=0)
    shibu.run() 

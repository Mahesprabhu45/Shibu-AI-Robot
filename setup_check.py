

import os
import importlib.util
import shutil
import speech_recognition as sr

def check_pass(msg): print(f"[PASS] {msg}")
def check_fail(msg): print(f"[FAIL] {msg}")
def check_info(msg): print(f"[INFO] {msg}")

def check_directory(path):
    if os.path.exists(path):
        check_pass(f"'{path}' directory found.")
        return True
    else:
        check_fail(f"'{path}' directory missing.")
        return False

def check_env_key(key_name="GEMINI_API_KEY"):
    from dotenv import load_dotenv
    load_dotenv()
    key = os.getenv(key_name)
    if key:
        check_pass(f"{key_name} found in .env file.")
        return True
    else:
        check_fail(f"{key_name} missing from .env file.")
        return False

def check_dependency(package_name):
    if importlib.util.find_spec(package_name) is not None:
        check_pass(f"{package_name} is installed.")
        return True
    else:
        check_fail(f"Missing required library: {package_name}")
        return False

def check_microphones():
    try:
        mics = sr.Microphone.list_microphone_names()
        if not mics:
            check_fail("No microphones detected.")
            return False
        else:
            check_pass(f"Microphones detected: {mics}")
            return True
    except Exception as e:
        check_fail(f"Microphone check failed: {e}")
        return False

def check_model_file(model_path="./models/phi-2-q4.gguf"):
    if os.path.exists(model_path):
        check_pass(f"Local model file found: {os.path.basename(model_path)}")
        return True
    else:
        check_fail(f"Model file missing: {model_path}")
        return False

def check_mpg123():
    if shutil.which("mpg123"):
        check_pass("mpg123 audio player found.")
        return True
    else:
        check_fail("mpg123 not found. Install via: sudo apt install mpg123")
        return False


def main():
    print("[INFO] Running Shibu setup checks...\n")

    dirs_ok = check_directory("commands") & check_directory("models")
    env_ok = check_env_key()
    mic_ok = check_microphones()

    check_info("Checking Python dependencies...")
    deps = [
        "speech_recognition",
        "gtts",
        "requests",
        "python_dotenv",
        "pyttsx3"
    ]
    all_deps_ok = all(check_dependency(dep) for dep in deps)

    optional_ok = check_dependency("llama_cpp")
    model_ok = check_model_file()
    mpg_ok = check_mpg123()

    print("\n" + "=" * 55)
    if all([dirs_ok, env_ok, mic_ok, all_deps_ok, model_ok, mpg_ok]):
        print("[PASS] ✅ All setup checks passed. Shibu is ready!")
    else:
        print("[FAIL] ❌ Some essential setup steps are missing or broken.")
    print("[INFO] Setup check completed.")
    print("=" * 55)


if __name__ == "__main__":
    main()

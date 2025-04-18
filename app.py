import speech_recognition as sr
import time

def list_available_microphones():
    """List all available microphones with their indices"""
    print("\nAvailable Microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")

def speech_to_text(microphone_index=None, language="en-US", timeout=4, phrase_time_limit=None):
    """
    Convert speech to text using Google's Speech Recognition API
    
    Args:
        microphone_index (int): Specific microphone to use (optional)
        language (str): Language code for recognition
        timeout (int): Seconds to wait for speech before timing out
        phrase_time_limit (int): Maximum length for speech input
        
    Returns:
        str: Recognized text or None if recognition failed
    """
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True  # Adjust for ambient noise changes
    
    try:
        with sr.Microphone(device_index=microphone_index) as source:
            print("\nAdjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print(f"\nListening for {timeout} seconds... (speak now)")
            start_time = time.time()
            recorded_audio = recognizer.listen(
                source, 
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )
            elapsed = time.time() - start_time
            print(f"Recorded {elapsed:.2f} seconds of audio")
            
            print("Processing speech...")
            text = recognizer.recognize_google(
                recorded_audio,
                language=language
            )
            return text
            
    except sr.WaitTimeoutError:
        print("\nNo speech detected within the timeout period")
    except sr.UnknownValueError:
        print("\nGoogle Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"\nCould not request results from Google Speech Recognition service: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    
    return None

if __name__ == "__main__":
    # List available microphones at startup
    list_available_microphones()
    
    # Get user input for microphone selection
    try:
        mic_index = int(input("\nEnter microphone index (or press Enter for default): ") or None)
    except ValueError:
        mic_index = None
        print("Using default microphone")
    
    # Run speech recognition
    recognized_text = speech_to_text(
        microphone_index=mic_index,
        language="en-US",
        timeout=4,
        phrase_time_limit=10  # Max 10 seconds of speech allowed
    )
    
    if recognized_text:
        print(f"\nRecognized Text: {recognized_text}")
    else:
        print("\nNo text was recognized")

# edit code 
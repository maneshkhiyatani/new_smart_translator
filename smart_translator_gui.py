import gradio as gr
from translate import Translator
import speech_recognition as sr
import pytesseract
import cv2
from PIL import Image

# Language code mapping
lang_codes = {"English": "en", "Urdu": "ur", "Hindi": "hi", "Roman Urdu": "ur"}

def translate_text(input_data, from_language, to_language):
    from_lang_code = lang_codes.get(from_language, "en")
    to_lang_code = lang_codes.get(to_language, "ur")
    try:
        translator = Translator(from_lang=from_lang_code, to_lang=to_lang_code)
        translated_text = translator.translate(input_data)
        return translated_text
    except Exception as e:
        return f"Error: {str(e)}"

def translate_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=5)
        try:
            voice_text = recognizer.recognize_google(audio)
            translated_text = translate_text(voice_text, "English", "ur")
            return translated_text
        except Exception as e:
            return f"Error: {str(e)}"

def capture_and_translate_image():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Camera Feed", frame)
            key = cv2.waitKey(1)
            if key == ord("q"):  # Press 'q' to capture
                cv2.imwrite("captured_image.jpg", frame)
                break
    cap.release()
    cv2.destroyAllWindows()

    # Perform OCR on the captured image
    try:
        image = Image.open("captured_image.jpg")
        text = pytesseract.image_to_string(image)
        translated_text = translate_text(text, "English", "ur")
        return translated_text
    except Exception as e:
        return f"Error: {str(e)}"

def gradio_interface(text_input, voice_input, capture_image):
    if text_input:
        return translate_text(text_input, "English", "ur")
    elif voice_input:
        return translate_voice()
    elif capture_image:
        return capture_and_translate_image()
    else:
        return "No input provided"

iface = gr.Interface(
    fn=gradio_interface,
    inputs=["text", "microphone", "image"],
    outputs="text",
    live=True
)

iface.launch()

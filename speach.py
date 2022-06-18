import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Ouvindo...")
    audio = r.listen(source)

res = r.recognize_google(audio, language="pt-BR")
print("Res ", res)

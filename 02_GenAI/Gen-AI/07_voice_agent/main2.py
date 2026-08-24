import speech_recognition as sr
import asyncio
from openai import APITimeoutError, OpenAI
from dotenv import load_dotenv

from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer


load_dotenv()
client = OpenAI()
async_client = AsyncOpenAI(timeout=60.0, max_retries=2)


async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Always speak in abusive manner with full of tease and derogation",
        input=speech,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)



def main():
    r=sr.Recognizer() # Speech to Text

    with sr.Microphone() as source: # Mic Access
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        SYSTEM_PROMPT = f"""
                            You're an expert voice agent. You are given the transcript of what
                            user has said using voice.
                            You need to output as if you are an voice agent and whatever you speak
                            will be converted back to audio using AI and played back to user.
                        """

        messages = [
                                { "role": "system", "content": SYSTEM_PROMPT },
                                { "role": "user", "content": stt }
                            ]
        

        while True:

            print("Speak Something...")
            audio = r.listen(source)

            print("Processing Audio... (STT)")
            stt = r.recognize_google(audio)

            print("You Said:", stt)
            messages.append({ "role": "user", "content": stt })
            
            
            
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )

            
            ai_response: str = response.choices[0].message.content or ""
            print("AI Response:", ai_response)
            if ai_response:
                try:
                    asyncio.run(tts(speech=ai_response))
                except APITimeoutError:
                    print("TTS request timed out; continuing without audio playback.")
main()

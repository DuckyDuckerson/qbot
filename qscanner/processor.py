import whisper
import os
import time

# Path to saved clips
output_folder = "audio_clips"

# Whisper model
model = whisper.load_model("base")


# Transcribe audio
def transcribe_audio(file_path):
    print("Transcribing audio...")
    result = model.transcribe(file_path)
    return result['text']


# Send to Discord
# async def send_to_discord(transcription, audio_file):
#     client = discord.Client()
#
#     @client.event
#     async def on_ready():
#         print(f'Logged in as {client.user}')
#
#         channel = client.get_channel(int(CHANNEL_ID))
#
#         # Send transcription
#         await channel.send(f"Transcription: {transcription}")
#
#         # Send audio clip
#         with open(audio_file, 'rb') as f:
#             await channel.send("Here is the audio clip:", file=discord.File(f, 'audio_clip.wav'))
#
#         await client.close()
#
#     await client.start(TOKEN)


# Process and send audio files
def process_clips():
    print("Starting processing clips...")
    clip_index = 0
    while True:
        print("Processing clips...")
        # Check if there are new clips
        clip_filename = os.path.join(output_folder, f"clip_{clip_index}.wav")
        if os.path.exists(clip_filename):
            print(f"Processing clip {clip_index}...")

            # Transcribe the clip
            transcription = transcribe_audio(clip_filename)
            print(f"Transcription for clip {clip_index}: {transcription}")

            # Send to Discord
            # This needs to be changed to work within my code
            # asyncio.run(send_to_discord(transcription, clip_filename))
            clip_index += 1
        else:
            time.sleep(1)


# Start processing clips in the background
process_clips()

import subprocess
import os
import time
import whisper

# Initialize Whisper model for transcription
model = whisper.load_model("base")

# Path to save recorded clips
output_folder = "audio_clips"
os.makedirs(output_folder, exist_ok=True)

# Silence detection parameters
SILENCE_THRESHOLD = -50  # dB
SILENCE_DURATION = 1  # seconds


# FFmpeg command to detect silence and record only activity
def record_audio():
    print("Recording started...")

    # Start FFmpeg with silencedetect filter
    ffmpeg_command = [
        'ffmpeg',
        '-f', 'Avfoundation',  # Replace with 'alsa' for Linux
        # audio is a focusrite scarlett 2i4 usb audio interface
        '-i', 'audio="Scarlett 2i4 USB"',  # Use your system's microphone or stream source
        '-af', f'silencedetect=n={SILENCE_THRESHOLD}dB:d={SILENCE_DURATION}',  # Silence detection filter
        '-vn',  # No video (just audio)
        '-acodec', 'pcm_s16le',  # Audio codec (WAV format)
        '-ar', '16000',  # Set sample rate (16 kHz for speech)
        '-ac', '1',  # Mono audio
        'pipe:1'  # Pipe audio output to stdout
    ]

    # Start the FFmpeg process
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Track the current audio data
    audio_data = b''  # Buffer to accumulate audio

    clip_index = 0  # To index saved clips

    silence_detected = False

    print("Entering loop...")

    while True:
        print("Recording...")
        output = process.stderr.readline().decode()  # Read stderr output for silencedetect logs

        # Check if silence was detected and stopped
        if "silence_start" in output:
            silence_start_time = float(output.split("silence_start: ")[1].split()[0])
            print(f"Silence detected, starting time: {silence_start_time}")

            if silence_detected:
                # Save the clip when silence starts and we have data to save
                if len(audio_data) > 0:
                    clip_filename = os.path.join(output_folder, f"clip_{clip_index}.mp3")
                    with open(clip_filename, 'wb') as f:
                        f.write(audio_data)
                    print(f"Clip {clip_index} saved: {clip_filename}")
                    clip_index += 1
                    audio_data = b''  # Reset buffer

            silence_detected = True

        # Check if sound (non-silence) starts
        if "silence_end" in output:
            silence_detected = False
            print("Sound detected, resuming recording...")

        # Read the live audio stream and accumulate in the buffer
        chunk = process.stdout.read(1024)
        if chunk:
            audio_data += chunk
        else:
            time.sleep(0.1)  # Sleep to avoid high CPU usage


# Start recording
record_audio()

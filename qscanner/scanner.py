from ffmpeg import FFmpeg, Progress


def recording():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("path/to/audio/stream")
        .output("output.mp3", vcodec="copy")
    )

    @ffmpeg.on("progress")
    def time_to_terminate(progress: Progress):
        if progress.frame > 200:
            ffmpeg.terminate()

    ffmpeg.execute()


recording()

import moviepy.editor
import os

video_path = 'videos/1. Introduction du cours.mp4'

audio_name = os.path.splitext(os.path.basename(video_path))[0]
video = moviepy.editor.VideoFileClip(video_path)

audio = video.audio

output_path = f"audios/{audio_name}.mp3"
os.makedirs("audios", exist_ok=True)

audio.write_audiofile(output_path)

print(f"Audio extrait : {output_path}")

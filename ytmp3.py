import yt_dlp
import streamlit as st

st.set_page_config(
     page_title="YouTube to MP3 Downloader",  # Title of the page shown in the browser tab
    page_icon="🎵"
)

# Function to convert the video to mp3
def download_audio(url, output_folder='"C:/Users/User/Downloads"'):
    try:
        # Set up options for yt-dlp
        ffmpeg_location = r"C:\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe" 
        ydl_opts = {
            'format': 'bestaudio/best',  # Download best audio format
            'extractaudio': True,  # Only extract audio
            'audioquality': 0,  # Best audio quality
            'outtmpl': f'{output_folder}/%(title)s.%(ext)s',  # Save audio in the desired folder
            'postprocessors': [{  # Convert to MP3 using FFmpeg
                'key': 'FFmpegExtractAudio',  # Correct key for audio conversion
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': ffmpeg_location
        }

        # Download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from: {url}")
            ydl.download([url])
            print(f"Audio downloaded successfully.")
            print("---------------------------------------")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Streamlit UI
st.title("YouTube to MP3 Downloader")
st.write("Enter the YouTube video URL to download the audio as MP3.")

youtube_url = st.text_input("YouTube Video URL")
video_url = youtube_url  # Replace with the actual YouTube URL

if youtube_url:
    if st.button("Download MP3"):
        with st.spinner("Downloading and converting..."):
            try:
                mp3_file = download_audio(video_url)
                st.success(f"Download complete! You can download the MP3 file.")
            except Exception as e:
                st.error(f"Error: {e}")

import yt_dlp
import os
import streamlit as st

# Set the page title and icon
st.set_page_config(
    page_title="YouTube to MP3 Downloader",  # Title of the page shown in the browser tab
    page_icon="🎵"
)

# Function to convert the video to mp3
def download_audio(url, output_folder='downloads'):
    try:
        # Ensure output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Set up options for yt-dlp
        ffmpeg_location = r"/usr/bin/ffmpeg"  # Default location for ffmpeg in a server environment
        
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
            'ffmpeg_location': ffmpeg_location,
            'noplaylist': True  # Avoid downloading entire playlist if URL points to one
        }

        # Download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from: {url}")
            info_dict = ydl.extract_info(url, download=True)  # Get information about the video
            title = info_dict.get('title', None)  # Extract title from info_dict
            audio_file = f"{output_folder}/{title}.mp3"  # Construct the MP3 file name
            
            print(f"Audio downloaded successfully as: {audio_file}")
            return audio_file
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Streamlit UI
st.title("YouTube to MP3 Downloader")
st.write("Enter the YouTube video URL to download the audio as MP3.")

youtube_url = st.text_input("YouTube Video URL")

if youtube_url:
    if st.button("Download MP3"):
        with st.spinner("Downloading and converting..."):
            try:
                mp3_file = download_audio(youtube_url)
                if mp3_file:
                    st.success(f"Download complete! You can download the MP3 file.")
                    # Provide the MP3 file for download
                    with open(mp3_file, "rb") as file:
                        st.download_button("Download MP3", file, file_name=os.path.basename(mp3_file), mime="audio/mp3")
            except Exception as e:
                st.error(f"Error: {e}")

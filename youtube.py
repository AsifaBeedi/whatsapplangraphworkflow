from pytube import YouTube

def get_video_url(query):
    yt = YouTube(f"https://www.youtube.com/results?search_query={query}")
    return yt.streams.filter(progressive=True, file_extension="mp4").first().url
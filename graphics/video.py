from moviepy.editor import VideoFileClip
def play_clip(video_file,x,y):
    video_clip = VideoFileClip(video_file)
    resized_clip = video_clip.resize((x, y))
    resized_clip.preview(fps=resized_clip.fps,fullscreen=True)

if __name__ == "__main__":
    video_file = "/Users/bradygess/Documents/SigEpGunGame.mp4"
    play_clip(video_file,100,100)
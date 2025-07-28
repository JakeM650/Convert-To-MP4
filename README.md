# Convert-to-MP4
_**Why:** I needed to convert .avi to .mp4 to play on my TV._
* Uses ffmpeg to convert video files to .mp4
* Defaults to GPU encoding on NVDA GPU, will fallback to CPU

### Requirements
* Python 3.x.x
* ffmpeg full (https://www.gyan.dev/ffmpeg/builds/)

### Setup & Usage
1. Download ffmpeg full
2. Add the direct path to the `ffmpeg/bin` directory to your system’s `PATH` environment variable
3. Create an `input` and `output` folder in project directory
4. Put video files in the `input` folder
5. Run the script

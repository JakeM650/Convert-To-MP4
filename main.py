import os
import subprocess
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

input_folder = os.path.join(os.getcwd(), "input")
output_folder = os.path.join(os.getcwd(), "output")
os.makedirs(output_folder, exist_ok=True)

supported_extensions = (".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm")

def nvenc_available():
    try:
        result = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"],
                                capture_output=True, text=True)
        return "h264_nvenc" in result.stdout
    except Exception:
        return False

use_gpu = nvenc_available()

if not use_gpu:
    logging.warning("h264_nvenc (GPU encoding) is not available.")
    logging.critical("Do you want to fall back to CPU encoding (libx264)? (y/n): ", end="")
    answer = input().strip().lower()
    if answer != "y":
        logging.info("Aborting conversion.")
        exit()
    else:
        logging.info("Falling back to CPU encoding...\n")

video_files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_extensions)]

if not video_files:
    logging.info("No supported video files found in the input folder.")
    exit()

logging.info(f"Found {len(video_files)} video files to convert.")
logging.info(f"Video files: {video_files}")
check_start = input("Start conversion? (y/n): ").strip().lower()

if check_start != 'y':
    logging.info("Aborting conversion.")
    exit()
    
logging.info("Starting Conversion")

for video_file in video_files:
    input_path = os.path.join(input_folder, video_file)

    cleaned_name = video_file.replace("", "").strip()
    base_name = os.path.splitext(cleaned_name)[0]
    output_filename = f"{base_name}.mp4"
    output_path = os.path.join(output_folder, output_filename)

    # ffmpeg command
    command = [
        "ffmpeg",
        "-i", input_path,
    ]

    if use_gpu:
        # use nvda NVENC GPU encoding
        logging.info("Using GPU encoding")
        command += [
            "-c:v", "h264_nvenc",
            "-preset", "p4",
            "-cq", "19",
        ]
    else:
        # use CPU encoding
        logging.info("Using CPU encoding")
        command += [
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
        ]

    # audio
    command += [
        "-c:a", "aac",
        "-b:a", "192k",
        output_path
    ]

    # run
    try:
        subprocess.run(command, check=True)
        logging.info(f"FINISHED: {video_file} -> {output_filename}\n")
    except subprocess.CalledProcessError as e:
        logging.critical(f"Failed to convert {video_file}: {e}\n")

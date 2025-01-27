import os
import cv2

def create_video_from_frames(temp_dir, output_file, fps=5):
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    frame_files = sorted([os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith(".png")])
    if not frame_files:
        raise ValueError("No se encontraron frames en el directorio temporal.")

    frame_size = cv2.imread(frame_files[0]).shape[1::-1]
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), fps, frame_size)

    for frame_file in frame_files:
        frame = cv2.imread(frame_file)
        out.write(frame)

    out.release()
    print(f"Video generado exitosamente en {output_file}")

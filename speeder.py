import os
import imageio
import shutil
for split in ["cluster", "fg"]:
    videos = os.listdir(f"SAFF/{split}_raw")
    videos = [video for video in videos if video.endswith("mp4")]
    os.makedirs(f"SAFF/{split}", exist_ok=True)
    fps = 10
    for video in videos:
        vid = imageio.get_reader(os.path.join(f"SAFF/{split}_raw", video))
        writer = imageio.get_writer(os.path.join(f"SAFF/{split}", video[:-4]+f"_{split}.mp4"), fps=fps)
        count = 0
        for num, image in enumerate(vid.iter_data()):
            if num % 2==1:
                continue
            writer.append_data(image)
            count += 1
            if count == 10:
                break
        writer.close()
        vid.close()



videos = os.listdir("NSFF/depth_raw")
videos = [video for video in videos if video.endswith("mp4")]
os.makedirs("NSFF/depth", exist_ok=True)
fps = 10
for video in videos:
    vid = imageio.get_reader(os.path.join(f"NSFF/depth_raw", video))
    writer = imageio.get_writer(os.path.join(f"NSFF/depth", video), fps=fps)
    count = 0
    for num, image in enumerate(vid.iter_data()):

        count += 1

    if count < 11:
        shutil.copyfile(os.path.join(f"NSFF/depth_raw", video), os.path.join(f"NSFF/depth", video))
        continue
    print(video, count)
    count = 0
    for num, image in enumerate(vid.iter_data()):
        if num % 2==1:
            continue
        writer.append_data(image)
        count += 1
        if count == 10:
            break
    writer.close()
    vid.close()

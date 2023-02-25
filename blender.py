import os
import imageio
import shutil
import numpy as np
from PIL import Image

for split in ["cluster", "fg"]:
    for method in ["SAFF", "NSFF", "ProposeReduce", "D2NeRF", "DinoBaseline"]:
        if os.path.exists(os.path.join(method, split)):
            print(os.path.join(method, split))
            videos = os.listdir(os.path.join(method, split))
            videos = [video for video in videos if video.endswith("mp4")]
            if os.path.exists(os.path.join(method, split+"_blend")):
                shutil.rmtree(os.path.join(method, split+"_blend"))
            os.makedirs(os.path.join(method, split+"_blend"), exist_ok=True)
            fps = 10
            for video in videos:
                vid = imageio.get_reader(os.path.join(method, split, video))
                try:
                    rid = imageio.get_reader(os.path.join(method, 'rgb', video.replace(split, 'rgb')))
                except:
                    rid = imageio.get_reader(os.path.join("SAFF", 'rgb', video.replace(split, 'rgb')))

                writer = imageio.get_writer(os.path.join(method, split+"_blend", video.replace(".mp4", "_blend.mp4")), fps=fps)
                for num, image in enumerate(vid.iter_data()):

                    #if method == "SAFF":
                    #    real = num * 2
                    #else:
                    #    if num < 3:
                    #        real = num
                    #    else:
                    #        real = 3*num - 6
                    #rgb = imageio.imread(os.path.join("rgb_raw", video.split("_")[0], "%05d.png" % (real)), ignoregamma=True).copy()
                    rgb = rid.get_data(num).copy()
                    if method == "SAFF":
                        rgb = imageio.imread(os.path.join("rgb_raw", video.split("_")[0], "%05d.png" % (2*num)), ignoregamma=True).copy()

                    rgb = np.array(Image.fromarray(rgb).resize((image.shape[1], image.shape[0])))
                    rgb = 0.5*rgb + 0.5*image
                       
                    writer.append_data(rgb)

                        

                writer.close()
                vid.close()


#D2NeRF/fg -> D2NeRF/fg-merged
#NSFF/fg -> NSFF/fg-merged

#SAFF/cluster -> SAFF/cluster-merged
#SAFF/fg -> SAFF/fg-merged
#DinoBaseline/fg -> DinoBaseline/fg-merged
#DinoBaseline/cluster -> DinoBaseline/cluster-merged
#ProposeReduce/fg -> ProposeReduce/fg-merged
#ProposeReduce/cluster -> ProposeReduce/cluster-merged

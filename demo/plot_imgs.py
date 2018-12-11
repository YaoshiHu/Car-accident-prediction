import matplotlib.pyplot as plt
import numpy as np
import os

score_data = np.load("data/prediction.npz")
predict_scores = score_data["data"]
label = score_data["label"]

save_dir = "data/scores"

def save_curve(video_id, num_img):
    save_file_name = os.path.join(save_dir, str(video_id), "000{}.jpg".format(str(num_img))[-8:])
    print(save_file_name)
    score = predict_scores[video_id-1]
    figure = plt.figure(0)
    figure.clear()
    plt.xlim((1, 90))
    plt.ylim((0, 1))

    plt.plot(range(1, num_img+1), score[0:num_img])
    figure.savefig(save_file_name)


if __name__ == "__main__":
    for clip in range(1, 11):
        for img_id in range(0, 90):
            save_curve(clip, img_id)

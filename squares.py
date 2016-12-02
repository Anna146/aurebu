from PIL import Image
from PIL import ImageDraw
import json
import csv

def downscale_image(im, max_dim=2048):
    """Shrink im until its longest dimension is <= max_dim.
    Returns new_image, scale (where scale <= 1).
    """
    a, b = im.size
    if max(a, b) <= max_dim:
        return 1.0, im

    scale = 1.0 * max_dim / max(a, b)
    new_im = im.resize((int(a * scale), int(b * scale)), Image.ANTIALIAS)
    return scale, new_im

def make_squares(path, out_path, json_path):
    orig_im = Image.open(path)
    a,b = orig_im.size
    im = Image.new("RGBA", (a*3,b*3), color = "white")
    draw = ImageDraw.Draw(im)
    js = json.load(open(json_path, 'r'))
    words = js["result"][0]["words"]
    for wrd in words:
        draw.rectangle(((wrd[1],wrd[2]),(wrd[3],wrd[4])), fill = "black", outline = "blue")
    scale, im = downscale_image(im, max_dim=2048)
    im.save(out_path)
    im.show()
    return

if __name__ == '__main__':
    from os import listdir
    print(listdir('/Users/tigunova/PycharmProjects/untitled1/imgs'))
    for fil in listdir('/Users/tigunova/PycharmProjects/untitled1/imgs'):
        path = "imgs/" + fil
        json_path = "jsons/" + fil[:-4] + "-words.json"
        out_path = "imgs_squares/out_"+ fil[:-4] +".png"
        make_squares(path, out_path, json_path)
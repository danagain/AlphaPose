import os 
from PIL import Image

ENSURE_PERSON_ONE = False

class Image_coords:

    def __init__(self, x_left=0, y_top=0, y_bottom=0, x_right=0):
        self.x_left = x_left
        self.y_top = y_top
        self.y_bottom = y_bottom
        self.x_right = x_right

def get_image_points(fname):
    with open(fname) as f:
        content = f.readlines()
        pts = get_useful_txt(content)
    return pts

def get_useful_txt(content):
    global ENSURE_PERSON_ONE
    frame_list = []
    for line in content:
        if("Frame number" in line and not ENSURE_PERSON_ONE):
            ENSURE_PERSON_ONE = True
        elif("person" in line and ENSURE_PERSON_ONE is True):
            ENSURE_PERSON_ONE = False
            modified_line = line.strip().replace(')', '')
            nums = [int(s) for s in modified_line.split() if s.isdigit()]
            y_bottom = nums[3]
            x_right = nums[2] 
            frame_list.append(Image_coords(nums[0], nums[1], y_bottom, x_right))
        elif "Frame number" in line and ENSURE_PERSON_ONE:
            frame_list.append("noimage")

    return frame_list

def crop_image(image_path):
    file_path = os.path.dirname(os.path.realpath(__file__)) + '/testfile.txt'
    pts = get_image_points(file_path)
    original = Image.open(image_path)
    index = image_path.split('/video-tmp/')
    index = index[1].split('.')
    index = index[0].lstrip("0")
    index = int(index) - 1
    print(len(pts))
    if index < len(pts):
        if str(pts[index]) != "noimage":
            width, height = original.size
            cropped_example = original.crop((pts[index].x_left, pts[index].y_top, pts[index].x_left + pts[index].x_right, (pts[index].y_top + pts[index].y_bottom)))
            cropped_example.save(image_path)


def main():
    image_dir = os.path.dirname(os.path.realpath(__file__)) + '/video-tmp'
    for subdir, dirs, files in os.walk(image_dir):
        for file in files:
            filepath = subdir + os.sep + file
            crop_image(filepath)
if __name__ == '__main__':
    main()
"""
Synthetic training examples using squares of different sizes and counts.

max_dim and max_color need to be read from env variables.
"""
import numpy as np
import os

max_dim = int(os.environ.get('MAX_DIM', 30))
max_color = int(os.environ.get('MAX_COLOR', 9))

def generate_images(random_background, number_boxes, box_size, space):
  
    def new_box(size):
        box = np.random.randint(max_dim - size, size=(1,4))
        box[0,2] = box[0,0] + size
        box[0,3] = box[0,1] + size
        return box

    def no_overlap(boxes, box2, space):
    # assume box1 is same size or bigger than box2.  No overlap if no point of box2
    # is inside box1.  Uses space to grow size of box1.
    # Generalize to box1 being an array of boxes.
        for box1 in boxes:
            if   box1[0]-space < box2[0] and box1[2]+space > box2[0] and box1[1]-space < box2[1] and box1[3]+space > box2[1]:
                return False
            elif box1[0]-space < box2[0] and box1[2]+space > box2[0] and box1[1]-space < box2[3] and box1[3]+space > box2[3]:
                return False
            elif box1[0]-space < box2[2] and box1[2]+space > box2[2] and box1[1]-space < box2[1] and box1[3]+space > box2[1]:
                return False
            elif box1[0]-space < box2[2] and box1[2]+space > box2[2] and box1[1]-space < box2[3] and box1[3]+space > box2[3]:
                return False
        return True

    def generate_boxes(number_boxes=4, box_size=8, space=1):
        box_array = new_box(box_size)
        size = box_size//2
        for i in range(number_boxes-1):
            next_box = new_box(size)
            count = 0
            while not no_overlap(box_array, next_box[0], space):
                if count < 5:
                    count += 1
                else:
                    size = size//2
                    if size < 1:
                        size = 1
                    count = 0
                next_box = new_box(size)
            box_array = np.append(box_array, next_box, axis=0)
        return box_array
  
    if random_background:
        background = np.random.randint(max_color)
        color_array = np.random.randint(max_color, size=(1,number_boxes))
        for box in range(number_boxes):
            if color_array[0,box] == background:
                if color_array[0,box] == 0:
                    color_array[0,box] = 1
                else:
                    color_array[0,box] = background - 1
    else:
        background = 0
        color_array = np.random.randint(1, high=max_color+1, size=(1,number_boxes))

    box_array = np.concatenate((generate_boxes(number_boxes, box_size, space), color_array.T), axis=1)

    a = np.ones((max_dim, max_dim))
    a = a * background
    for box in box_array:
        a[box[0]:box[2], box[1]:box[3]] = box[4]
    b = np.zeros((max_dim,max_dim))
    b[box_array[0,0]:box_array[0,2], box_array[0,1]:box_array[0,3]] = 1
    return (a,b)


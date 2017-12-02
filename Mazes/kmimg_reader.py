from PIL import Image
import random
import math
import matplotlib.pyplot as plt
import numpy as np

def classify(points,centroids):
    ans=[]
    for p in points:
        distances = []
        for c in centroids:
            distance = math.sqrt((p[0] - c[0])**2.0+(p[1] - c[1])**2.0+(p[2] - c[2])**2.0)
            distances.append(distance)
        classification = distances.index(min(distances))
        """assign centroid and distance"""
        q = p,classification,min(distances)
        ans.append(q)
    return ans

def k_means(points,centroids,max_iteration):
    new_image_values = []
    for iteration in range(max_iteration):
        print(iteration)
        """ assign each point to a centroid
            each element of the classes array is: [0]original point, [1] centroid_id, [2] distance
        """
        classes = classify(points,centroids)
        new_image_values.clear()
        for new_p in classes:
            n_r = centroids[new_p[1]][0]
            n_b = centroids[new_p[1]][1]
            n_g = centroids[new_p[1]][2]
            np = n_r,n_b,n_g
            new_image_values.append(np)
        #classes should update
        #update centroids:
        for i in range(0,15):
            sum_r = 0
            sum_g = 0
            sum_b = 0
            average_r = 0.0
            average_g = 0.0
            average_b = 0.0
            count = 0
            for point in classes:
                if point[1] == i:
                    sum_r += point[0][0]
                    sum_g += point[0][1]
                    sum_b += point[0][2]
                    count +=1
            new_red = int(sum_r/count)
            new_green = int(sum_g/count)
            new_blue = int(sum_b/count)
            centroids[i] = new_red,new_green,new_blue
    print(new_image_values)
    return new_image_values


def solve(image_rgb):
    iterations = 10
    """should return 16 randomly generated unique samples from image_rgb"""
    initial_centroid_coordinates = random.sample(image_rgb,16)
    return k_means(image_rgb,initial_centroid_coordinates,iterations)


"""opens the image file"""
image = Image.open('kmimg1.png', 'r')
"""in case sh!t happens"""
old_image = image.__copy__()
"""returns the RGB values of each pixel, from x[0]y[0] to x[127]y[127]"""
image_values = list(image.getdata())

ans = solve(image_values)
new_image = Image.new('RGB', (128, 128))
for y in range(0,127):
    for x in range(0,127):
        new_image.putpixel((x,y),ans[128*y + x])

imgs_comb = np.hstack((old_image,new_image))

plt.imshow(imgs_comb)
plt.show()

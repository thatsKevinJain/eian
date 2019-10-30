## Apply ELA,CCL,Union-Find,Graph-Theory ##

#!/usr/bin/env python
# DEPENDENCIES #
from PIL import Image, ImageChops, ImageEnhance, ImageFilter
import sys, os.path
import urllib.request
import random
import math
from collections import OrderedDict

# Test Image Path #
filename = './images/image.jpeg'

# COMPRESSION QUALITY #
quality = 85
threshold = 150

# FILENAMES #
TEMP = './images/temp.jpeg'

# Apply Error Level Analysis #
# @profile
def ELA(imgfile,type):

    ## TYPE 1 (IMAGE) --- TYPE 2 (URL) ##
    # Load Original Image #
    original = None
    if type == 1:
        original = Image.open(imgfile)
    elif type == 2:
        # Download the file #
        urllib.request.urlretrieve(imgfile, filename)
        original = Image.open(filename)

    if original is None:
        return 'Couldnt process your request.'
    
    # Convert to Black and White #
    original = original.convert('L')
    original = ImageEnhance.Sharpness(original).enhance(0.0)
    print('Image: %s' %(filename))

    # Compress at 70% #  
    original.save(TEMP,'JPEG',quality=quality)
    temporary = Image.open(TEMP)

    # Find Difference between original and temporary #
    diff = ImageChops.difference(original, temporary)

    # Find the max value of color band in image #
    extrema = diff.getextrema()
    max_diff = extrema[1]
    print('Extrema: %d' %(max_diff),end=' ')
    scale = 255.0/max_diff

    # Enhance the image based on that scale #
    diff = ImageEnhance.Brightness(diff).enhance(scale)

    # Fetch the histogram of the difference image (Count of color pixels) #
    lists = diff.histogram(mask=None, extrema=None)

    # Calculate Threshold by keeping last 75 pixels #
    pixels = 0
    for i in range(255,1,-1):
        if pixels+lists[i] <= 75:
            pixels += lists[i]
        else:
            threshold = i+1
            print('Threshold: %d' %(threshold),end=' ')
            break

    # Apply Threshold #
    bw = diff.point(lambda x: 0 if x < threshold else 255, '1')
    
    # Calculate Radius #
    WIDTH, HEIGHT = bw.size
    RADIUS = int(math.sqrt((WIDTH*HEIGHT)/(3.14*625.23)))
    print('Radius: %d' %(RADIUS))

    # Maintain a pixel array (Pixel Number : X-Y Co-ordinate) #
    coordinates = []

    # EDGES {(V1->V2) (V2->V3) (V4->V5)}#
    edges = []

    # Scan the entire image and fetch co-ordinates of white pixels #
    bwa = bw.load()
    for x in range(WIDTH):
        for y in range(HEIGHT):

            # Fetch each pixel #
            # color = bw.getpixel((x,y))
            color = bwa[x,y]

            # If pixel is white, record its co-ordinates #
            if color==255:
                coordinates.append([x,y])

    # Loop through XY Co-Ordinates and find Edges #
    for coord in coordinates:

        index = coordinates.index(coord)
        
        x1 = coord[0]
        y1 = coord[1]

        for next_index in range(index+1,len(coordinates)):
            
            x2 = coordinates[next_index][0]
            y2 = coordinates[next_index][1]

            distance = math.sqrt(((x1-x2)**2)+((y1-y2)**2))

            if (distance < (2*RADIUS)):
                edges.append([index,next_index])
    
    # Create a list that has connections for every pixel (V1:V2,V3,...) (V2:V1,V2,...) #
    connectedPixelsList = []

    # No of white pixels #
    total_white_pixels = len(coordinates)
    connectedPixelsList = getConnectedPixels(edges,total_white_pixels)

    # Labels of clusters (Starting value -> 100) #
    labelCount = 100

    # Dictionary (Pixel:Label) #
    label_of_pixels = {}

    # Assign every pixel a label of 0 #
    for index in range(0,len(connectedPixelsList)):
        label_of_pixels.update({connectedPixelsList[index][0]:0})

    # Check neighbor of every pixel and find the root label of every pixel #
    for index in range(0,len(connectedPixelsList)):
        element = connectedPixelsList[index]

        # Arbitrary root number #
        root = 1000

        # Find label with lowest value and assign to root #
        for i in range(1,len(element)):
            pixel = element[i]
            label = label_of_pixels.get(pixel)

            if label > 0 and root > label:
                root = label

        # Union-Find Algorithm #
        
        # If no root found, assign an arbitrary label #
        if root == 1000:
            labelCount += 1
            label_of_pixels.update({element[0]:labelCount})
        else:
            # Update all pixels with root as label #
            for i in range(0,len(element)):
                pixel = element[i]
                label_of_pixels.update({pixel:root})

    # # Count the number of white pixels for each label #
    color_count = {}
    for lp in label_of_pixels.items():
        label = lp[1]
        if label not in color_count:
            color_count.update({label:1})
        else:
            color_count.update({label:color_count.get(label)+1})

    # White Pixels in each Cluster #
    print('White pixels in each cluster: ',end=' ')
    max = 0
    for p in color_count.values():
        if max < p:
            max = p
        print(p,end='  ')
    print()
    print('Max: %d' %(max))

    maxToTotalRatio = (max/total_white_pixels)*100
    if maxToTotalRatio > 80:
        return {'maxToTotalRatio':maxToTotalRatio,'edited':True}
    else:
        return {'maxToTotalRatio':maxToTotalRatio,'edited':False}

# Find connections for each pixel #
def getConnectedPixels(edges,total_white_pixels):
    cpl = []

    for index in range(0,total_white_pixels):

        # Create new element for new pixel #
        cpl.append([index])
        # Index of the last element of list #
        cpl_index = (len(cpl) - 1)

        for i in range(0,len(edges)):

            edge = edges[i]
            start = edge[0]
            end = edge[1]

            # Edges (V1->V2) where {start: V1, end: V2} #
            if start == index:
                cpl[cpl_index].append(end)
                continue
            elif end == index:
                cpl[cpl_index].append(start)
                continue

        # Remove all pixels with no connections #
        if len(cpl[cpl_index]) == 1:
            cpl.remove(cpl[cpl_index])

    return cpl

# if __name__ == '__main__':
#     url = 'https://cdn.vox-cdn.com/thumbor/Pkmq1nm3skO0-j693JTMd7RL0Zk=/0x0:2012x1341/1200x800/filters:focal(0x0:2012x1341)/cdn.vox-cdn.com/uploads/chorus_image/image/47070706/google2.0.0.jpg'
#     ELA(url, 2)



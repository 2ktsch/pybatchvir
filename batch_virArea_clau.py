#!/usr/bin/env python
import os
from gimpfu import *


def python_vareac(img, layer, inFolder, outFolder, bgColor, bgThresh, healthyL, healThrL, healthyD, healThrD, percentlist):
    ''' 2015 KAS, GNU GPL
    Converts images of leaves over a red background to a black and white map of areas affected by virosis.

    Parameters:
    img : image (current image)
    layer : layer (layer that is selected)
    inFolder : string (folder where the images are located)
    outFolder : string (folder to place processed images)
    bgThresh : int8 (threshold value for red background detection)
    thrlvl : int8 (threshold value for final separation)
    percentlist : string (name of file to save the histogram readings in outFolder)
    '''

    # Initialize row in file to save data in...
    afile = open(outFolder + "/" + percentlist + ".csv", 'a')
    afile.write("C\t" + str(bgColor) + "\t" + str(bgThresh) + "\t" + str(healthyL) + "\t" + str(healThrL) + "\t" + str(healthyD) + "\t" + str(healThrD) + "\t")
    
    for file in os.listdir(inFolder):
        try:
            inPath = inFolder + "/" + file
            outPath = outFolder + "/" + file

            image = None
            if file.lower().endswith(('.jpeg', '.jpg')):
                image = pdb.file_jpeg_load(inPath, inPath)

            if image != None:
                if len(image.layers) > 0:
                    layer = image.layers[0]
                    # Select red around leaf
                    pdb.gimp_layer_add_alpha(layer)
                    pdb.gimp_context_set_sample_threshold_int(bgThresh)
                    pdb.gimp_image_select_color(image, 0, layer, bgColor)
                    # Delete red background
                    pdb.gimp_edit_clear(layer)

                    # Select healthy tissue by lighter color
                    pdb.gimp_context_set_sample_threshold_int(healThrL)
                    pdb.gimp_image_select_color(image, 0, layer, healthyL)
                    # Select healthy tissue by darker color
                    pdb.gimp_context_set_sample_threshold_int(healThrD)
                    pdb.gimp_image_select_color(image, 0, layer, healthyD)
                    # Make all of that black
                    pdb.gimp_threshold(layer, 255, 255)
                    # Move to everything else
                    #pdb.gimp_selection_invert(image)
                    pdb.gimp_selection_clear(image)
                    # Threshold everything else to white
                    pdb.gimp_threshold(layer, 1, 255)

                    # Count the pixels
                    mean, stddev, median, pixels, count, percentile = pdb.gimp_histogram(layer, 0, 1, 255)
                    
                    # Write the data to specified file
                    afile.write(file + "\t" + str(percentile) + "\t")

                    # Save to png with transparency
                    pdb.file_png_save(image, layer, outFolder + "/" + image.name[:-4] + "_C.png", outFolder + "/" + image.name[:-4] + "_C.png", 0, 9, 0, 0, 0, 0, 0)
                    # Clean up after ourselves to not run out of memory...
                    pdb.gimp_image_delete(image)

        except Exception as err:
            gimp.message("Unexpected error: " + str(err))


    afile.write("\n")
    afile.close


register(
    "python_fu_batch_virArea_clau",
    "Batch virArea by Claudia's method",
    "Maps virosis of the JPEG images of leaves in a folder using something like Claudia's method.",
    "tonyschindler",
    "GPL v3",
    "2015",
    "<Image>/Script-Fu/virClaudia",
    "*",
    [
        (PF_DIRNAME, "inFolder", "Input directory", ""),
        (PF_DIRNAME, "outFolder", "Output directory", ""),
        (PF_COLOR, "bgColor", "Background color", (255,0,0)),
        (PF_SLIDER, "bgThresh", "Background threshold", 10, (0, 255, 1)),
        (PF_COLOR, "healthyL", "Healthy tissue ligther color", (67,116,68)),
        (PF_SLIDER, "healThrL", "Healthy tissue ligther color threshold", 28, (0, 255, 1)),
        (PF_COLOR, "healthyD", "Healthy tissue darker color", (60,108,51)),
        (PF_SLIDER, "healThrD", "Healthy tissue darker color threshold", 36, (0, 255, 1)),
        (PF_STRING, "percentlist", "Name of file to save data to in output directory", "percentiles")
    ],
    [],
    python_vareac)

main()

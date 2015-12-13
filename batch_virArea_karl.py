#!/usr/bin/env python
'''
 KAS 2015 GPL

This script uses code from:
    [PhotoLab :: Curve Batch
    Copyright Raymond Ostertag 2007-2009
    Licence GPL] to read gimp's curve file format.
'''
import os, glob, string, sys
from gimpfu import *

# ########################## By Raymond Ostertag ##############################
def readcurvefile(curvefilename):
    curvefile = open( curvefilename, 'r' )
    lines = curvefile.readlines()
    if lines[0] == "# GIMP curves tool settings\n":
        for line in lines:
            if line == "(channel value)\n":
                nameCurve = "value"
            if line == "(channel red)\n":
                nameCurve = "red"
            if line == "(channel green)\n":
                nameCurve = "green"
            if line == "(channel blue)\n":
                nameCurve = "blue"
            if line == "(channel alpha)\n":
                nameCurve = "alpha"
            if line != "\n" :
                words = string.split( line )
                if words[0] == "(points":
                    if nameCurve == "value":
                        curve = words[2:]
                    if nameCurve == "red":
                        curvered = words[2:]
                    if nameCurve == "green":
                        curvegreen = words[2:]
                    if nameCurve == "blue":
                        curveblue = words[2:]
                    if nameCurve == "alpha":
                        curvealpha = words[2:]
        return curve, curvered, curvegreen, curveblue, curvealpha # Alpha is ignored
    else:
        pdb.gimp_message( _("This is not a GIMP Curves File") )
        curvefile.close()


def extractpoints( curve ):
    icurve= []
    for curvestr in curve:
        if curvestr[-1] == ")" :
            curvestr = curvestr[:-1]
        curvefloat = float( curvestr )
        curveint = (curvefloat * 255.0) #scale to [0,255]
        icurve.append( int( curveint ))
    ibmax = int( len(icurve) ) - 1
    ib= 0
    ixcurve= []
    while ib <= ibmax:
        if icurve[ ib ] != -255:
        # Suppress all XY points beginning by -255
        # Not sure what I am doing here but you can not introduce directly the gimpcurve in gimp_curves_splines, doesn't work
        # Tested like that and seem's to work correctly
            ixcurve.append( icurve[ ib ] )
            ixcurve.append( icurve[ ib + 1 ] )
        ib = ib + 2
    return ixcurve
# #############################################################################

def vareak(img, layer, inFolder, outFolder, bgColor, bgThresh, curvefilename, thrlvl, percentlist):
    '''
    Converts images of leaves over a red background to a black and white map of areas affected by virosis.
    This script uses Karl's method.

    Parameters:
    img : image (current image)
    layer : layer (layer that is selected)
    inFolder : string (folder where the images are located)
    outFolder : string (folder to place processed images)
    bgThresh : int8 (threshold value for red background detection)
    curvefilename : file (file to use for curve processing of images)
    thrlvl : int8 (threshold value for final separation)
    percentlist : string (name of file to save the histogram readings in outFolder)
    '''
# ########################## By Raymond Ostertag ##############################
    curve, curvered, curvegreen, curveblue, curvealpha = readcurvefile( curvefilename ) # Alpha is ignored
    icurve = extractpoints( curve )
    icurvered = extractpoints( curvered )
    icurvegreen = extractpoints( curvegreen )
    icurveblue = extractpoints( curveblue )
# #############################################################################
    # Start processing files! :D
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
                    pdb.gimp_selection_none(image)

                    # Process with curves (Raymond Ostertag)
                    if len(icurve) >= 4:
                        pdb.gimp_curves_spline(layer, 0, len(icurve), icurve )
                    if len(icurvered) >= 4:
                        pdb.gimp_curves_spline(layer, 1, len(icurvered), icurvered )
                    if len(icurvegreen) >= 4:
                        pdb.gimp_curves_spline(layer, 2, len(icurvegreen), icurvegreen )
                    if len(icurveblue) >= 4:
                        pdb.gimp_curves_spline(layer, 3, len(icurveblue), icurveblue )

                    # Let's turn that into black and white:
                    pdb.gimp_threshold(layer, thrlvl, 255)

                    # Count the pixels
                    mean, stddev, median, pixels, count, percentile = pdb.gimp_histogram(layer, 0, 1, 255)
                    # Write the data to specified file
                    afile = open(outFolder + "/" + percentlist + ".csv", 'a')
                    afile.write(file + ", " + str(percentile) + "\n")
                    afile.close

                    # Save to png with transparency
                    pdb.file_png_save(image, layer, outPath[:-3] + "png", outPath[:-3] + "png", 0, 9, 0, 0, 0, 0, 0)
                    # Clean up after ourselves so the computer doesn't run out of memory...
                    pdb.gimp_image_delete(image)

        except Exception as err:
            gimp.message("Unexpected error: " + str(err))


register(
    "python_fu_batch_virArea_karl",
    "Batch virArea by Karl's method",
    "Maps virosis of the JPEG images of leaves in a folder using Karl's method.",
    "tonyschindler",
    "GPL v3",
    "2015",
    "<Image>/Script-Fu/virKarl",
    "*",
    [
        (PF_DIRNAME, "inFolder", "Input directory", ""),
        (PF_DIRNAME, "outFolder", "Output directory", ""),
        (PF_COLOR, "bgColor", "Background color", (255,0,0)),
        (PF_SLIDER, "bgThresh", "Background threshold", 10, (0, 255, 1)),
        (PF_FILENAME, "curvefilename", "Curve file", ""),
        (PF_SLIDER, "thrlvl", "Threshold", 142, (0, 255, 1)),
        (PF_STRING, "percentlist", "Name of file to save data in output directory", "percentiles"),
    ],
    [],
    vareak)

main()

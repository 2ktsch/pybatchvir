# pybatchvir
GIMP python scripts to batch process images of leaves to aid plant breeders in assessing chlorotic area as a percentage of leaf area.

The purpose of these scripts is to automate the processing of images (samples) in plant breeding or phytopathology programs.
They were created after realizing that doing this stuff by hand is tedious and inefficient for production use.  We (Claudia Gordillo and Karl Schindler) were doing a video (for a plant breeding class) on methods (using image processing in the GIMP) to calculate percentage of virus infected tissue in plants.  We came up with two generalized methods, though there may be better ways.

## Output:
The scripts will put black and white PNG images that should be maps of "infected" area on each leaf.  Filenames will end with "C" for Claudia's method and "K" for Karl's.  The percentiles will be saved to a TAB separated .csv file in the same output folder. Each row corresponds to a run of the script. The first column will be a "C" or "K", followed by the parameters of the script and then (filename, percentile) for each image processed.


## Stuff you still have to do manually for both methods:

### 1. Take adequate images:
It's best if each picture is taken by sandwiching the leaf between a red background (or something that makes good contrast) and a transparent material, such as plastic, glass or plexiglass.  The lighting over the entire surface of the leaf must be even. 
### 2. Make sure all the leaves are of the same species.
Since these scripts work by folder, just keep each set in its own folder. :)
You will be asked for a background color, to be used in selecting and removing the background.  Play with the threshold to your heart's content.

### 3. Open a 'representative' image
To run the script, there must be an image open.  Choose one that is 'representative' of the rest in the batch.


## Claudia's method:
Selects by similar colors given by the user, using keys for a lighter and a darker center of what "healthy" looks like.
You need to provide these colors picking from the image opened to run the script.

## Karl's method:
Using the open image, we must manually create a set of curves that bring out the proper contrast between healthy and infected areas.  Save this curve to a file in the same folder as the images to be processed.  Play around with different settings!

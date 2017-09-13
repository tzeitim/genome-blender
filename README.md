# 3d Genome blender

Scripts to create cartoons of 3D genomes on blender.
![example of coloured TADs](http://i.cubeupload.com/LAXSWV.jpg)
![another example of coloured TADs](http://i.cubeupload.com/LyryNB.jpg)


# requires
- R-base
- RANN R package
- [blender v2.77](https://www.blender.org/features/past-releases/2-77/). Have not tested other versions but it might work unless something really basic had changed.
- Does not require but makes use of the color palettes from [colorbrewer](https://github.com/axismaps/colorbrewer/).
# examples of models generated with this code
https://vimeo.com/genome3d

Based on the concepts developed on ["Capturing pairwise and multi-way chromosomal conformations using chromosomal walks"][cwalks].

[cwalks]: http://www.nature.com/nature/journal/v540/n7632/full/nature20158.html

# How to use
In general one has to create the semi-random walk that will determine the "chromatin". This is done on R given my lack of experience on python. After saving the chromatin path in R one should import it using the python script within blender. A handful of blender files are provided and links to the corresponding videos too.

## Simple example

    source('tads.r')
    # for a rather dense large "TAD"
    gg = generate_tad_random(6000, warp = 200, limit = 0.7, abs_limit = 0.9 * 4)
    # save the path as a text file
    write.table(gg$path, "path_6k_dense_w_200_l_0.7.txt", quote=F, row.names=F, sep="\t");

Once the path is computed it has to be imported into **blender**. The code at this moment has a lot of room for improvement but for the time being one must manually change the path at the bottom of the **chromosomes.py** script and point towards the text file generated in R.

    tad_path6 = importWalk("path_6k_dense_w_200_l_0.7.txt")
    
# Notes
The current scripts by no means represent real information. They are just a cartoon if how I imagine things to work. This of course could be fed with real data (not sure yet what type) and draw something more "real".

Due to attention to other projects this libraries are considered as stand-by.

Please feel free to take over the project or contribute. Just drop a line.


keywords: 3d genome, hic, chromatin, chromosome conformation capture, 3C, chromosomal walks, C-walks.

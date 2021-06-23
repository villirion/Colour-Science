## GSoC 2021 with NumFOCUS 

Hello, I am Cédric DOLLET, a French student in Cergy, near Paris. 
I have been selected for GSoC 2021 and here is a blog that will tell you about my journey.

## Colour

Colour is an open-source python package providing a complete set of algorithms and datasets for color science. So it is a very complete package of different ways to handle colors in scientific and research projects.

# My proposal

You can find the propasal I sent [here](https://drive.google.com/file/d/1mO5zLtGICHV1qgvm7F7Hz8ZniUTRhU7E/view?ths=true)
In summary, I will focus on implementing support for spectral sensitivity functions for digital color cameras and implementing a new color and appearance model.

# Spectral sensitivity functions for digital color cameras
###### 21 june

For Spectral sensitivity functions for digital color cameras, I need to translate the matlab functions of a scientist into python functions. I started by reading the article to understand what these matlab functions do. Once I had a general idea of how they work I started translating them. The matlab syntax is different from the python one but you get used to it quickly. The biggest difficulty is that many matlab functions don't exist in python but fortunately they have almost all a numpy equivalent ([Here is a very useful site](https://numpy.org/doc/stable/user/numpy-for-matlab-users.html)). I've almost finished translating the functions, you can follow my progress [here](https://github.com/villirion/Colour-Science).

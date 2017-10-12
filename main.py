# Image manipulation
#
# You'll need Python 2.7 and must install these packages:
#
#   numpy, PyOpenGL, Pillow

import sys, os, numpy
import math
from collections import Counter
import matplotlib.pyplot as plt

try: # Pillow
  from PIL import Image
except:
  print 'Error: Pillow has not been installed.'
  sys.exit(0)

try: # PyOpenGL
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print 'Error: PyOpenGL has not been installed.'
  sys.exit(0)



# Globals
windowWidth  = 600 # window dimensions
windowHeight =  800

factor = 1 # factor by which luminance is scaled
filter = [1]
apply_filter = False
radius = [0, 0]



# Image directory and pathe to image file

imgDir      = 'images'
imgFilename = 'barbara.png'

imgPath = os.path.join( imgDir, imgFilename )



# File dialog

# import Tkinter, tkFileDialog
#
# root = Tkinter.Tk()
# root.withdraw()

#
# def equalize(freqs, y_vals):
#   L = len(freqs)
#   pn = 0
#   sum_px = 0
#   for key in freqs.iterkeys():
#     sum_px += freqs[key]
#     pn += float(freqs[key]) / float(sum_px)
#     freqs[key] = int(math.floor(L * pn))
#   return freqs


# Read and modify an image.

def buildImage():

  # Read image and convert to YCbCr

  print imgPath
  src = Image.open( imgPath ).convert( 'YCbCr' )
  srcPixels = src.load()

  width  = src.size[0]
  height = src.size[1]

  # Set up a new, blank image of the same size

  dst = Image.new( 'YCbCr', (width,height) )
  dstPixels = dst.load()

  # Build destination image from source image
  #y_vals = []

  if radius != [0, 0]:
    # i = radius[0]
    # j = radius[1]
    # final_y = 0
    # for row in range(len(filter)):
    #   for px in range(len(filter[row])):
    #     # here we multiply the filter by each of the pixel values and add it to the final_y for each location
    #     try:
    #       final_y += filter[row][px] * srcPixels[i + row, j + px][0]
    #     except IndexError:
    #       # this could be fixed by wrapping the image instead of throwing down 0s
    #       final_y += filter[row][px] * 0
    # srcPixels[i, j][0] = int(final_y)

  for i in range(width):
    for j in range(height):

      # read source pixel
      
      y,cb,cr = srcPixels[i,j]
      # print 'srcPixels[i,j]', srcPixels[i,j]
      # try:
      #   print 'srcPixels[i,j+1][0]', srcPixels[i,j+1][0]
      # except IndexError:
      #   print 0

      # ---- MODIFY PIXEL ----
      #y_vals.append(y)
      y = int(factor * y)
      if filter != [1] and apply_filter:
        final_y = 0
        # TODO: the filter begins in the wrong place right now
        for row in range(len(filter)):
          for px in range(len(filter[row])):
            # here we multiply the filter by each of the pixel values and add it to the final_y for each location
            try:
              final_y += filter[row][px] * srcPixels[i+row, j+px][0]
            except IndexError:
              # this could be fixed by wrapping the image instead of throwing down 0s
              final_y += filter[row][px] * 0

        y = int(final_y)

      # write destination pixel (while flipping the image in the vertical direction)
      dstPixels[i, height-j-1] = (y,cb,cr)

  # Done
  #freqs = Counter(y_vals)
  #freqs = equalize(freqs, y_vals)
  #plt.bar(freqs.keys(), freqs.values())
  #plt.show()

  return dst.convert( 'RGB' )



# Set up the display and draw the current image

def display():

  # Clear window

  glClearColor ( 1, 1, 1, 0 )
  glClear( GL_COLOR_BUFFER_BIT )

  # rebuild the image

  img = buildImage()

  width  = img.size[0]
  height = img.size[1]

  # Find where to position lower-left corner of image

  baseX = (windowWidth-width)/2
  baseY = (windowHeight-height)/2

  glWindowPos2i( baseX, baseY )

  # Get pixels and draw

  imageData = numpy.array( list( img.getdata() ), numpy.uint8 )

  glDrawPixels( width, height, GL_RGB, GL_UNSIGNED_BYTE, imageData )

  glutSwapBuffers()

def get_filter():
  filter = []
  filter_type = str(raw_input("Which filter would you like to load? "))
  with open('filters/' + filter_type) as inputfile:
    for line in inputfile:
      filter.append(line.strip().split(','))
  clean_filter = []
  for i in filter[2:]:
    line = i[0].split(" ")
    # godly list comprehension
    clean_filter.append([(int(x)*float(filter[1][0])) for x in line if x.isdigit() or x.startswith('-') and x[1:].isdigit()])
  print 'the filter is: ', clean_filter
  global filter
  # we make the global varaible the flipped so it's ready for convoultion
  filter = clean_filter[::-1]
  
# Handle keyboard input

def keyboard( key, x, y ):

  if key == '\033': # ESC = exit
    sys.exit(0)

  elif key == 'l':
    path = tkFileDialog.askopenfilename( initialdir = imgDir )
    if path:
      loadImage( path )

  elif key == 's':
    outputPath = tkFileDialog.asksaveasfilename( initialdir = '.' )
    if outputPath:
      saveImage( outputPath )
  elif key == 'f':
    get_filter()
  elif key == 'a':
    global apply_filter
    apply_filter = True

  else:
    print 'key =', key    # DO NOT REMOVE THIS LINE.  It will be used during automated marking.

  glutPostRedisplay()



# Load and save images.
#
# Modify these to load to the current image and to save the current image.
#
# DO NOT CHANGE THE NAMES OR ARGUMENT LISTS OF THESE FUNCTIONS, as
# they will be used in automated marking.

def loadImage( path ):

  global imgPath
  imgPath = path

def saveImage( path ):

  buildImage().save( path )

  

# Handle window reshape

def reshape( newWidth, newHeight ):

  global windowWidth, windowHeight

  windowWidth  = newWidth
  windowHeight = newHeight

  glutPostRedisplay()



# Mouse state on initial click

button = None
initX = 0
initY = 0
initFactor = 0



# Handle mouse click/unclick

def mouse( btn, state, x, y ):

  global button, initX, initY, initFactor

  if state == GLUT_DOWN:

    button = btn
    if button == 2 and filter != [1]:
      global radius
      radius = [x,y]
      glutPostRedisplay()

    initX = x
    initY = y
    initFactor = factor

  elif state == GLUT_UP:

    button = None



# Handle mouse motion

def motion( x, y ):

  diffX = x - initX
  diffY = y - initY

  global factor

  factor = initFactor + diffX / float(windowWidth)

  if factor < 0:
    factor = 0

  glutPostRedisplay()
  

    
# Run OpenGL

glutInit()
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
glutInitWindowSize( windowWidth, windowHeight )
glutInitWindowPosition( 50, 50 )

glutCreateWindow( 'imaging' )

glutDisplayFunc( display )
glutKeyboardFunc( keyboard )
glutReshapeFunc( reshape )
glutMouseFunc( mouse )
glutMotionFunc( motion )

glutMainLoop()

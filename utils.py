# dependencies
from PIL import Image
import _imaging
import ImageChops
import numpy as np
import StringIO

#utility to load outfiles created by 'save_images'
def load_images(num_images) : 
  images = []
	for i in range(1,num_images+1) :
		images.append(Image.open("images/outfile-" + str(i) + ".bmp"))
	return images

#utility to save images
def save_images(images) : 
	for i in range(0,len(images)) :
		images[i].save("images/outfile-" + str(i+1) + ".bmp")

# compute the average of the images using PIL's Image.blend
#
# @param images <array> - array of images
# @return average <image>
def average(images) :
	average = images[0].copy()
	for image in images :
		average = Image.blend(average,image,0.5)
	return average

def np_sub_average(np_images, avg) :
	for (x,y), value in np.ndenumerate(np_images) :
		np_images[x][y] = value - avg[x]
	return np_images

def np_add_average(np_images, avg) :
	for (x,y), value in np.ndenumerate(np_images) :
		np_images[x][y] = value + avg[x]
	return np_images

def np_average(np_images) :
	avg = []
	for i in range(np_images.shape[0]) :
		avg.append(np.sum(np_images[i])/np_images.shape[1])
	return avg

def np_covariance_matrix(average) :
	transpose = np.transpose(average)
	fl = (1/float(average.shape[1]-1))
	return np.dot(fl, np.dot(average,transpose))

# computes the mean centered image by subtracting
# the average image from each image in the array
#
# @param average <image> - average image
# @param images <array> - array of images
# @return 
def subtract_average(images,average) :
	height, width = images[0].size
	diff = []
	for image in images :
		diff.append(ImageChops.difference(image, average))
	return diff

# resize and convert images to grayscale
def sanitize(images) :
 	images2 = []
 	for image in images :
 		images2.append(grayscale(image.resize((64, 48), Image.ANTIALIAS)).convert("L"))
 	return to_np_array(images2)

# convert PIL images to Numpy arrays
# essentially the reverse of to_pil_images()
def to_np_array(images) :
	np_images = np.zeros((len(images),images[0].size[0]*images[0].size[1]))
	for i in range(len(images)) :
		np_images[i] = (np.array(list(images[i].getdata())))
	return np_images

# convert numpy arrays to PIL images
# essentially the reverse of to_np_array()
def to_pil_images(np_array) :
	images = []
	for i in range(0,np_array.shape[0]) :
		array_2d = np.vstack((np.split(np_array[i],640)))
		# print array_2d.tofile()
		images.append(Image.fromstring("L",(480,640),array_2d.tostring()))
		# print list(images[i].getdata())
	return images

#convert to grayscale by merging RGB bands
def grayscale(image) :
    r, g, b = image.split()
    image = Image.merge("RGB", (g,g,g))
    return image

# use numpy linear algebra functions to compute the covariance matrix
def covariance_matrix(images) :
	matrix = np.zeros(shape=(len(images),len(images[0].getdata())))
	for i in range(len(images)) :
		matrix[i] = np.array(images[i].getdata())
	transpose = np.transpose(matrix)
	return np.dot(matrix,transpose)

# @return eigenvalues and eigenvectors sorted highest to lowest
# eigenvalues arranged to match with associated eigenvector
def eigen_solve(matrix) :
	solution = np.linalg.eig(matrix)
	eigenValues = solution[0]
	eigenVectors = solution[1]
	sort = eigenValues.argsort()[::-1]   
	eigenValues = eigenValues[sort]
	eigenVectors = eigenVectors[:,sort]
	return eigenValues,eigenVectors

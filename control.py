from utils import *

# enrolls a face in the database
def add_to_db(images) :
  # save the images to the outfiles directory
	save_images(images)

	# all images are converted into grayscale, 
	# reduced to a maneageable size and
	# converted into Numpy arrays
	np_images = sanitize(images)
	
	# re_images = to_pil_images(np_images)
	# re_images[1].show()

	# the average of the images is taken
	mean = np_average(np_images)

	# then the average is subtracted from every image
	# resulting in mean adjusted data
	average = np_sub_average(np_images, mean)

	# the covariance matrix is constructed by
	# a) constructing a matrix out of 'average'
	#	 where the pixels of each image are 
	#	 represented by a column vector
	# b) multiplying the transpose of that matrix by the matrix
	np_matrix = np_covariance_matrix(average)

	# the feature vector is composed by taking the eigenvetors of the eigenvalues (arranged
	# highest to lowest) and placing them in the columns 
	# this is given by 'eigenVectors'
	eigenValues, eigenVectors = eigen_solve(np_matrix)

	# the final data is the rows of the feature vector 
	# times the rows of the mean adjusted data
	finalData = np.transpose(np.dot(eigenVectors,average))

	# reconstruct face from vectors
	a = np.dot(np.transpose(np.linalg.inv(np.transpose(eigenVectors))),np.transpose(finalData))
	eigenFace = np_add_average(a,mean)

	#save eigenFace in the database

	return eigenVectors, eigenFace

	# end 'add_to_db'

#determines whether a face matches any eigenface in the database
def verify_face(image) :
	images = load_images(6)
	eigenVectors, eigenFace = add_to_db(images)

	print "here"
	# print np.array(eigenVectors[0]).shape

	np_image = sanitize(image)
	mean = np_average(np_image)
	average = np_sub_average(np_image,mean)

	# print np.linalg.inv(eigenVectors).shape
	print np.array([eigenVectors[0]]).shape
	print np.transpose(average).shape
	
	omega = np.dot(np.transpose(average),np.array([eigenVectors[0]]))

	result = np.linalg.norm(omega - np.transpose(eigenFace)) 

	print result

	# if the result is a certain amount above or below
	# the threshhold, the face is not recognized

	if result+50 > 17500 and result-50 < 17500 :
		print "Correct Face"
	else :
		print "Incorrect Face"

# end 'verify_face'

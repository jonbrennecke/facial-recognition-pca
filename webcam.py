import cv
from PIL import Image

# callback to display image in window instance
def repeat(capture) :
    frame = cv.QueryFrame(capture)
    cv.ShowImage("Face Capture", frame)

# retrieves n-many webcam images
#
# @param n <int> - number of images to capture
# @return pil_images <array of PIL.Image> - n-many webcam captured images
def handleWebcamCapture(n) :
  cv.NamedWindow("Face Capture", cv.CV_WINDOW_AUTOSIZE)
	camera_index = 0
	capture = cv.CaptureFromCAM(camera_index)
	pil_images = []
	while True:
	    repeat(capture)
	    if (cv.WaitKey(10) == 27) :
	    	print 'ESC pressed. Exiting ...'
	    	cv.DestroyAllWindows()
	    	break
	    if (cv.WaitKey(10) == 13) :
		   	image = cv.QueryFrame(capture)
			pil_images.append(Image.fromstring("RGB",cv.GetSize(image),image.tostring(),'raw','BGR',image.width*3,0))
			print 'Image captured.'
			if len(pil_images) > n - 1 :
				cv.DestroyAllWindows()
				return pil_images
			else : continue

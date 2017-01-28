import sys
import cv2.cv as cv
from optparse import OptionParser

min_size=(20,20)
image_scale=2
haar_scale=1.2
min_neighbors=2
haar_flags=0

def detect_and_draw(img,cascade):
    gray=cv.CreateImage((img.width,img.height),8,1)
    small_img=cv.CreateImage((cv.Round(img.width/image_scale),cv.Round(img.height/image_scale)),8,1)
    cv.CvtColor(img,gray,cv.CV_BGR2GRAY)
    cv.Resize(gray,small_img,cv.CV_INTER_LINEAR)
    cv.EqualizeHist(small_img,small_img)

    if(cascade):
        t=cv.GetTickCount()
        faces=cv.HaarDetectObjects(small_img,cascade,cv.CreateMemStorage(0),haar_scale,min_neighbors,haar_flags,min_size)
        t=cv.GetTickCount()-t
        print "time taken for detection = %gms"%(t/(cv.GetTickFrequency()*1000.))
        if faces:
            for ((x,y,w,h),n) in faces:
                pt1=(int(x*image_scale),int(y*image_scale))
                pt2=(int((x+w)*image_scale),int((y+h)*image_scale))
                cv.Rectangle(img,pt1,pt2,cv.RGB(255,0,0),3,8,0)

        cv.ShowImage("video",img)



cascade=cv.Load("face.xml")
input_name=0
if input_name==0:
    capture=cv.CreateCameraCapture(int(input_name))
else:
    capture=None

cv.NamedWindow("video",1)
width=160*2
height=120*2

if width is None:
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)

if height is None:
    height=int(cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height)

if capture:
    frame_copy=None
    while True:
        frame=cv.QueryFrame(capture)
        if not frame:
            cv.WaitKey(0)
            break
        if not frame_copy:
            frame_copy=cv.CreateImage((frame.width,frame.height),cv.IPL_DEPTH_8U,frame.nChannels)
        if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame,frame_copy)
        else:
            cv.Flip(frame,frame_copy,0)

        detect_and_draw(frame_copy,cascade)
        if cv.WaitKey(10) >= 0:
            break
else:
    image = cv.LoadImage(input_name,1)
    detect_and_draw(image,cascade)
    cv.WaitKey(0)

cv.DestroyWindow("video")

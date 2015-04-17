import numpy as np
import cv2

cap = cv2.VideoCapture(0)
# # Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret==True:
#         frame = cv2.flip(frame,0)

#         # write the flipped frame
#         out.write(frame)

#         cv2.imshow('frame',frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break

# # Release everything if job is finished
# cap.release()
# out.release()
# cv2.destroyAllWindows()


# import cv
# cv.NamedWindow('cap', 1)
# w = cv.CreateVideoWriter('test.avi',cv.CV_FOURCC('X','V','I','D'),25,(640,480))
# cap = cv.CaptureFromCAM(0)
# while(1):
#     img = cv.QueryFrame(cap)
#     cv.ShowImage('cap', img)
#     cv.WriteFrame(w, img)
#     if cv.WaitKey(1) == 27:
#         break
# cv.DestroyWindow('cap')



fps = 15
capSize = (1028,720) # this is the size of my source video
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case
self.vout = cv2.VideoWriter()
success = self.vout.open('output.mov',fourcc,fps,capSize,True) 

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)
        self.vout.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        else:
            break

cap.release()
out.release()



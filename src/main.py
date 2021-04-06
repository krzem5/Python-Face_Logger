from PIL import Image
from cv2.data import haarcascades as H_DIR
import cv2
import pickle
import requests
import sys
import threading
import time



a=sys.argv[1:]
LOG=("--log" in a)
SHOW=("--show" in a)
V_FLIP=("--flip-v" in a)
H_FLIP=("--flip-h" in a)
SAVE=("--save" in a)
DEBUG=("--debug" in a)
MIN_EYES=max((int(a[a.index("--min-eyes")+1]) if "--min-eyes" in a else 2),0)
MAX_EYES=(int(a[a.index("--max-eyes")+1]) if "--max-eyes" in a else 2)
OUT_DIR=(a[a.index("--out-path")+1] if "--out-path" in a else ".")
UPLOAD_DIR=(a[a.index("--upload")+1] if "--upload" in a else None)
H_DIR=(a[a.index("--haarcascades-path")+1] if "--haarcascades-path" in a else H_DIR)



def r(frame):
	if (V_FLIP==True):
		frame=cv2.flip(frame,0)
	if (H_FLIP==True):
		frame=cv2.flip(frame,1)
	gr=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	d=frame.copy()
	o=face.detectMultiScale(gr)
	eo=eye.detectMultiScale(gr)
	no=[]
	for k in o:
		no+=[[tuple(k),0]]
	for e in eo:
		e=tuple(e)
		for f in no:
			k=f[0]
			if (k[0]<=e[0] and k[1]<=e[1] and k[2]>=e[2] and k[3]>=e[3]):
				f[1]+=1
	for k in no:
		for o in no:
			if (k==o):continue
			for p in [list(o[0][:2]),[o[0][0]+o[0][2],o[0][1]+o[0][3]]]:
				if (p[0]>=k[0][0] and p[1]>=k[0][1] and p[0]<=k[0][0]+k[0][2] and p[1]<=k[0][1]+k[0][3]):
					if (abs(k[1]-(MIN_EYES/2+MAX_EYES/2))<abs(o[1]-(MIN_EYES/2+MAX_EYES/2))):
						o[1]=-1
					else:
						k[1]=-1
					break
	for k in no:
		if (MIN_EYES>k[1] or MAX_EYES<k[1]):
			if (DEBUG==True and k[1]!=-1):
				k=k[0]
				cv2.rectangle(d,tuple(k[:2]),(k[0]+k[2],k[1]+k[3]),(0,0,128),3)
			continue
		k=k[0]
		o=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		i=Image.fromarray(o)
		i=i.crop(k[:2]+(k[0]+k[2],k[1]+k[3]))
		if (SAVE==True):
			i.save(f"{OUT_DIR}/{time.time()}.png")
		if (UPLOAD_DIR!=None):
			def f():
				d=pickle.dumps([i.mode,i.size,i.tobytes()])
				requests.post(UPLOAD_DIR,data=d)
			thr=threading.Thread(target=f,args=(),kwargs={})
			thr.start()
		if (LOG==True):
			print("Detected!")
		if (DEBUG==True):
			cv2.rectangle(d,tuple(k[:2]),(k[0]+k[2],k[1]+k[3]),(0,128,0),3)
	if (DEBUG==True):
		for k in eo:
			cv2.rectangle(d,tuple(k[:2]),(k[0]+k[2],k[1]+k[3]),(128,0,128),2)
	return d



c=cv2.VideoCapture(0)
face=cv2.CascadeClassifier()
face.load(H_DIR+"haarcascade_frontalface_default.xml")
eye=cv2.CascadeClassifier()
eye.load(H_DIR+"haarcascade_eye_tree_eyeglasses.xml")



if (LOG==True):
	print("Start")



while True:
	_,frame=c.read()
	frame=r(frame)
	if (SHOW==True):
		cv2.imshow("Cap",frame)
		cv2.waitKey(1)

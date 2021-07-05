"""
create manage and recognize face and face model
:author shaikh jabir mohammed
"""
from cv2 import data,face,imshow,imread,IMREAD_GRAYSCALE,imwrite,waitKey,destroyAllWindows,VideoCapture,cvtColor,COLOR_BGR2GRAY,rectangle,CascadeClassifier,putText,FONT_HERSHEY_PLAIN
from os import mkdir,path,listdir
from numpy import array
from pickle import load,dump

class Recognize:
    def __init__(self):
        for dir in ['cascade','map_database','model','person','style']:
            if not path.exists(dir):
                mkdir(dir)
        cascade=data.haarcascades+'haarcascade_frontalface_default.xml'
        if not path.exists(cascade):
            cascade='cascade/haarcascade_frontalface_default.xml'
        self.cascade = CascadeClassifier(cascade)

    def recognize(self):
        model=face.LBPHFaceRecognizer_create()
        model.read('model/trained_model.yml')
        map=load(open('map_database/mapping_location','rb'))
        camera=VideoCapture(0)
        try:
            while True:
                ret,frame=camera.read()
                if ret:
                    gray=cvtColor(frame,COLOR_BGR2GRAY)
                    for (x,y,w,h) in self.cascade.detectMultiScale(gray,1.2,5):
                        id,conf=model.predict(gray[y:y+h,x:x+w])
                        conf=int(100*(1-conf/300))
                        if conf>75:
                            rectangle(frame,(x,y),(x+w,y+h),[0,255,0],2)
                            putText(frame,map[id],(x+w,y+h+20),FONT_HERSHEY_PLAIN,2,[0,255,0])
                            print(map[id],conf,True)
                        else:
                            rectangle(frame, (x, y), (x + w, y + h), [0,0,255], 2)
                            putText(frame,'Un-known', (x + w, y + h + 20),FONT_HERSHEY_PLAIN,2,[0,0, 255])
                            print(map[id],conf,False)
                imshow("recognizing...", frame)
                if waitKey(1)==27:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            camera.release()
            destroyAllWindows()

    def captureSample(self,name,sample):
        location='person/'+name
        if not path.exists(location):
            mkdir(location)
        camera=VideoCapture(0)
        try:
            count=0
            while True:
                ret,frame=camera.read()
                if ret:
                    gray_image=cvtColor(frame, COLOR_BGR2GRAY)
                    map=self.cascade.detectMultiScale(gray_image,1.2,5)
                    for (x,y,w,h) in map:
                        rectangle(frame, (x, y), (x + w, y + h), [0, 255, 0], 2)
                        if len(map)==1:
                            imwrite(f"{location}/{name }{count}.jpg",gray_image[y:y+h,x:x+w])
                            count+=1
                    imshow("capturing...",frame)
                if waitKey(1)==27 or sample<=count:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            camera.release()
            destroyAllWindows()
            self.createModel()

    def createModel(self):
        print("model training started...")
        model=face.LBPHFaceRecognizer_create()
        images=[]
        labels=[]
        map={}
        for id,groups in enumerate(listdir('person')):
            map.update({id:groups})
            if path.isdir('person/'+groups):
                for img in listdir('person/'+groups):
                    images.append(array(imread(f'person/{groups}/{img}',IMREAD_GRAYSCALE),'uint8'))
                    labels.append(id)
        model.train(images,array(labels))
        model.save('model/trained_model.yml')
        dump(map,open('map_database/mapping_location','wb'))
        print("model training completed...")
#-*- coding: utf-8 -*-
# Programed by Park Nam In
import os
#f_out = open("/Users/naminpark/Desktop/python/python_kmooc/test_out", 'wb')
#word = raw_input("Search key word:")

class GPRMC_parsor:

    ################# binary file read #########################
    data_stream=[]
    flag_count=0;
    _pos=0
    cnt =0
    _time_cnst = ''
    _speed_cnst = ''
    _time_done=0
    _speed_done=0
    TAG_leng=0;
    hword=0;


    def __init__(self,hword,TAG_leng,fileName):

        self.hword = hword
        self.TAG_leng=TAG_leng
        self.word_length=len(self.hword)/2

        self.flag_count=0;
        self._pos=0
        self.cnt =0
        self._time_done=0
        self._speed_done=0
        self.Initialization(fileName)
        self.TIME_RESULT=[]
        self.SPEED_RESULT=[]

    def Initialization(self,fileName):
        self.f = open(fileName,'rb')

    def RUN(self):
        while True:
            self.f.seek(self._pos)
            target_stream=self.f.read(self.word_length)

            #f.tell()
            tword=target_stream.encode("hex")
            if len(tword)/2 != self.word_length:
                break
            if tword == self.hword:
                #print("finding....\n")
                self.flag_count +=1
                self._pos+=self.word_length
                self.f.seek(self._pos)
                #f.tell()
                # GPRMC EXTRACTION
                for i in range(self.TAG_leng):
                    done1 = False
                    time_stamp=[]
                    speed_stamp=[]
                    while not done1:
                        one_word=self.f.read(1)
                        if one_word == ',':
                            done1 =True
                            self._pos +=1
                        else:
                            if i ==1:
                                time_stamp.append(one_word)
                                self._time_done = 1
                            if i ==7:
                                speed_stamp.append(one_word)
                                self._speed_done = 1
                            self._pos +=1

                    #GPRMC정보 저장
                    if self._time_done == 1:
                        for j in range(len(time_stamp)):
                            self._time_cnst += time_stamp[j]
                        _time=float(self._time_cnst)
                        _hour =int(_time)/10000
                        _min  =(int(_time)-_hour*10000)/100
                        _sec  =(int(_time)-_hour*10000-_min*100)
                        timeInfo=str(_hour)+":"+str(_min)+":"+str(_sec)
                        self.TIME_RESULT.append(timeInfo)
                        print (timeInfo)
                        self._time_cnst=''
                        self._time_done =0

                    if self._speed_done == 1:
                        for j in range(len(speed_stamp)):
                            self._speed_cnst += speed_stamp[j]
                            speed=float(self._speed_cnst)*1.852
                        print (speed)
                        self.SPEED_RESULT.append(speed)
                        self._speed_cnst=''
                        self._speed_done =0

                self._pos -=1
            self._pos +=1
            self.cnt +=1

        if self.flag_count == 0:
            print("It is not a GPRMC format")
        else:
            print("complete.....")

        self.f.close()

        return self.TIME_RESULT, self.SPEED_RESULT


if __name__ == "__main__":


    cwd = os.getcwd()

    filename = cwd+"/"+"gprmc_1.mp4"

    hword = "GNRMC".encode("hex")
    TAG_leng = 11

    GPRMC=GPRMC_parsor(hword,TAG_leng,filename)
    time, speed=GPRMC.RUN()


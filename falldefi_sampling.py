import scipy.io
import numpy as np,numpy
import csv
import glob
import os

window_size = 1000
threshold = 60
slide_size = 200 #less than window_size!!!

def dataimport(path1, label):

        xx = np.empty([0,window_size,90],float)
        yy = np.empty([0,1],int)

        ###Input data###
        input_mat_files = glob.glob(path1)
        #data import from csv
        print(label)
        path1 = path1[:len(path1)-5]
        print(path1)
        if (label == 'fall'):
            #input_mat_files = glob.glob(path1)
            input_mat_files = filter(lambda x: (x.startswith(path1+'fa') or x.startswith(path1+'lb') or x.startswith(path1+'lc') or x.startswith(path1+'tr') or x.startswith(path1+'sl') or x.startswith(path1+'fw')), input_mat_files)
            input_mat_files = sorted(input_mat_files)
        else:
            #input_mat_files = glob.glob(path1)
            input_mat_files = filter(lambda x: not (x.startswith(path1+'fa') or x.startswith(path1+'lb') or x.startswith(path1+'lc') or x.startswith(path1+'tr') or x.startswith(path1+'sl') or x.startswith(path1+'fw')), input_mat_files)
            input_mat_files = sorted(input_mat_files)

        print(input_mat_files)
        for f in input_mat_files:
                print("input_file_name=",f)
                data = scipy.io.loadmat(f)
                data = {k:v for k,v in data.items() if k[0] != '_'}
                data = [data[k] for k in data]
                data = np.array(data)
                data = np.squeeze(data, axis = 0)
                tmp1 = data
                x2 =np.empty([0,window_size,90],float)

                #data import by slide window
                k = 0
                while k <= (len(tmp1) + 1 - 2 * window_size):
                        x = np.dstack(np.array(tmp1[k:k+window_size, 0:90]).T)
                        x2 = np.concatenate((x2, x),axis=0)
                        k += slide_size

                xx = np.concatenate((xx,x2),axis=0)
        xx = xx.reshape(len(xx),-1)
    
        # labeling
        if (label == 'fall'):
            yy = np.ones((len(xx),1))
        else:
            yy = np.zeros((len(xx),1))
        print(xx.shape,yy.shape)
        return xx, yy

#### Main ####
if not os.path.exists("input_files/"):
        os.makedirs("input_files/")

"""for k, folder in enumerate(['bathroom', 'bathroom2', 'bedrooms', 'bedrooms2', 'corridor1', 'corridor2_1','corridor2_2','kitchen','kitchen2','lab2']):"""
for k, folder in enumerate(['lab2']):
    if not os.path.exists("input_files/"+str(folder)+'/'):
        os.makedirs("input_files/"+str(folder)+'/')

    for i, label in enumerate (['fall','nonfall']):
        filepath = './merge/'+str(folder)+'/*.mat'
        
        outputfilename1 = './input_files/'+str(folder)+'/xx_'+str(window_size)+'_'+str(threshold)+'_'+str(label)+".csv"
        outputfilename2 = './input_files/'+str(folder)+'/yy_'+str(window_size)+'_'+str(threshold)+'_'+str(label)+".csv"       

        x, y = dataimport(filepath,str(label))
        with open(outputfilename1, "w") as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerows(x)
        with open(outputfilename2, "w") as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerows(y)
        print(label + "finish!")

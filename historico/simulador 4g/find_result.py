#임포트 부
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from operator import itemgetter
import matplotlib.patches as mpatches

# 가장 가까운 BLER 찾기
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]
def find_snr(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

#파일읽고 행렬 선언부
#regression set을 먼저 작동시켜야 동작
makecsv = pd.DataFrame(columns=["kind","alphaseed","betaseed","alpha","beta","loss","MSE"])
for train_i in range(4,5):
    searchs = {"TDL_A"}#,"PedB","VehA","VehB"}
    for search in searchs:
        dlatl = range(11,16)
        for filenum in dlatl:#range(1,16):
            for seed_time in range(50):
                print(search+'/CQI'+str(filenum)+'.csv')
                df=pd.read_csv(search+'/CQI'+str(filenum)+'.csv',usecols = None,skiprows = None,header=None)
                awg=pd.read_csv('AWGN/NEW'+str(filenum)+'.csv',usecols = None,skiprows = None,header=None)
                a = awg.values
                d = df.values
                da = np.float32(d)
                #AWGN 데이터 추출
                aw = np.float32(a)
                #ber 값들 저장
                ber = da[:,[da.shape[1]-1]]
                #맨 마지막 줄 삭제
                dat = np.delete(da,np.s_[-1::], 1)
                #첫번째 줄 삭제, 결국 data 에는 received snr만 남음
                data = np.delete(dat,0, 1)
                #AWGN 가져와서 순서대로 정렬
                vectors_set_awgn = []
                for i in range(0,aw.shape[1]-1):
                    xawgn=aw[[0],[i]]
                    yawgn=aw[[1],[i]]
                    vectors_set_awgn.append([xawgn,yawgn])
                vectors_set_awgn = sorted(vectors_set_awgn,key=itemgetter(1))
                x_awgn = [v[0] for v in vectors_set_awgn]
                y_awgn = [v[1] for v in vectors_set_awgn]
                # find awgn's snr min max
                awgn_snr_max = np.amax(x_awgn)
                awgn_bler_max = np.amax(y_awgn)
                awgn_snr_min = np.amin(x_awgn)
                awgn_bler_min = np.amin(y_awgn)
                ######### this part is add snr ###########
                for i in range(int(awgn_snr_max),100):
                    x_awgn.append([i+1])
                    y_awgn.append([awgn_bler_min-1])
                for i in range(0,int(awgn_snr_min)):
                    x_awgn.append([i])
                    y_awgn.append([-i+awgn_snr_min+awgn_bler_max])
                ##########################################

                # awgn regression
                xawgn = np.squeeze(x_awgn)
                yawgn = np.squeeze(y_awgn)
                #SNR 가져와서 순서대로 정렬
                vectors_set =[]
                for i in range(0,data.shape[0]-1):
                    if ber[i] <= 0.9 and ber[i] >= 0.01:
                        y1=find_nearest(y_awgn,np.log10(ber[i]))
                        x1=data[[i]]
                        goal_SNR = xawgn[find_snr(yawgn,y1)]
                        vectors_set.append([x1,y1,goal_SNR])
                vectors_set = sorted(vectors_set,key=itemgetter(1))
                x_data = [v[0] for v in vectors_set]
                y_data = [v[1] for v in vectors_set]
                goal_data = [v[2] for v in vectors_set]
                K=np.asarray(y_data).shape[0]
                for_sub_x=np.squeeze(np.asarray(x_data))

                #---------텐서플로우 시작----------#
                #변수 선언
                alpha = tf.Variable(initial_value=tf.random_uniform([1], 0.1, 30.0),name='alpha',trainable=True)
                alpha = tf.where(tf.less(alpha, tf.zeros_like(alpha)),tf.zeros_like(alpha)+0.01,alpha)
                beta = tf.Variable(initial_value=tf.random_uniform([1], 0.1, 30.0),name='beta',trainable=True)
                beta = tf.where(tf.less(beta, tf.zeros_like(beta)),tf.zeros_like(beta)+0.01,beta)
                #가공한 자료 가져오기
                BLER_i = tf.constant(np.asarray(y_data),dtype=tf.float32)
                x_data1 = tf.constant(np.squeeze(np.asarray(x_data)),dtype=tf.float32)
                reff = -1*alpha*tf.log(tf.reduce_mean(tf.exp(-1*x_data1/beta),axis=1))
                BLER_reff = tf.constant(np.asarray(goal_data),dtype=tf.float32)
                #에러가 무엇인지 알려주는 부분
                loss = tf.reduce_sum(tf.abs(tf.subtract(BLER_reff,reff)))

                #트레이닝 알고리즘 선택
                if train_i == 0:
                    #그래디언트디센트
                    train = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
                    train_name = "SGD"
                elif train_i == 1:
                    #아담옵티마이저
                    train = tf.train.AdamOptimizer(0.1).minimize(loss)
                    train_name = "Adam"
                elif train_i == 2:
                    #모멘텀옵티마이저
                    train = tf.train.MomentumOptimizer(0.1,0.1).minimize(loss)
                    train_name = "Momentum"
                elif train_i == 3:
                    #Adadelta
                    train = tf.train.AdadeltaOptimizer(0.1).minimize(loss)
                    train_name = "Adadelta"
                elif train_i == 4:
                    #Adagard
                    train = tf.train.AdagradOptimizer(0.1).minimize(loss)
                    train_name = "Adagrad"
                elif train_i == 5:
                    #RMSProp
                    train = tf.train.RMSPropOptimizer(0.01).minimize(loss)
                    train_name = "RMSProp"


                #텐서플로우 실행부분
                init = tf.global_variables_initializer()
                with tf.Session() as sess:
                    sess.run(init)
                    chk = 100000.
                    b = 0.
                    a = 0.
                    seed_alpha=sess.run(alpha)
                    seed_beta=sess.run(beta)

                    for i in range(4000):
                        sess.run(train)
                        if chk > sess.run(loss)/K:
                            chk = sess.run(loss)/K
                            a = sess.run(alpha)
                            b = sess.run(beta)
                            time = i

                    reff = -1*a*np.log(np.mean(np.exp(-1*for_sub_x/b),axis=1))
                    sub_sum = []
                    for i in range(for_sub_x.shape[0]):
                        sub_bler = yawgn[find_snr(xawgn,reff[i])]
                        sub_sum.append([sub_bler])
                    result_loss = np.mean(np.abs(np.subtract(np.asarray(sub_sum),np.asarray(y_data))))
                    makecsv.loc[len(makecsv)] = [search+str(filenum),seed_alpha,seed_beta,a,b,chk,result_loss]
                    print(train_name," alpha seed ",seed_alpha," beta seed ",seed_beta,str(seed_time+1))
                    print("training_time ",time," alpha result ",a," beta result ",b," loss ",chk," MSE ",result_loss)
makecsv.to_csv("SISO AWGN CQI"+str(filenum)+"_"+str(search)+"_"+train_name+".csv")

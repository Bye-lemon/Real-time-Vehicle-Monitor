from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np


def predict(data):
    AmountofData = 40

    Amountoflist = int(AmountofData/4)
    DataTransInterval = 2  # 数据库采样间隔2s
    SamplingInterval = 8  # 数据处理采样间隔8s
    Ts = int(SamplingInterval/DataTransInterval)

    ProData = []  # 重新分组
    Average_speed = []  # 速度平均值
    Sdev_speed = []  # 速度标准差
    Average_la = []
    Sdev_la = []

    for cnt in range(0, AmountofData-1, Ts):
        ProData.append([])
        Average_speed.append([0])
        Sdev_speed.append([0])
        Average_la.append([0])
        Sdev_la.append([0])
    for i in range(0, Amountoflist):
        j = Ts*i
        temp_list_speed = []
        temp_list_la = []
        ProData[i] = data[j:j+Ts]
        for item in ProData[i]:
            temp_list_speed.append(item.speed)
            temp_list_la.append(item.la_x**2+item.la_y**2+item.la_z**2)
        Average_speed[i] = np.mean(temp_list_speed)
        Sdev_speed[i] = np.std(temp_list_speed)
        Average_la[i] = np.mean(temp_list_la)
        Sdev_la[i] = np.std(temp_list_la)

    scaler = StandardScaler()

    DrivingRiskData = [i for i in zip(Average_speed, Sdev_speed)]

    DRD = DrivingRiskData
    DRD_scaled = scaler.fit_transform(DRD)
    X_blobs = DRD_scaled
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X_blobs)
    x_min, x_max = X_blobs[:, 0].min()-0.5, X_blobs[:, 0].max()+0.5
    y_min, y_max = X_blobs[:, 1].min()-0.5, X_blobs[:, 1].max()+0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, .02),
                         np.arange(y_min, y_max, .02))
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    AmountofSmp = len(kmeans.labels_)
    c0 = kmeans.cluster_centers_[0][0] + kmeans.cluster_centers_[0][1]
    c1 = kmeans.cluster_centers_[1][0] + kmeans.cluster_centers_[1][1]
    c2 = kmeans.cluster_centers_[2][0] + kmeans.cluster_centers_[2][1]
    if (c0 > c1):
        if (c0 > c2):
            MAX = 0
            if (c1 > c2):
                MID = 1
                MIN = 2
            else:
                MID = 2
                MIN = 1
        else:
            MAX = 2
            MID = 0
            MIN = 1
    else:
        if (c1 > c2):
            MAX = 1
            if (c0 > c2):
                MIN = 2
                MID = 0
            else:
                MIN = 0
                MID = 2
        else:
            MAX = 2
            MIN = 0
            MID = 1

    AmountofSmp = len(kmeans.labels_)
    cnt0 = 0
    cnt1 = 0
    cnt2 = 0
    for cnts in range(0, AmountofSmp):
        if (kmeans.labels_[cnts] == MIN):
            cnt0 += 1
        elif (kmeans.labels_[cnts] == MID):
            cnt1 += 1
        elif (kmeans.labels_[cnts] == MAX):
            cnt2 += 1
    per0 = cnt0 / AmountofSmp
    per1 = cnt1 / AmountofSmp
    per2 = cnt2 / AmountofSmp

    return per0, per1, per2


if __name__ == "__main__":
    import utils

    data = utils.getData()
    for i in range(20):
        i0, i1, i2 = predict(data)
        print(i0, i1, i2)

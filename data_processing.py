import pandas as pd
import numpy as np

data = pd.read_excel("tracks_21-05-21.xlsx")
print(data)
cropdata = pd.DataFrame(columns=['Scene', 'Vehicle_ID', 'Frame', 'X', 'Y', 'VX', 'VY', 'AX', 'AY'])
for i in range(1, 24):
    # load the data for each scene
    scene = data[data.Scene == i]
    l = scene.Vehicle_ID.unique()
    
    # find the two closest vehicles
    vehX = []
    for j in l:
        vehX.append(scene[scene.Vehicle_ID == j].X.mean())
    d = dict(zip(l, vehX))
    pos_d = {key: value for key, value in d.items() if value >= 0}
    lowest_value = sorted(pos_d.values())[0]
    keys_lowest_values = [key for key, value in pos_d.items() if value == lowest_value]
    scene1veh = scene[scene.Vehicle_ID == keys_lowest_values[0]]
    
    # calculate speed in x and y
    VX = [np.nan]
    VY = [np.nan]
    AX = [np.nan, np.nan]
    AY = [np.nan, np.nan]
    for i in range(1, len(scene1veh)):
        x1 = scene1veh.iloc[i-1, 3]
        x2 = scene1veh.iloc[i, 3]
        y1 = scene1veh.iloc[i-1, 4]
        y2 = scene1veh.iloc[i, 4]
        VX.append(np.sqrt(x1**2 + x2**2))
        VY.append(np.sqrt(y1**2 + y2**2))
    scene1veh.insert(5, 'VX', VX, True)
    scene1veh.insert(6, 'VY', VY, True)
   
    # calculate acceleration
    for i in range(2, len(scene1veh)):
        vx1 = scene1veh.iloc[i-1, 5]
        vx2 = scene1veh.iloc[i, 5]
        vy1 = scene1veh.iloc[i-1, 6]
        vy2 = scene1veh.iloc[i, 6]
        AX.append(np.sqrt(vx1**2 + vx2**2))
        AY.append(np.sqrt(vy1**2 + vy2**2))
    scene1veh.insert(7, 'AX', AX, True)
    scene1veh.insert(8, 'AY', AY, True)

    cropdata = pd.concat([cropdata, scene1veh], ignore_index=True)

print(cropdata)

# SSMs
MADR = 8  # m^2/S
TTC = []
PSD = []
DRAC = []
for i in range(len(cropdata)):
    if np.sum(cropdata.iloc[i, :].isna()) == 0 and cropdata.iloc[i, :].any() != 0:
        D = np.sqrt(cropdata.iloc[i, 3]**2 + cropdata.iloc[i, 4]**2)
        V = np.sqrt(cropdata.iloc[i, 5]**2 + cropdata.iloc[i, 6]**2)
        A = np.sqrt(cropdata.iloc[i, 7]**2 + cropdata.iloc[i, 8]**2)
        TTC.append(D/V)
        PSD.append(D/((V**2)/(2*MADR)))
        DRAC.append(V**2/(2*D))
    else:
        TTC.append(np.nan)
        PSD.append(np.nan)
        DRAC.append(np.nan)
cropdata.insert(9, 'TTC', TTC, True)
cropdata.insert(10, 'PSD', PSD, True)
cropdata.insert(11, 'DRAC', DRAC, True)
print(cropdata)


# for i in VehID:
#     d = data[data.iloc[:, 1] == i]
#     data[data.iloc[:, 1] == i] = d['X'].rolling(5).mean()
#     data[data.iloc[:, 1] == i] = d['Y'].rolling(5).mean()
# print('pro data', d)


import numpy as np
import matplotlib.pyplot as plt
import gpxpy.parser as ps
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as poly
from mpl_toolkits import mplot3d

#parse --> get data

gpx_file = open('track.gpx', 'r')
gpx_parser = ps.GPXParser(gpx_file)
gpx = gpx_parser.parse()
gpx_file.close()

data_list = []

for track in gpx.tracks:
	for segment in track.segments:
		for point in segment.points:
			data_res = []
			data_res.append(float(point.latitude))
			data_res.append(float(point.longitude))
			data_res.append(float(point.elevation))
			
			for extension in point.extensions:
				data_res.append(float(extension.text))
			if len(data_res) != 4:
				continue
			data_list.append(data_res)	
data = np.array(data_list)	

#setting
fig = plt.figure(figsize=(20,5))
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

#ax1
select_up = []
select_down = []
for i in range(len(data[:,2])-1):
	if data[i+1,2] > data[i,2]:
		select_up.append(i+1)
	else :
		select_down.append(i+1)

#start_end point
ax1.scatter3D(data[-1,0], data[-1,1], data[-1,2], s=60, color='black', marker="P", label='start_end point')

#route& upward or downward 
ax1.scatter3D(data[select_up,0], data[select_up,1], data[select_up,2], s=0.1, color='red', label='upward')
ax1.scatter3D(data[select_down,0], data[select_down,1], data[select_down,2], s=0.1, color='darkgreen', label='downward')
ax1.set_xlabel("lat",size=12, color='indigo', rotation=-20, labelpad=5) 
ax1.set_ylabel("lon",size=12, color='indigo', rotation=50, labelpad=10)
ax1.set_zlabel("ele",size=12, color='indigo', rotation=-5)  
ax1.set_zlim((200, 900))

#highest&lowest point
sort_elevation=sorted(data[:,2])
lowest=sort_elevation[0]
highest=sort_elevation[-1]
low=np.where(data[:,2]==lowest)
high=np.where(data[:,2]==highest)
int_low=int(low[0])
int_high=int(high[0])
ax1.scatter3D(data[int_low,0],data[int_low,1],data[int_low,2],s=60,color='blue',marker="v",label="lowest point:"+str(data[int_low,2]))
ax1.scatter3D(data[int_high,0],data[int_high,1],data[int_high,2],s=60,color='red',marker="^",label='highest point:'+str(data[int_high,2]))

#caption
ax1.legend(numpoints=1, loc='upper left')

#draw the poly
height=min(data[:,2])
v = []
for k in range(0, len(data[:,1]) - 1):
    x = [data[k,0], data[k+1,0], data[k+1,0], data[k,0]]
    y = [data[k,1], data[k+1,1], data[k+1,1], data[k,1]]
    z = [data[k,2], data[k+1,2], height,height]
    v.append(list(zip(x, y, z)))

poly1=poly(v, alpha=0.3, facecolors='cyan')
ax1.add_collection3d(poly1)

#ax2
select_ac = []
select_dc = []
for i in range(len(data[:,3])-1):
	if data[i+1,3] > data[i,3]:
		select_ac.append(i+1)
	else :
		select_dc.append(i+1)

#show the acceleration(positive or negative)
cb1 = ax2.scatter3D(data[select_ac,0], data[select_ac,1], data[select_ac,2], s=1, c=data[select_ac,3], cmap='winter_r')
cb2 = ax2.scatter3D(data[select_dc,0], data[select_dc,1], data[select_dc,2], s=1, c=data[select_dc,3], cmap='Wistia')
cbar1 = plt.colorbar(cb1, pad=0, aspect=80)
cbar2 = plt.colorbar(cb2, pad=0.1, aspect=80)
cbar1.set_label("speed\nac", size=12, color='indigo', rotation=0, labelpad=-25, y=1.085)
cbar2.set_label("speed\ndc", size=12, color='indigo', rotation=0, labelpad=-25, y=1.085)
ax2.set_xlabel("lat",size=12, color='indigo', rotation=-20, labelpad=5) 
ax2.set_ylabel("lon",size=12, color='indigo', rotation=50, labelpad=10)
ax2.set_zlabel("ele",size=12, color='indigo', rotation=-5) 
ax2.set_zlim((200, 900))

#fastest and slowest
sort_speed=sorted(data[:,3])
slowest=sort_speed[0]
fastest=sort_speed[-1]
slow=np.where(data[:,3]==slowest)
fast=np.where(data[:,3]==fastest)
int_slow=int(slow[0])
int_fast=int(fast[0])
ax2.scatter3D(data[int_slow,0],data[int_slow,1],data[int_slow,2],s=100,color='darkblue',marker="v",label="slowest point:"+str(data[int_slow,3]))
ax2.scatter3D(data[int_fast,0],data[int_fast,1],data[int_fast,2],s=100,color='red',marker="^",label='fastest point:'+str(data[int_fast,3]))

ax2.legend(numpoints=1, loc="upper center")

#title
start_t = str(gpx.tracks[0].segments[0].points[0].time)
end_t = str(gpx.tracks[0].segments[0].points[-1].time)
fig.suptitle(gpx.name+"\nIn Spanish")
fig.suptitle(gpx.name+"\n(location:Spanish)"+"\nstart_time:"+start_t+"\nend_time:"+end_t)

#show
plt.show()
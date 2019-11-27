import numpy as np
import matplotlib.pyplot as plt
import gpxpy.parser as ps
from mpl_toolkits import mplot3d

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


fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2, projection='3d')



select_up = []
select_down = []
for i in range(len(data[:,2])-1):
	if data[i+1,2] > data[i,2]:
		select_up.append(i+1)
	else :
		select_down.append(i+1)

ax1.scatter3D(data[-1,0], data[-1,1], data[-1,2], s=3, color='cyan')
ax1.text(data[0,0]-0.01,data[0,1],data[0,2]-150, 'start point', color='green')

ax1.scatter3D(data[select_up,0], data[select_up,1], data[select_up,2], s=0.1, color='red')
ax1.scatter3D(data[select_down,0], data[select_down,1], data[select_down,2], s=0.1, color='darkgreen')
ax1.set_xlabel("lat",size=12, color='indigo', rotation=-10) 
ax1.set_ylabel("lon",size=12, color='indigo', rotation=50)
ax1.set_zlabel("ele",size=12, color='indigo')  
ax1.set_zlim((200, 700))

cb = ax2.scatter3D(data[:,0], data[:,1], data[:,2], s=3, c=data[:,3], cmap='Reds')
cbar = plt.colorbar(cb)
cbar.set_label("speed", size=12, color='indigo', rotation=10)
ax2.set_zlim((200, 700))

plt.title(gpx.name)
plt.show()
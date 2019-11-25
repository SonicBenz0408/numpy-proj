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


figure = plt.figure()
ax = plt.axes(projection='3d')

cb = ax.scatter3D(data[:,0], data[:,1], data[:,2], s=3, c=0.01*data[:,3], cmap='Reds')
ax.scatter3D(data[0,0], data[0,1], data[0,2], s=30, color='green')
ax.plot3D(data[:,0], data[:,1], data[:,2], c='blue')
ax.text(data[0,0]-0.01,data[0,1],data[0,2]-150, 'start point', color='green')
plt.colorbar(cb)
plt.title(gpx.name)
ax.set_xlabel("lat",size=12, color='indigo') 
ax.set_ylabel("lon",size=12, color='indigo')
ax.set_zlabel("ele",size=12, color='indigo')  


plt.show()
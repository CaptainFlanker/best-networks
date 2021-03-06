# -- coding: utf-8 --
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import math
import copy
from matplotlib.patches import Circle, PathPatch
# register Axes3D class with matplotlib by importing Axes3D
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
def findXX(s,i):
	m=0
	for n in range(i+1):
		m=s%2
		s=s/2
	return m

def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, **kwargs):
    '''
    Plots the string 's' on the axes 'ax', with position 'xyz', size 'size',
    and rotation angle 'angle'.  'zdir' gives the axis which is to be treated
    as the third dimension.  usetex is a boolean indicating whether the string
    should be interpreted as latex or not.  Any additional keyword arguments
    are passed on to transform_path.

    Note: zdir affects the interpretation of xyz.
    '''
    x, y, z = xyz
    if zdir == "y":
        xy1, z1 = (x, z), y
    elif zdir == "y":
        xy1, z1 = (y, z), x
    else:
        xy1, z1 = (x, y), z

    text_path = TextPath((0, 0), s, size=size, usetex=usetex)
    trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])

    p1 = PathPatch(trans.transform_path(text_path), **kwargs)
    ax.add_patch(p1)
    art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)	

def exchange_hang(l,m,n,h1,h2): #默认采用0表示第一行
	if h1>=m or h2>=m:
		print "hang wrong!!"
	new_l=copy.copy(l)		
	for j in range(n):
		new_l[m*h2+j]=l[m*h1+j]
		new_l[m*h1+j]=l[m*h2+j]
	return new_l
def exchange_lie(l,m,n,l1,l2): #默认采用0表示第一列
	if l1>=n or l2>=n:
		print "lie wrong!!"
	new_l=copy.copy(l)	
	
	for i in range(m):
		
		new_l[m*i+l1]=l[m*i+l2]
		new_l[m*i+l2]=l[m*i+l1]
	return new_l

def ex_line(l,num_x,num_y,location_j,goal_j): #矩阵的零层对应神经网络的第一层，神经网的初始层为0,i表示第几层神经网络
	l_new=copy.copy(l)
	for layer in range(num_x-1):
		i=layer+1
		p1=l[(i-1)*num_y*num_y:i*num_y*num_y]
		new_p1=exchange_hang(p1,num_y,num_y,location_j,goal_j)
		new_p2=exchange_lie(new_p1,num_y,num_y,location_j,goal_j)
		l_new[(i-1)*num_y*num_y:i*num_y*num_y]=new_p2		
	return l_new

def find_num(l):
	num=0
	for i in range(len(l)):
		num=num+l[i]*pow(2,i)
	return num





num_x=3 #表示层数
num_y=3 #表示每层的神经元数
ss=np.loadtxt("left.txt")
s=ss.astype(int)
open_turn=2
l=[] #113982, 126201
for i in range(num_y*num_y*(num_x-1)): #相当于一层需要用几位二进制作数表示，需要总层数减一的规模
	l.append(0)

#for n in range(pow(2,num_y*num_y*(num_x-1))-1001,pow(2,num_y*num_y*(num_x-1))-1002):
for n in range (len(s)):
	
	
	for i in range(1,num_x): #计算本解各个位上的值
			for k in range(0,num_y):
				for j in range (0,num_y):
					l[(i-1)*num_y*num_y+j*num_y+k]=findXX(s[n],(i-1)*num_y*num_y+j*num_y+k)
	p=copy.copy(l)
	fig = plt.figure(figsize=(10,10))
	ax = fig.gca(projection='3d')
	
	
	# 画矩阵括号
	x0=0.2
	y0=1
	z0=-0.2
	zHigh=2.35
	xWidth=2.65
	yLong=1
	dL=0.1#短线的宽度
	
	# 第一层左|	
	x = np.linspace(x0, x0, 100)
	y = np.linspace(y0, y0, 100)
	z = np.linspace(z0,z0+zHigh, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第一层右|
	x = np.linspace(x0+xWidth, x0+xWidth, 100)
	y = np.linspace(y0, y0, 100)
	z = np.linspace(z0, z0+zHigh, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第二层左|
	x = np.linspace(x0, x0, 100)
	y = np.linspace(y0+yLong, y0+yLong, 100)
	z = np.linspace(z0, z0+zHigh, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第二层右|
	x = np.linspace(x0+xWidth, x0+xWidth, 100)
	y = np.linspace(y0+yLong, y0+yLong, 100)
	z = np.linspace(z0, z0+zHigh, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第一层左上-
	x = np.linspace(x0, x0+dL, 100)
	y = np.linspace(y0, y0, 100)
	z = np.linspace(z0+zHigh, z0+zHigh, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第二层左上-
	x = np.linspace(x0, x0+dL, 100)
	y = np.linspace(y0+yLong, y0+yLong, 100)
	z = np.linspace(z0+zHigh, z0+zHigh, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第一层右上-
	x = np.linspace(x0+xWidth-dL, x0+xWidth, 100)
	y = np.linspace(y0, y0, 100)
	z = np.linspace(z0+zHigh, z0+zHigh, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第二层右上-
	x = np.linspace(x0+xWidth-dL, x0+xWidth, 100)
	y = np.linspace(y0+yLong, y0+yLong, 100)
	z = np.linspace(z0+zHigh, z0+zHigh, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第一层左下-
	x = np.linspace(x0, x0+dL, 100)
	y = np.linspace(y0, y0, 100)
	z = np.linspace(z0, z0, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第二层左下-
	x = np.linspace(x0, x0+dL, 100)
	y = np.linspace(y0+yLong, y0+yLong, 100)
	z = np.linspace(z0, z0, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第一层右下-
	x = np.linspace(x0+xWidth-dL, x0+xWidth, 100)
	y = np.linspace(y0, y0, 100)
	z = np.linspace(z0, z0, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
	# 第二层右下-
	x = np.linspace(x0+xWidth-dL, x0+xWidth, 100)
	y = np.linspace(y0+yLong, y0+yLong, 100)
	z = np.linspace(z0, z0, 100)
	ax.plot(x, y, z, color='black',label='parametric curve')
			
	
				
			
	
	
	#3D scatter,画神经元
	x = []
	y = []
	z = []
	for i in range(num_x):
		for j in range(num_y):
			x.append(0)
			y.append(i) 
			z.append(j)			
	ax.scatter(x, y, z, s=300,c="r")
			
	#画矩阵的项数
	# Plot a sin curve using the x and y axes.
	for c in range(num_y*num_y*(num_x-1)):#表示位置数	
				
		i=c/(num_y*num_y)+1
		j=num_y-1-c%(num_y*num_y)/num_y
		k=num_y-1-c%(num_y*num_y)%num_y
				
		colar=["y",'b','r','g'] #定义字体颜色数组
		
		
		
		if open_turn==1:
			
			colar_line=['blue','green','red','darkmagenta']
		
		if open_turn==0:
			
			colar_line=['red','green','blue','darkmagenta']
		
		if open_turn==2:
			
			colar_line=['red','blue','green','darkmagenta']
			
			
				
		
		colar_first_Layer="y" #定义前层字体颜色
		colar_second_Layer="b" #定义后层字体颜色	
		
			
		if p[c]==1: #判断是否有连接
					
			y = np.linspace(i, i-1, 3)
			z = np.linspace(j, k, 3)
			#ax.plot(x, y, zs=0, zdir='z')
			#ax.plot(x, z, zs=0, zdir='y' )
			#画线 
			ax.plot(y, z, zs=0, color=colar_line[k%4], zdir='x') #如果有连接就画线，zdir='x'表示在垂直于x轴的面上
					
			if i==1: #判断是否是前层
				text3d(ax, (2.1+x0-k, i, j+z0+0.1), "1", zdir="y", size=.4, usetex=False,
       angle=0, ec="none", fc=colar_first_Layer) #画前层主字
				#text3d(ax, (2.35+x0-k, i, j+z0+0.27), "i", zdir="y", size=.15, usetex=False,
       #angle=0, ec="none", fc=colar_first_Layer) #画前层主字的上标
				text3d(ax, (2.35+x0-k, i, j+z0+0.1), str(3-j)+","+str(3-k), zdir="y", size=.15, usetex=False,
       angle=0, ec="none", fc=colar_first_Layer) #画前层主字的下标
		
			else:
				text3d(ax, (2.1+x0-k, i, j+z0+0.1), "1", zdir="y", size=.4, usetex=False,
       angle=0, ec="none", fc=colar_second_Layer)
				#text3d(ax, (2.35+x0-k, i, j+z0+0.27), "i+1", zdir="y", size=.15, usetex=False,
      # angle=0, ec="none", fc=colar_second_Layer)
				text3d(ax, (2.35+x0-k, i, j+z0+0.1), str(3-j)+","+str(3-k), zdir="y", size=.15, usetex=False,
       angle=0, ec="none", fc=colar_second_Layer)
       
		else: #如果没有连接
			
			if i==1: #判断是否是前层
				text3d(ax, (2.1+x0-k, i, j+z0+0.1), "0", zdir="y", size=.4, usetex=False,
       angle=0, ec="none", fc=colar_first_Layer) #画前层主字
				#text3d(ax, (2.35+x0-k, i, j+z0+0.27), "i", zdir="y", size=.15, usetex=False,
       #angle=0, ec="none", fc=colar_first_Layer) #画前层主字的上标
				text3d(ax, (2.35+x0-k, i, j+z0+0.1), str(3-j)+","+str(3-k), zdir="y", size=.15, usetex=False,
       angle=0, ec="none", fc=colar_first_Layer) #画前层主字的下标
			else:
				text3d(ax, (2.1+x0-k, i, j+z0+0.1), "0", zdir="y", size=.4, usetex=False,
       angle=0, ec="none", fc=colar_second_Layer) #画后层主字
				#text3d(ax, (2.35+x0-k, i, j+z0+0.27), "i+1", zdir="y", size=.15, usetex=False,
       #angle=0, ec="none", fc=colar_second_Layer) #画后层主字的上标
				text3d(ax, (2.35+x0-k, i, j+z0+0.1), str(3-j)+","+str(3-k), zdir="y", size=.15, usetex=False,
       angle=0, ec="none", fc=colar_second_Layer) #画后层主字的下标
	# Make legend, set axes limits and labels
	#ax.legend()
	ax.set_xlim(0, num_y)
	ax.set_xlim(left=None, right=None, emit=True, auto=False)
	ax.set_ylim(0, num_x-1)
	ax.set_zlim(0, num_y-1)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')

	# Customize the view angle so it's easier to see that the scatter points lie
	# on the plane y=0
	ax.view_init(elev=20., azim=-35)
	plt.savefig("ch_stru25"+str(n))
	plt.close()		


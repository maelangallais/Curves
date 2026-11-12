#Créé le 26 Août 2024
from math import pi,sin,cos,fabs as va,floor
from kandinsky import fill_rect as fr
from ion import keydown as kd
from time import sleep as sl

bk,wh=(0,)*3,(255,)*3
re,gr,bl=(255,0,0),(0,255,0),(0,0,255)

value=[ #tous nos points
  (270,110),(310,10),(180,20),
  (160,60),(140,20),(10,10),
  (50,110),(60,150),(130,160),
  (160,200),(190,160),(260,150)
]
links=[[0,1,2,3],[3,4,5,6],[6,7,8,9],[9,10,11,0]] #Quels points sont reliés entre eux
ct=[(11,0,1,1),(5,6,7,1)] #Continuity: 1=G1; 2=C1
step=30 #nombre d'étapes pour dessiner la courbe

fp=[v[0]for v in links] #First Points (Anchor Points)
wv=0 #which value
dm=3 #valeur du déplacement de la séléction
width,height=320,222
cr=3 #taille du cercle

inf=lambda x1,x2:x1<x2
sup=lambda x1,x2:x1>x2
ent=lambda n:floor(n)if n-floor(n)<0.5 else floor(n)+1
dst=lambda x1,y1,x2,y2:((x1-x2)**2+(y1-y2)**2)**.5

def draw_point(cx,cy,cl):
 for rep in range(8*cr*pi):
  adj=cos(rep)*cr
  x=cx+adj
  opp=sin(rep)*cr
  y=cy+opp
  fr(ent(x),ent(y),1,-2*ent(opp),cl)

def draw_points():
 for i in range(len(value)):
  cl=bl if i==wv else gr if i in fp else re
  draw_point(value[i][0],value[i][1],cl)

def dl(x1,y1,x2,y2,t=1,cl=bk): #draw_line
 w=h=1
 dx=min(max((x2-x1)/va(y2-y1)if va(y2-y1)!=0 else x2-x1,-1),1)
 dy=min(max((y2-y1)/va(x2-x1)if va(x2-x1)!=0 else y2-y1,-1),1)
 c=va(x2-x1)if va(x2-x1)>va(y2-y1)else va(y2-y1)
 if va(dx)<va(dy):w,x1,x2=t,x1-(t-1)//2,x2-(t-1)//2
 else:h,y1,y2=t,y1-(t-1)//2,y2-(t-1)//2
 for i in range(c):fr(ent(x1+dx*i),ent(y1+dy*i),w,h,cl)

def lerp(a,b,t): #linear interpolation
 return a+(b-a)*t

def bezier_curve(val):
 def de_casteljau(l,t):
  while len(l)>1:l=[lerp(l[i],l[i+1],t)for i in range(len(l)-1)]
  return l
 x,y=[],[]
 for i in range(step+1):
  t=1/step*i
  x.append(de_casteljau([v[0]for v in val],t)[0])
  y.append(de_casteljau([v[1]for v in val],t)[0])
 for i in range(step):
  dl(ent(x[i]),ent(y[i]),ent(x[i+1]),ent(y[i+1]),3)

def c_v(a,b,c,lr): #Calculate (new) Values
 v1,v2,v3=value[a],value[b],value[c]
 x1,y1,x2,y2,x3,y3=v1[0],v1[1],v2[0],v2[1],v3[0],v3[1]
 r1,r2=dst(x1,y1,x2,y2),dst(x3,y3,x2,y2)
 dx,dy=(va(x1-x2)/r1)*(1 if x2>=x1 else -1),(va(y1-y2)/r1)*(1 if y2>=y1 else -1)
 rd=r1 if lr-1 else r2 #Lock Rotation (or not)
 nx,ny=x2+dx*rd,y2+dy*rd
 value[c]=(ent(nx),ent(ny))

def move(i,n):
 vl=value[n]
 xv=vl[0]-dm if i==0 else vl[0]+dm if i==3 else vl[0]
 yv=vl[1]-dm if i==1 else vl[1]+dm if i==2 else vl[1]
 value[n]=(xv,yv)

new=True
for v in ct:c_v(v[0],v[1],v[2],v[3])
while True:
 if new:
  new=False
  fr(0,0,320,222,wh)
  for link in links:bezier_curve([value[i]for i in link])
  for v in ct:dl(value[v[0]][0],value[v[0]][1],value[v[2]][0],value[v[2]][1],1,(120,)*3)
  draw_points()

 for i in range(4): #Tentative de simplification des mouvements
  if kd(i):
   vl=value[wv]
   for n in range(4):
    f,v1,v2=inf if n<2 else sup,1 if n in[1,2]else 0,height if n==2 else width if n==3 else 0
    if i==n and f(vl[v1],v2):n=5;break
   if n==5:continue
   move(i,wv)
   for v in ct:
    a,b,c,d=v[0],v[1],v[2],v[3]
    if wv==a:c_v(a,b,c,d)
    if wv==b:move(i,a),move(i,c)
    if wv==c:c_v(c,b,a,d)
   new=True
 if kd(4)or kd(52):wv=wv+1 if wv<len(value)-1 else 0;draw_points();sl(0.1)

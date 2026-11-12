#Créé le 16 Août 2024
from math import pi,sin,cos,sqrt,fabs as va,floor
from kandinsky import fill_rect as fr
from ion import keydown as kd
from time import sleep as sl

bk,wh=(0,)*3,(255,)*3
re,gr,bl=(255,0,0),(0,255,0),(0,0,255)

value=[(20,20),(270,50),(40,180),(250,200)] #tous nos points
wv=0 #which value
step=30 #nombre d'étapes pour dessiner la courbe
dm=3 #valeur du déplacement de la séléction
width,height=320,222
cr=3 #taille du cercle

ent=lambda n:floor(n)if n-floor(n)<0.5 else floor(n)+1

def draw_point(cx,cy,cl):
 for rep in range(8*cr*pi):
  adj=cos(rep)*cr
  x=cx+adj
  opp=sin(rep)*cr
  y=cy+opp
  fr(ent(x),ent(y),1,-2*ent(opp),cl)

def dl(x1,y1,x2,y2,t=1): #draw_line
 w=h=1
 dx=min(max((x2-x1)/va(y2-y1)if va(y2-y1)!=0 else x2-x1,-1),1)
 dy=min(max((y2-y1)/va(x2-x1)if va(x2-x1)!=0 else y2-y1,-1),1)
 c=va(x2-x1)if va(x2-x1)>va(y2-y1)else va(y2-y1)
 if va(dx)<va(dy):w,x1,x2=t,x1-(t-1)//2,x2-(t-1)//2
 else:h,y1,y2=t,y1-(t-1)//2,y2-(t-1)//2
 for i in range(c):fr(ent(x1+dx*i),ent(y1+dy*i),w,h,bk)

def lerp(a,b,t): #linear interpolation
 return a+(b-a)*t

def quadratic_curve(a,b,c,t):
 p0=lerp(a,b,t)
 p1=lerp(b,c,t)
 return lerp(p0,p1,t)

def cubic_curve(a,b,c,d,t):
 p0=quadratic_curve(a,b,c,t)
 p1=quadratic_curve(b,c,d,t)
 return lerp(p0,p1,t)

def draw_curve():
 x,y=[],[]
 for i in range(step+1):
  t=1/step*i
  x.append(cubic_curve(value[0][0],value[1][0],value[2][0],value[3][0],t))
  y.append(cubic_curve(value[0][1],value[1][1],value[2][1],value[3][1],t))
 for i in range(step):
  dl(ent(x[i]),ent(y[i]),ent(x[i+1]),ent(y[i+1]),3)

new=True
while True:
 if new:
  new=False
  fr(0,0,320,222,wh)
  draw_curve()
  for i in range(len(value)):
   cl=bl if i==wv else re if i in[1,2] else gr
   draw_point(value[i][0],value[i][1],cl)

 for i in range(4): #Tentative de simplification des mouvements
  if kd(i):
   vl=value[wv]
   if i==0 and not vl[0]>0:continue
   elif i==1 and not vl[1]>0:continue
   elif i==2 and not vl[1]<height:continue
   elif i==3 and not vl[0]<width:continue
   xv=vl[0]-dm if i==0 else vl[0]+dm if i==3 else vl[0]
   yv=vl[1]-dm if i==1 else vl[1]+dm if i==2 else vl[1]
   value[wv],new=(xv,yv),True
 if kd(4)or kd(52):wv=wv+1 if wv<len(value)-1 else 0;new=True;sl(0.1)

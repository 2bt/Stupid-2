import sys,math,pygame,savage
from stupid import*
from vec import*
class W(Entity):
 def __init__(S):Entity.__init__(S);S.o=savage.Orb(.1,3).gen_list();S.p=[vec(*map(eval,l.split()))for l in open("wave.txt")];m=[];exec"m=[1]+map(sum,zip(m,m[1:]))+[1];"*~-len(S.p);S.m=m;S.f=0
 def update_sub(S,time_dif):S.f^=Stupid.key_state(K_t,1)
 def b(S,t):l=len(S.p);return sum((c*(1-t)**i*x*t**(l-i-1)for i,x,c in zip(range(l),S.p,S.m)),vec())
 def l(S,t):l=len(S.p);r=range(l);return sum((x*reduce(float.__mul__,((t*~-l-k)/(i-k+.0)for k in r if i-k))for i,x in zip(r,S.p)),vec())
 def render_sub(S):
	glDisable(2896);glDisable(2929);p=S.p;glLineWidth(5);glColor(.3,.3,.25)
	for x in p:glPushMatrix();glTranslate(*x);glCallList(S.o);glPopMatrix()
	glBegin(3)
	for x in p:glVertex(x)
	glEnd();glBegin(3);glColor(0,0,0)
	f=[S.l,S.b][S.f];d=a=f(0);glVertex(a);t=0
	while t<1:t+=.01;b=f(t);c=b-a;glColor(0,0,1-c.normalize().dot(d)**150);glVertex(b);a=b;d=c
	glEnd()
s=Stupid("4")
s.add(W())
s.mainloop()

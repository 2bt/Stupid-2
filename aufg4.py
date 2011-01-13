from stupid import*
import savage
T=glTranslate;C=glColor;V=glVertex;R=range;B=glBegin;D=glDisable;F=Stupid
class W(Entity):
 def __init__(S):Entity.__init__(S);S.o=savage.Orb(.1,3).gen_list();S.p=[vec(*map(eval,l.split()))for l in open("wave.txt")];m=[];exec"m=[1]+map(sum,zip(m,m[1:]))+[1];"*~-len(S.p);S.m=m;S.f=0
 def b(S,t):l=len(S.p);return sum((c*(1-t)**i*x*t**(l-i-1)for i,x,c in zip(R(l),S.p,S.m)),vec())
 def l(S,t):l=len(S.p);return sum((x*reduce(float.__mul__,((t*~-l-k)/(i-k+.0)for k in R(l)if i-k))for i,x in zip(R(l),S.p)),vec())
 def render_sub(S):
	S.f^=F.key_state(K_t,1);D(2896);D(2929);p=S.p;glLineWidth(5);C(.3,.3,.25)
	for x in p:T(*x);glCallList(S.o);T(*-x)
	B(3)
	for x in p:V(x)
	glEnd();B(3);C(0,0,0);f=[S.l,S.b][S.f];d=a=f(0);V(a);t=0
	while t<1:t+=.01;b=f(t);c=b-a;C(0,0,1-c.normalize().dot(d)**150);V(b);a=b;d=c
	glEnd()
s=F("")
s.add(W())
s.mainloop()

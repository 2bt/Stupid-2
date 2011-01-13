from stupid import*;import savage
T=glTranslate;C=glColor;V=glVertex;B=glBegin;D=glDisable;F=Stupid;
p=[vec(*map(eval,l.split()))for l in open("wave.txt")];l=len(p);r=range(l);v=vec()
m=[];exec"m=[1]+map(sum,zip(m,m[1:]))+[1];"*~-l
class W(Entity):
 def __init__(S):Entity.__init__(S);S.f=0
 def b(S,t):return sum((c*(1-t)**i*x*t**(l-i-1)for i,x,c in zip(r,p,m)),v)
 def l(S,t):return sum((x*reduce(float.__mul__,((t*~-l-k)/(i-k+.0)for k in r if i-k))for i,x in zip(r,p)),v)
 def render(S):
	S.f^=F.key_state(K_t,1);D(2896);D(2929);glLineWidth(5);C(.3,.3,.25)
	for x in p:T(*x);glCallList(o);T(*-x)
	B(3);map(V,p);glEnd();B(3);C(*v);f=[S.l,S.b][S.f];d=a=f(0);V(a);t=0
	while t<1:t+=.005;b=f(t);c=b-a;C(0,0,1-c.normalize().dot(d)**150);V(b);a=b;d=c
	glEnd()
s=F("");o=savage.Orb(.1,3).gen_list();s.add(W());s.mainloop()

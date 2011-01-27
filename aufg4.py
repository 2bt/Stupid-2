from stupid import*;from savage import*
T=glTranslate;C=glColor;V=glVertex;B=glBegin;D=glDisable
p=[vec(*map(eval,l.split()))for l in open("wave.txt")];l=len(p);r=range(l);v=vec()
m=[];exec"m=[1]+map(sum,zip(m,m[1:]))+[1];"*~-l
class W(Entity):
 f=0;b=lambda S,t:sum((c*(1-t)**i*x*t**(l+~i)for i,x,c in zip(r,p,m)),v);l=lambda S,t:sum((x*reduce(float.__mul__,((t*~-l-k)/(i-k)for k in r if i-k))for i,x in zip(r,p)),v)
 def render(S):
	S.f^=s.key_state(K_t,1);D(2896);D(2929);glLineWidth(5);C(.3,.3,.25)
	for x in p:T(*x);o.render();T(*-x)
	B(3);map(V,p);glEnd();B(3);C(*v);f=[S.l,S.b][S.f];t=.0;d=a=f(t);V(a)
	while t<1:t+=.01;b=f(t);c=b-a;C(0,0,1-c.normalize().dot(d)**150);V(b);a=b;d=c
	glEnd()
s=Stupid("");o=Orb(.1,3);o.gen_list();s.add(W());s.mainloop()

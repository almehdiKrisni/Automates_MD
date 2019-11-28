from automate import Automate
from state import State
from transition import Transition
from parser import *

print("DEBUT PROGRAMME\n")

s1=State(1, True, True)
s2=State(2, False, False)
t1= Transition(s1,"a",s1)
t2=Transition(s1,"a",s2)
t4=Transition(s2,"a", s2)
t5=Transition(s2,"b",s2)
t6= Transition(s1,"a",s1)
t7= Transition(s2,"b",s1)
listeT1 = [t1,t2,t4,t5,t6,t7]
a=Automate(listStates=[], label="a", listTransitions=listeT1)
print(a)


s3=State(1,True,False)
s4=State(2,False,True)

tb1= Transition(s3,"b",s3)
tb2= Transition(s3,"a",s4)
tb3= Transition(s4,"b",s4)
tb4= Transition(s4,"c",s3)
tb5 = Transition(s3,"b",s4)
listeT2 = [tb1,tb2,tb3,tb4,tb5]
b=Automate(listStates=[s3,s4], label= "b", listTransitions = listeT2)
print(b)

s5=State(3,False,False)
tc1 = Transition(s1,"b",s1)
tc2 = Transition(s1,"c",s1)
tc3 = Transition(s1,"a",s2)
tc4 = Transition(s2,"a",s2)
tc5 = Transition(s2,"b",s5)
tc6 = Transition(s2,"c",s2)
tc7 = Transition(s5,"a",s5)
tc8 = Transition(s5,"b",s5)
tc9 = Transition (s5,"c",s1)
listeT3= [tc1,tc2,tc3,tc4,tc5,tc6,tc7,tc8,tc9]
c=Automate(listStates=[s1,s2,s5], label= "c", listTransitions = listeT3)
print(c)

s6=State(2,True,True)
tc1= Transition(s1,"a",s6)
tc2 = Transition(s6,"b",s1)
listeT4=[tc1,tc2]
d=Automate(listStates=[s1,s6], label = "d", listTransitions = listeT4)
print(d)

list = [s1,s2]
print (a.succ(list,"c"))
print (a.succ(list,"b"))
list2 = [s1,s6]
print (d.succ(list2,"c"))
print (d.succ(list2,"b"))
print ("Etats accessibles")

print (Automate.accepte(a, "abc"))
print (Automate.accepte(a, "aaabbcb"))
print (Automate.accepte(a, "abs"))
print (Automate.accepte(c, "abc"))
print (Automate.accepte(c, "aaabbcb"))
print (Automate.accepte(c, "abcs"))
a.show("hey.pdf")
a.show("salut")



print (Automate.estComplet(a,["a","b","c"]))
print (Automate.estComplet(a, ["0","1"]))
print (Automate.estComplet(a, ["a","b"]))
print (Automate.estComplet(c,["a","b","c"]))

print ("\nDeterministe\n")
print (Automate.estDeterministe(a))
print (Automate.estDeterministe(b))
print (Automate.estDeterministe(c))
print (Automate.estDeterministe(d))

e=Automate.completeAutomate(a,["a","b"])
a.show("automate_a")
e.show("e=a_aprescompletion")
print(e)

print("Determinisation")
f = Automate.determinisation(b)
f.show("Determinisationb")

G = Automate.determinisation(d)
d.show("Determinisationd")

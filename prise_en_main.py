from transition import *
from state import *
import os
import copy
from sp import *
from parser import *
from itertools import product
from automateBase import AutomateBase
from automate import Automate

def main():
    ### EXERCICE 2
    # Création des états et des transitions
    s0 = State(0, True, False)
    s1 = State(1, False, False)
    s2 = State(2, False, True)
    t1 = Transition(s0, "a", s1)
    t2 = Transition(s0, "b", s1)
    t3 = Transition(s1, "a", s2)
    t4 = Transition(s1, "b", s2)
    t5 = Transition(s2, "a", s0)
    t6 = Transition(s2, "b", s1)

    # On crée l'automate 0 à partir de transitions
    auto = Automate([t1, t2, t3, t4, t5, t6])
    print(auto)
    # On crée l'automate 1 à partir de transitions et d'états (auto et auto1 sont identiques)
    auto1 = Automate([t1, t2, t3, t4, t5, t6], [s0, s1, s2])
    print(auto1)
    # On crée l'automate 2 à partir d'un fichier
    auto2 = Automate.creationAutomate("exempleAutomate.txt")
    print(auto2)


    """# On print l'automate 0 dans un pdf
    auto.show("auto_ListeTrans")
    # On print l'automate 0 dans un pdf
    auto1.show("auto1_ListeTrans")
    # On print l'automate 0 dans un pdf
    auto2.show("auto2_ListeTrans")"""


    # TRAVAIL SUR L'AUTOMATE 0
    # On supprime une transition (t1) et on affiche le résultat
    auto.removeTransition(t1)
    print(auto)
    # On rajoute la transition supprimée et on affiche le résultat
    auto.addTransition(t1)
    print(auto)
    # On supprime l'état 1 (s1) de l'automate 0 et on affiche le résultat
    auto.removeState(s1)
    print(auto)
    # On ajoute l'état 1 (s1) de l'automate 0 et on affiche le résultat
    auto.addState(s1)
    print(auto)
    # On affiche les transitions de l'automate 0
    print(auto.getListTransitionsFrom(s1))
    print()


    ### EXERCICE 3
    # On récupère l'automate auto1 pour effectuer les tests
    print(auto1.succ([s0, s1, s2], "a"))
    print()
    # On vérifie si un mot est accepté ou non par l'automate auto1
    print("L'automate auto1 accepte-t-il le mot 'aababaabbba' : " +  str(Automate.accepte(auto1, "aababaabbba")))
    print()
    # On vérifie si les automates auto1 et auto2 sont complets
    print("L'automate auto1 est-il complet : " +  str(Automate.estComplet(auto1, auto1.getAlphabetFromTransitions())))
    print("L'automate auto2 est-il complet : " +  str(Automate.estComplet(auto2, auto2.getAlphabetFromTransitions())))
    print()
    # On vérifie si les automates auto1 et auto2 sont déterministes
    print("L'automate auto1 est-il déterministe : " + str(Automate.estDeterministe(auto1)))
    print("L'automate auto2 est-il déterministe : " + str(Automate.estDeterministe(auto2)))
    print()
    # On complète l'automate auto2
    #auto2.show("Avant_la_completion.pdf")
    #new_auto2 = Automate.completeAutomate(auto2, auto2.getAlphabetFromTransitions())
    #new_auto2.show("Apres_la_completion.pdf")
    

    ss0 = State(0, True, False)
    ss1 = State(1, False, False)
    ss2 = State(2, False, False)
    ss3 = State(3, False, True)
    tt1 = Transition(ss0, "a", ss0)
    tt2 = Transition(ss0, "b", ss0)
    tt3 = Transition(ss0, "b", ss1)
    tt4 = Transition(ss1, "a", ss2)
    tt5 = Transition(ss2, "b", ss3)

    autotest = Automate([tt1, tt2, tt3, tt4, tt5])
    print(autotest)
    autotest.show("autotest_avant_determinisation")
    new_autotest = Automate.determinisation(autotest)
    print(new_autotest)
    new_autotest.show("autotest_apres_determinisation")
    


if __name__ == "__main__":
    main()
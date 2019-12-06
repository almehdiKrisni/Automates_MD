# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from sp import *
from parser import *
from itertools import product
from automateBase import AutomateBase



class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        
        setSucc = []
        for s in listStates :
            for t in self.getListTransitionsFrom(s) :
                if ((t.stateDest not in setSucc) and (t.etiquette == lettre)) :
                    setSucc.append(t.stateDest)

        return setSucc
                



    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """

    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """

        trans = auto.getListInitialStates()

        for i in range(len(mot)) :
            for s in auto.succ(trans, mot[i]) :
                if (i == len(mot) - 1) and (s.fin) :
                    return True
            trans = auto.succ(trans, mot[i])
        return False


    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """

        for s in auto.listStates :
            for a in alphabet :
                if auto.succElem(s, a) == [] :
                    return False
        
        return True


        
    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """

        if len(auto.getListInitialStates()) > 1 :
            return False

        for s in auto.listStates :
            for a in auto.getAlphabetFromTransitions() :
                if len(auto.succElem(s, a)) > 1 :
                    return False

        return True
        
       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """

        if Automate.estComplet(auto, alphabet) :
            print("L'automate est déja complet")
            return auto

        new_auto = auto
        i = 0

        for s in new_auto.listStates :
            for a in alphabet :
                if new_auto.succElem(s, a) == [] :
                    ns = State("neo" + str(s.id), False, False)
                    i = i + 1
                    new_auto.addTransition(Transition(s, a, ns))
                    for l in alphabet :
                        new_auto.addTransition(Transition(ns, l, ns))

        return new_auto

       

    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """

        if auto.estDeterministe :
            return auto

        listTransitions = []
        alphabet = list(auto.getAlphabetFromTransitions())
        dicoStates = dict()

        aTraiter = []
        dejaTraiter = []

        numero = 0

        setATraiter = set()
        for s in auto.getListInitialStates() :
            setATraiter.add(s)
        aTraiter.append(setATraiter)

        for a in aTraiter :
            if str(a) not in dicoStates.keys() :
                dicoStates[str(a)] = State(numero, True, any(i.fin for i in a), str(a))
                numero = numero + 1

        while aTraiter != [] :

            listRepro = aTraiter

            for a in listRepro :

                if str(a) not in dicoStates.keys() :
                    dicoStates[str(a)] = State(numero, any(i.init for i in a), any(i.fin for i in a), str(a))
                    numero = numero + 1

                dejaTraiter.append(a)

                listElem = []
                for b in a :
                    listElem.append(b)

                for l in alphabet :
                    listDest = auto.succ(listElem, l)
                    dest = set(listDest)

                    if dest == set() :
                        continue

                    if str(dest) not in dicoStates.keys() :
                        dicoStates[str(dest)] = State(numero, False, any(i.fin for i in dest), str(dest))
                        numero = numero + 1
                        
                    if Transition(dicoStates[str(a)], l, dicoStates[str(dest)]) not in listTransitions :
                        listTransitions.append(Transition(dicoStates[str(a)], l, dicoStates[str(dest)]))

                    if dest not in dejaTraiter :
                        aTraiter.append(dest)

                aTraiter.remove(a)
                dejaTraiter.append(a)

        autonew = Automate(listTransitions)
        return autonew

 
    @staticmethod
    def complementaire(auto,alphabet):
        autocpy = copy.deepcopy(auto)
        
        new_auto = Automate.completeAutomate(Automate.determinisation(autocpy), auto.getAlphabetFromTransitions())

        for v in new_auto.listStates :
            v.fin = not v.fin

        return new_auto
   
    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """



        return

    @staticmethod
    def union (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """

        autonew = Automate([])
        autonew.listStates = auto1.listStates + auto2.listStates
        autonew.listTransitions = auto1.listTransitions + auto2.listTransitions

        alphabet = autonew.getAlphabetFromTransitions()

        autonew.show("Pre_Union")

        origin = State(0, True, False, "Origin")
        autonew.listStates.append(origin)

        for s in autonew.listStates :
            if (s in auto1.getListInitialStates()) or (s in auto2.getListInitialStates()) :
                s.init = False
                for a in alphabet :
                    listTrans = autonew.succElem(s, a)
                    for t in listTrans :
                        autonew.listTransitions.append(Transition(origin, a, t))

        autonew.show("Post_Union")

        return autonew


    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """

        autonew = Automate([])
        autonew.listStates = auto1.listStates + auto2.listStates
        autonew.listTransitions = auto1.listTransitions + auto2.listTransitions

        alphabet = autonew.getAlphabetFromTransitions()

        #autonew.show("Pre_Concatenation")

        for i2 in auto2.getListInitialStates() :
            for f1 in auto1.getListFinalStates() :
                if i2.fin == False :
                    f1.fin = False
                for a in alphabet :
                    listTrans = auto2.succElem(i2, a)
                    for ns in listTrans :
                        if ns == i2 :
                            autonew.listTransitions.append(Transition(f1, a, f1))
                        else :
                            autonew.listTransitions.append(Transition(f1, a, ns))
            autonew.listStates.remove(i2)

        print("\nsalut\n")
        
        #autonew.show("Post_Concatenation")

        return autonew
        
       
    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """

        #auto.show("Pre_Etoile")

        autonew = copy.deepcopy(auto)
        alphabet = auto.getAlphabetFromTransitions()

        for s in autonew.getListInitialStates() :
            for a in alphabet :
                transList = list(autonew.succElem(s, a))
                for f in autonew.getListFinalStates() :
                    for ns in transList :
                        if ns not in autonew.getListInitialStates() :
                            autonew.listTransitions.append(Transition(f, a, ns))

        for i in autonew.getListInitialStates() :
            i.fin = True

        #autonew.show("Post_Etoile")

        return autonew





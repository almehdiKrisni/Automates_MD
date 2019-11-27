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
            if (i == len(mot) - 1) :
                for s in auto.succ(trans, mot[i]) :
                    if s.fin :
                        return True
                return False
            else :
                if auto.succ(trans, mot[i]) != [] :
                    trans = auto.succ(trans, mot[i])
                else :
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
        i = len(auto.listStates)

        for s in new_auto.listStates :
            for a in alphabet :
                if new_auto.succElem(s, a) == [] :
                    ns = State(i, False, False)
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

                    if str(dest) not in dicoStates.keys() :
                        dicoStates[str(dest)] = State(numero, False, any(i.fin for i in dest), str(dest))
                        numero = numero + 1
                        
                    listTransitions.append(Transition(dicoStates[str(a)], l, dicoStates[str(dest)]))

                    if dest not in dejaTraiter :
                        aTraiter.append(dest)

                aTraiter.remove(a)
                dejaTraiter.append(a)

        autonew = Automate(listTransitions)
        return autonew

 
    @staticmethod
    def complementaire(auto,alphabet):
        listEtats = auto.listStates

        for v in listEtats :
            v.fin = !(v.fin)

        return Automate(auto.listTransitions, listEtats)
   
    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        return

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        return
        

   
       

    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        return
        
       
    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        return





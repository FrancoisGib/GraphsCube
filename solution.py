from __future__ import annotations
from typing import Union
import cubeGame as cb
from collections import deque
import numpy as np
import heapq


class Node:
    """Une classe de noeuds d'un arbre ou graphe de recherche"""
    def __init__(self, plateau: cb.Plateau,
                 pred: Union[Node, None] = None,
                 action: str = "None") -> None:
        """On mémorise dans le noeud
        - l'état du jeu correspondant : le plateau
        - le noeud précédent
        - l'action qui a mené dans cet état"""
        self._plateau = plateau
        self._predecesseur = pred
        self._action = action
        # la liste des actions possibles est les 4 directions
        # ici, je mémorise les 4 fonctions qui instancient ces directions
        # on peut accéder à une représentation sous forme de string
        # d'une fonction par l'attribut __name__
        self._actions = [plateau.haut, plateau.bas,
                         plateau.droite, plateau.gauche]

    def _solution_rec(self, acc: list) -> list:
        """On a besoin d'un accumulateur pour implanter la récursion
        qui calcule le chemin de la racine à ce noeud"""
        if self._predecesseur:
            solution = self._predecesseur._solution_rec([self._action] + acc)
            return solution
        return acc

    def solution(self) -> list:
        """Calcul du chemin de la racine au noeud"""
        return ['None'] + self._solution_rec([]) # racine donc []

    def __iter__(self):
        """Retourne un itérateur sur les actions de ce noeud.
        On peut donc écrire for "action in node"...
        """
        return self._actions.__iter__()

    def final(self):
        """Un noeud est final si le plateau est final"""
        return self._plateau.final()

    def __eq__(self, __o: object) -> bool:
        """Deux noeuds sont égaux si ils ont le même plateau"""
        if not isinstance(__o, Node):
            raise NotImplemented()
        return self._plateau == __o._plateau

    def __hash__(self) -> int:
        """On ne peut stocker que des valeurs hachables comme clef
        dans les dictionnaires (dict) ou ensembles (set).
        Par défaut, seuls les non mutables sont hachables.
        Mais ici un noeud ne doit pas être modifié, on va le
        hacher selon la représentation textuelle de son plateau
        (cela peut être coûteux si on avait un grand plateau...)"""
        return hash(self._plateau.__repr__())


def recherche_largeur(start: cb.Plateau) -> Union[None, list[str]]:
    """Parcours en largeur"""
    root = Node(start) # sommet initial
    visited = set()
    toVisit = deque([root])
    while len(toVisit) > 0:
        node = toVisit.popleft() # popleft sinon pop() rapprocherait de la recherche par profondeur
        visited.add(node)
        if node.final(): # on a une solution
            return node.solution() # on renvoie le chemin de ce noeud jusqu'à la racine
        for act in node: # on teste pour chaque actions
            try:
                next = Node(act(), node, act.__name__) # prochain noeud à tester
                if next not in toVisit:
                    toVisit.append(next)
            except cb.HorsPlateau:
                pass
    return [None] # pas de solution


def recherche_profondeur_bornee(start: cb.Plateau, maxDepth: int) -> Union[None, list[str]]:
    "Parcours en profondeur bornée"
    root = Node(start)
    depth = 0
    toVisit = deque([(root, 0)]) # tuple du noeud et de la profondeur de celui-ci
    visited = set()
    while len(toVisit) > 0:
        node, depth = toVisit.pop()
        visited.add(node)
        if node.final():
            return node.solution()
        if depth < maxDepth:
            for act in node: # on teste pour chaque actions
                try:
                    next = Node(act(), node, act.__name__) # prochain noeud à tester
                    if next not in visited:
                        toVisit.append((next, depth+1))
                except cb.HorsPlateau:
                    pass
    return [None]

if __name__ == "__main__":
    long_alea = 4
    maxDepth = 10

    start = cb.Plateau(do_alea=True, long_alea=long_alea)
    print(start)
    solution1 = recherche_largeur(start)
    solution2 = recherche_profondeur_bornee(start, maxDepth)
    print("Solution 1 : \n", solution1)
    print("Solution 2 : \n", solution2)
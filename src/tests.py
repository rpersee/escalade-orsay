#!/usr/bin/env python3

from main import get_flag


def test_get_flag():
    # Test case for a basic flag in the string
    assert get_flag("départ assis", "Bleu clair. Départ assis sous R7") == True
    assert get_flag("module", "3 prises ! Sans module. Avec dièdre et arête.") == False
    
    # Test case for a flag not in the string
    assert get_flag("départ assis", "2 variantes, fin R8 ou R10") == False
    assert get_flag("module", "5a dalle, 5c vertical, cotations à confirmer, prises à grosses vis. Dalle faisable sans mains") == False
    
    # Test case with parentheses
    assert get_flag("départ assis", "Départ allongé (pas assis).") == False
    assert get_flag("module", "7b? (avec module)") == True
    assert get_flag("arête", "Module (mais pas à droite), arêtes autorisées") == True
    assert get_flag("module", "Avec module (5b+ sans)") == True
    
    # Test case for nested parentheses
    assert get_flag("module", "Tout autorisé (arête, dièdre (mais pas à gauche), module).") == True
    assert get_flag("arête", "Avec carré Entreprises. Sans module,sans arête. Cot. à confirmer.") == False
    
    # Test case for modifiers
    assert get_flag("arête", "Avec inserts et sans arêtes") == False
    assert get_flag("départ assis", "Avec module et arête à D. Départ assis.") == True
    assert get_flag("arête", "Sans module. Trois prises à G. de l'arête.") == False
    assert get_flag("module", "Avec module. Pas final 5c") == True
    assert get_flag("module", "Pas final en 5b+, module.") == True
    assert get_flag("arrête", "Pas d'arêtes mais inserts") == False
    assert get_flag("arête", "Ni arêtes, ni inserts. Départ assis") == False


if __name__ == "__main__":
    test_get_flag()
    print("All tests passed!")

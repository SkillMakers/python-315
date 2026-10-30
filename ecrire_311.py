# Ecrit un fichier SANS preciser encoding= : sous Windows avant 3.15, c'est cp1252
open("clients.csv", "w").write("nom;ville\nHélène;Besançon\nJérôme;Orléans\n")

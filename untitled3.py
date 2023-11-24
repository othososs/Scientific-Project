Sub ChangerMois(versMoisSuivant As Boolean)
    Dim feuille As Worksheet
    Dim colonneDebut As Integer
    Dim colonneFin As Integer
    Dim ligneDebut As Integer
    Dim ligneFin As Integer
    Dim celluleDate As Range
    Dim nouvelleDate As Date
    
    ' Spécifiez la feuille de calcul
    Set feuille = ThisWorkbook.Sheets("NomDeVotreFeuille") ' Remplacez "NomDeVotreFeuille" par le nom de votre feuille
    
    ' Spécifiez la plage de colonnes et de lignes
    colonneDebut = 5 ' Colonne E
    colonneFin = 34 ' Colonne AH
    ligneDebut = 2 ' 2ème ligne
    ligneFin = 30 ' 30ème ligne
    
    ' Trouver la cellule contenant la date actuelle (la première date dans la plage spécifiée)
    Set celluleDate = feuille.Cells(ligneDebut, colonneDebut)
    
    ' Récupérer la date actuelle
    Dim dateActuelle As Date
    dateActuelle = celluleDate.Value
    
    ' Calculer la nouvelle date en ajoutant ou en soustrayant un mois
    If versMoisSuivant Then
        nouvelleDate = DateAdd("m", 1, dateActuelle)
    Else
        nouvelleDate = DateAdd("m", -1, dateActuelle)
    End If
    
    ' Mettre à jour la première cellule de date
    celluleDate.Value = nouvelleDate
    
    ' Mettre à jour les valeurs en dessous de la date dans la plage spécifiée
    Dim i As Integer
    For i = ligneDebut + 1 To ligneFin
        feuille.Cells(i, colonneDebut).FormulaR1C1 = "=EDATE(R[-1]C,1)"
    Next i
End Sub

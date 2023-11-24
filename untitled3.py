Sub DeplacerMois()

    Dim debutColonne As Integer
    Dim finColonne As Integer
    Dim dateCell As Range
    Dim moisActuel As Integer
    Dim anneeActuelle As Integer

    ' Spécifiez la plage des colonnes contenant les dates
    debutColonne = 5 ' Colonne E
    finColonne = 26 ' Colonne Z

    ' Récupérez la date de la première cellule de la plage
    Set dateCell = Cells(1, debutColonne)

    ' Obtenez le mois actuel et l'année
    moisActuel = Month(dateCell.Value)
    anneeActuelle = Year(dateCell.Value)

    ' Demandez à l'utilisateur s'il veut déplacer vers le mois suivant ou précédent
    Dim choix As Integer
    choix = MsgBox("Voulez-vous déplacer vers le mois suivant (Oui) ou le mois précédent (Non)?", vbYesNo)

    ' Déplacez les dates en conséquence
    If choix = vbYes Then
        moisActuel = moisActuel + 1
        If moisActuel > 12 Then
            moisActuel = 1
            anneeActuelle = anneeActuelle + 1
        End If
    Else
        moisActuel = moisActuel - 1
        If moisActuel < 1 Then
            moisActuel = 12
            anneeActuelle = anneeActuelle - 1
        End If
    End If

    ' Mettez à jour les dates dans les colonnes spécifiées
    For i = debutColonne To finColonne
        Set dateCell = Cells(1, i)
        dateCell.Value = GetProchaineDateValide(dateCell.Value, choix)
    Next i

End Sub

Function GetProchaineDateValide(dateOrigine As Date, sens As Integer) As Date
    ' Fonction pour obtenir la prochaine date valide (en excluant les week-ends)

    Dim nouvelleDate As Date
    Dim joursAajouter As Integer
    nouvelleDate = dateOrigine
    
    ' Spécifie le nombre de jours à ajouter ou soustraire en fonction du sens
    If sens = vbYes Then
        joursAajouter = 1
    Else
        joursAajouter = -1
    End If

    ' Ajoute ou soustrait les jours et ajuste si nécessaire pour éviter les week-ends
    Do
        nouvelleDate = DateAdd("d", joursAajouter, nouvelleDate)
    Loop While Weekday(nouvelleDate, vbMonday) > 5 ' Exclut les samedis et dimanches

    GetProchaineDateValide = nouvelleDate
End Function

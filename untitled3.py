Sub ChangerDatesEtValeursSansWeekend()
    ' Demander à l'utilisateur d'entrer le mois
    Dim mois As String
    mois = InputBox("Entrez le mois (MM/YYYY) :", "Changer les dates")

    ' Vérifier si l'utilisateur a annulé
    If mois = "" Then
        Exit Sub
    End If

    ' Déterminer le premier jour du mois
    Dim premierJour As Date
    premierJour = DateValue("01/" & mois)

    ' Boucler à travers les colonnes de E à AH
    Dim col As Integer
    For col = 5 To 34 ' Correspond à la plage E1:AH1
        ' Trouver le premier jour ouvrable du mois
        While Weekday(premierJour, vbMonday) > 5 ' Si c'est un week-end
            premierJour = premierJour + 1 ' Passer au jour suivant
        Wend

        ' Changer la date dans la cellule en fonction du mois fourni par l'utilisateur
        Cells(1, col).Value = premierJour

        ' Effacer les valeurs dans les cellules de la colonne correspondante (ligne 2 à 30)
        Columns(col).Range("A2:A30").ClearContents

        ' Passer au jour ouvrable suivant
        premierJour = premierJour + 1
    Next col
End Sub

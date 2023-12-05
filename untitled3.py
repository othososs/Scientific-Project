Sub CreerCalendrier()
    Dim dateDebut As Date
    Dim dateFin As Date
    Dim mois As Integer
    Dim annee As Integer
    Dim jourActuel As Date
    Dim colActuelle As Integer
    
    ' Demander à l'utilisateur de saisir le mois et l'année
    mois = InputBox("Entrez le mois (1-12):", "Mois")
    annee = InputBox("Entrez l'année:", "Année")
    
    ' Vérifier si les valeurs saisies sont valides
    If mois < 1 Or mois > 12 Then
        MsgBox "Mois invalide. Veuillez entrer un mois entre 1 et 12.", vbExclamation
        Exit Sub
    End If
    
    ' Définir la date de début comme étant le premier jour du mois spécifié
    dateDebut = DateSerial(annee, mois, 1)
    
    ' Trouver le dernier jour du mois
    dateFin = DateSerial(annee, mois + 1, 1) - 1
    
    ' Boucler à travers les jours du mois
    For jourActuel = dateDebut To dateFin
        ' Vérifier si le jour est un jour de semaine (du lundi au vendredi)
        If Weekday(jourActuel, vbMonday) >= 2 And Weekday(jourActuel, vbMonday) <= 6 Then
            ' Trouver la prochaine colonne vide à partir de la colonne E
            colActuelle = Cells(1, Columns.Count).End(xlToLeft).Column + 1
            
            ' Mettre à jour la cellule avec la nouvelle date
            Cells(1, colActuelle).Value = jourActuel
        End If
    Next jourActuel
End Sub

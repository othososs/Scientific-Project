Sub GenererDates()
    ' Déclaration des variables
    Dim ws As Worksheet
    Dim debutColonne As Integer
    Dim finColonne As Integer
    Dim ligneDebut As Integer
    Dim ligneFin As Integer
    Dim moisAnnee As String
    Dim dateDebut As Date
    Dim dateFin As Date
    Dim dateCourante As Date
    
    ' Spécifiez le nom de votre feuille de calcul
    Set ws = ThisWorkbook.Sheets("NomDeVotreFeuille")
    
    ' Spécifiez la plage des colonnes E à AC
    debutColonne = 5 ' Colonne E
    finColonne = 29 ' Colonne AC
    
    ' Spécifiez la plage des lignes de 2 à 30
    ligneDebut = 2
    ligneFin = 30
    
    ' Effacez les dates de la première ligne
    ws.Range(ws.Cells(1, debutColonne), ws.Cells(1, finColonne)).ClearContents
    
    ' Effacez les valeurs dans la plage spécifiée
    ws.Range(ws.Cells(ligneDebut, debutColonne), ws.Cells(ligneFin, finColonne)).ClearContents
    
    ' Demandez à l'utilisateur de saisir le mois/année au format "mm/yyyy"
    moisAnnee = InputBox("Entrez le mois/année au format mm/yyyy", "Mois/Année")
    
    ' Vérifiez si l'entrée est valide
    If IsDate("01/" & moisAnnee) Then
        dateDebut = DateValue("01/" & moisAnnee)
        dateFin = DateAdd("m", 1, dateDebut) - 1 ' Dernier jour du mois
        dateCourante = dateDebut
        
        ' Générez les dates et remplissez la première ligne
        For i = debutColonne To finColonne
            ' Ignorez les weekends (samedi et dimanche)
            Do While Weekday(dateCourante) = 1 Or Weekday(dateCourante) = 7
                dateCourante = dateCourante + 1
            Loop
            
            ' Arrêtez lorsque la date atteint la fin du mois
            If dateCourante > dateFin Then
                Exit For
            End If
            
            ws.Cells(1, i).Value = Format(dateCourante, "dd/mm/yyyy")
            dateCourante = dateCourante + 1
        Next i
    Else
        MsgBox "Format de date incorrect. Veuillez utiliser le format mm/yyyy.", vbExclamation
    End If
End Sub

Sub CopierValeurs()

    ' Déclaration des variables
    Dim wsDest As Worksheet
    Dim wsSource As Worksheet
    Dim fichierSource As String
    Dim titreCokpit As String
    Dim dateCible As Date
    Dim valeurCokpit As Double
    Dim lastColumn As Integer
    Dim lastRow As Integer
    
    ' Définir la feuille de destination
    Set wsDest = ThisWorkbook.Sheets("FeuilleDestination")
    
    ' Boucler à travers les dates dans la première ligne du tableau de destination
    For Each cel In wsDest.Range("C1:ZZ1")
        If IsDate(cel.Value) Then
            ' Récupérer la date cible
            dateCible = cel.Value
            
            ' Boucler à travers les fichiers sources
            fichierSource = "Cokpit_BASE" & Format(dateCible, "yyyymmdd")
            Set wsSource = Workbooks.Open("CheminDuDossier\" & fichierSource & ".xlsx").Sheets(1) ' Modifier le chemin selon vos besoins
            
            ' Trouver la colonne correspondante au titre du cokpit dans le fichier source
            lastColumn = wsSource.Cells(1, wsSource.Columns.Count).End(xlToLeft).Column
            colTitre = Application.Match("Titre cokpit", wsSource.Rows(1), 0)
            
            ' Trouver la ligne correspondante au titre dans le fichier source
            lastRow = wsSource.Cells(wsSource.Rows.Count, colTitre).End(xlUp).Row
            ligneTitre = Application.Match(wsDest.Cells(1, cel.Column).Value, wsSource.Range(wsSource.Cells(1, colTitre), wsSource.Cells(lastRow, colTitre)), 0)
            
            ' Copier la valeur du cokpit dans le fichier destination
            valeurCokpit = wsSource.Cells(ligneTitre, colTitre + 5).Value ' Colonne G dans l'exemple
            
            wsDest.Cells(2, cel.Column).Value = valeurCokpit
            
            ' Fermer le fichier source
            Workbooks(fichierSource).Close SaveChanges:=False
        End If
    Next cel

End Sub

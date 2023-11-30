Sub MiseAJourDonnees()
    Dim ws As Worksheet
    Dim col As Range
    Dim currentDate As Date
    Dim sourceFilePath As String
    Dim rowCountBloquant As Long
    Dim rowCountImportant As Long
    
    ' Obtenez la feuille de calcul active (vous pouvez également spécifier une feuille spécifique)
    Set ws = ActiveSheet

    ' Boucle sur les colonnes de la première ligne (E à AA)
    For Each col In ws.Range("E:AA").Columns
        ' Récupère la date de la colonne actuelle
        currentDate = ws.Cells(1, col.Column).Value
        
        ' Génère le nom de fichier source
        sourceFilePath = "Chemin\vers\votre\dossier\" & "NomDuFichier_" & Format(currentDate, "YYYYMMDD") & ".xlsx"

        ' Vérifie si le fichier source existe
        If FileExists(sourceFilePath) Then
            ' Ouvre le fichier source
            Workbooks.Open sourceFilePath

            ' Applique un filtre dans la colonne AE pour sélectionner tous sauf 'Pas intervention'
            ws.Columns("AE").AutoFilter Field:=1, Criteria1:="<>Pas intervention"

            ' Compte le nombre de lignes Bloquantes et importantes dans la colonne A
            rowCountBloquant = Application.WorksheetFunction.CountIf(ws.Columns("A"), "Bloquant")
            rowCountImportant = Application.WorksheetFunction.CountIf(ws.Columns("A"), "Important")

            ' Ferme le fichier source sans sauvegarder les modifications
            ActiveWorkbook.Close False

            ' Met à jour les données sur la feuille principale
            ws.Cells(29, col.Column).Value = rowCountBloquant
            ws.Cells(30, col.Column).Value = rowCountImportant
        Else
            ' Affiche un message d'avertissement si le fichier source n'est pas trouvé
            MsgBox "Le fichier source pour la date " & Format(currentDate, "YYYYMMDD") & " n'a pas été trouvé.", vbExclamation
        End If
    Next col
End Sub

Function FileExists(filePath As String) As Boolean
    ' Vérifie si le fichier existe
    On Error Resume Next
    FileExists = (Len(Dir(filePath)) > 0)
    On Error GoTo 0
End Function

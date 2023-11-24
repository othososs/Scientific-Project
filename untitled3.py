Sub RemplirValeurs()

    Dim ws As Worksheet
    Dim dateCell As Range
    Dim folderPath As String, monthFolder As String
    Dim fileName As String
    Dim lastRow As Long
    Dim rowCount As Long
    
    ' Référence à la feuille de calcul
    Set ws = ThisWorkbook.Sheets("NomDeVotreFeuille")

    ' Chemin du dossier racine
    folderPath = "C:\Dossier\down\"

    ' Parcourir les cellules de la ligne 1 de E à AA
    For Each dateCell In ws.Range("E1:AA1")
        ' Convertir la date en format "mm - Mois"
        monthFolder = Format(dateCell.Value, "mm - Mmmm")
        
        ' Construire le chemin complet du dossier
        folderPath = folderPath & monthFolder & "\"

        ' Parcourir les fichiers dans le dossier
        fileName = Dir(folderPath & "COU2 Places - Circuit du " & Format(dateCell.Value, "ddmmyy") & ".xls")
        
        ' Vérifier si le fichier existe
        If Len(fileName) > 0 Then
            ' Ouvrir le classeur de travail
            Workbooks.Open (folderPath & fileName)
            
            ' Trouver le nombre de lignes dans la colonne X, à partir de la ligne 3
            lastRow = Cells(Rows.Count, "X").End(xlUp).Row
            ' Filtrer et compter les lignes sans "Pas intervention"
            rowCount = Application.WorksheetFunction.CountIfs(ws.Range("X3:X" & lastRow), "<>Pas intervention")
            
            ' Fermer le classeur de travail
            ActiveWorkbook.Close
            
            ' Mettre la valeur dans la cellule correspondante sur la feuille d'origine
            ws.Cells(28, dateCell.Column).Value = rowCount
        Else
            ' Si le fichier n'existe pas, afficher un message d'erreur
            MsgBox "Le fichier pour la date " & Format(dateCell.Value, "dd/mm/yyyy") & " n'a pas été trouvé.", vbExclamation
        End If
        
        ' Réinitialiser le chemin du dossier racine pour la prochaine itération
        folderPath = "C:\Dossier\down\"
    Next dateCell

End Sub

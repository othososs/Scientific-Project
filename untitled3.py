Sub MettreAJourFichierExcel()
    Dim wbDestination As Workbook
    Dim wsDestination As Worksheet
    Dim dateCell As Range
    Dim sourceFilePath As String
    Dim sourceFileName As String
    Dim destinationDate As Date
    Dim sourceDate As Date
    Dim matchRow As Variant
    
    ' Ouvrir le fichier destination
    Set wbDestination = ThisWorkbook ' Le classeur actif
    ' Remplacez "Feuil1" par le nom de votre feuille de destination
    Set wsDestination = wbDestination.Sheets("Feuil1")
    
    ' Parcourir les dates dans les colonnes E à Z de la première ligne
    For Each dateCell In wsDestination.Range("E1:Z1")
        destinationDate = dateCell.Value
        
        ' Construire le nom du fichier source en fonction de la date
        sourceFileName = "Cokpit_BASE" & Format(destinationDate, "YYYYMMDD")
        ' Construire le chemin complet du fichier source
        sourceFilePath = ThisWorkbook.Path & "\" & sourceFileName & ".xlsx"
        
        ' Vérifier si le fichier source existe
        If Dir(sourceFilePath) <> "" Then
            ' Ouvrir le fichier source
            Dim wbSource As Workbook
            Set wbSource = Workbooks.Open(sourceFilePath)
            
            ' Parcourir les valeurs de colonne C dans le fichier destination
            For Each cell In wsDestination.Range("C2:C" & wsDestination.Cells(wsDestination.Rows.Count, "C").End(xlUp).Row)
                ' Récupérer la date correspondante dans la ligne actuelle du fichier destination
                sourceDate = wsDestination.Cells(cell.Row, dateCell.Column).Value
                
                ' Comparer les dates
                If destinationDate = sourceDate Then
                    ' Trouver la ligne correspondante dans le fichier source
                    matchRow = Application.Match(cell.Value, wbSource.Sheets(1).Range("C:C"), 0)
                    
                    ' Vérifier si une correspondance a été trouvée
                    If Not IsError(matchRow) Then
                        ' Récupérer la valeur de la colonne G dans le fichier source
                        wsDestination.Cells(cell.Row, dateCell.Column).Value = wbSource.Sheets(1).Cells(matchRow, 7).Value
                    End If
                End If
            Next cell
            
            ' Fermer le fichier source
            wbSource.Close SaveChanges:=False
        Else
            ' Afficher un message si le fichier source est introuvable
            MsgBox "Le fichier source '" & sourceFilePath & "' n'existe pas."
        End If
    Next dateCell
    
    ' Enregistrer le fichier destination
    wbDestination.Save
End Sub

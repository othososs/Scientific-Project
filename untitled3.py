Sub MettreAJourFichierDestination()
    Dim wbDestination As Workbook
    Dim wsDestination As Worksheet
    Dim wbSource As Workbook
    Dim wsSource As Worksheet
    Dim cell As Range
    Dim dateCell As Range
    Dim sourceDateCell As Range
    Dim sourceFilePath As String
    Dim sourceFileName As String
    Dim destinationDate As Date
    Dim sourceDate As Date
    Dim matchRow As Long
    
    ' Ouvrir le fichier destination
    Set wbDestination = Workbooks.Open("chemin_vers_votre_fichier_destination.xlsx")
    ' Remplacez "Feuil1" par le nom de votre feuille de destination
    Set wsDestination = wbDestination.Sheets("Feuil1")
    
    ' Parcourir les dates dans les colonnes E à Z de la feuille de destination
    For Each dateCell In wsDestination.Range("E1:Z1")
        destinationDate = dateCell.Value
        
        ' Construire le nom du fichier source en fonction de la date
        sourceFileName = "Cokpit_BASE" & Format(destinationDate, "YYYYMMDD")
        ' Construire le chemin complet du fichier source
        sourceFilePath = "chemin_vers_votre_repertoire_source\" & sourceFileName & ".xlsx"
        
        ' Ouvrir le fichier source
        Set wbSource = Workbooks.Open(sourceFilePath)
        ' Remplacez "Feuil1" par le nom de votre feuille source
        Set wsSource = wbSource.Sheets("Feuil1")
        
        ' Parcourir les valeurs de colonne C dans le fichier destination
        For Each cell In wsDestination.Range("C2:C" & wsDestination.Cells(wsDestination.Rows.Count, "C").End(xlUp).Row)
            ' Récupérer la date correspondante dans la ligne actuelle
            sourceDate = wsSource.Cells(cell.Row, 5).Value
            
            ' Comparer les dates
            If destinationDate = sourceDate Then
                ' Trouver la ligne correspondante dans le fichier source
                matchRow = Application.Match(cell.Value, wsSource.Range("C:C"), 0)
                
                ' Vérifier si une correspondance a été trouvée
                If Not IsError(matchRow) Then
                    ' Récupérer la valeur de la colonne G dans le fichier source
                    wsDestination.Cells(cell.Row, dateCell.Column).Value = wsSource.Cells(matchRow, 7).Value
                End If
            End If
        Next cell
        
        ' Fermer le fichier source
        wbSource.Close SaveChanges:=False
    Next dateCell
    
    ' Fermer le fichier destination
    wbDestination.Close SaveChanges:=True
End Sub

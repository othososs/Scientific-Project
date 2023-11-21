Sub RechercherValeurs()

    Dim wsSource As Worksheet
    Dim wsDest As Worksheet
    Dim sourcePath As String
    Dim sourceFile As String
    Dim currentDate As String
    Dim lastRowSource As Long
    Dim lastRowDest As Long
    Dim i As Long, j As Long
    Dim found As Boolean
    
    ' Spécifiez le chemin du répertoire source
    sourcePath = "C:\Votre\Chemin\Vers\Les\Fichiers\"
    
    ' Obtenez la date actuelle au format YYYYMMDD
    currentDate = Format(Date, "YYYYMMDD")
    
    ' Spécifiez le nom du fichier source en fonction de la date
    sourceFile = "Cokpit_BASE" & currentDate & ".xlsx"
    
    ' Définissez la feuille de calcul source
    Set wsSource = Workbooks.Open(sourcePath & sourceFile).Worksheets(1)
    
    ' Définissez la feuille de calcul de destination (le fichier où vous avez votre tableau)
    Set wsDest = ThisWorkbook.Worksheets("NomDeVotreFeuille")
    
    ' Trouvez la dernière ligne avec des données dans la feuille source
    lastRowSource = wsSource.Cells(wsSource.Rows.Count, "C").End(xlUp).Row
    
    ' Trouvez la dernière ligne avec des données dans la feuille de destination
    lastRowDest = wsDest.Cells(wsDest.Rows.Count, "B").End(xlUp).Row
    
    ' Bouclez à travers chaque ligne dans la feuille de destination
    For i = 2 To lastRowDest ' Assurez-vous que la première ligne contient des en-têtes
        
        ' Réinitialisez le marqueur de "trouvé" pour chaque itération
        found = False
        
        ' Bouclez à travers chaque ligne dans la feuille source
        For j = 2 To lastRowSource ' Assurez-vous que la première ligne contient des en-têtes
            
            ' Vérifiez si le titre de la feuille de destination correspond au titre de la feuille source
            If wsDest.Cells(i, 2).Value = wsSource.Cells(j, 3).Value Then
                
                ' Copiez la valeur correspondante de la colonne G de la feuille source
                wsDest.Cells(i, 3).Value = wsSource.Cells(j, 7).Value
                
                ' Marquez comme "trouvé"
                found = True
                
                ' Sortez de la boucle interne une fois que la correspondance est trouvée
                Exit For
            End If
        Next j
        
        ' Si la correspondance n'est pas trouvée, vous pouvez ajouter un traitement supplémentaire ici si nécessaire
        
    Next i
    
    ' Fermez le classeur source
    Workbooks(sourceFile).Close SaveChanges:=False
    
End Sub

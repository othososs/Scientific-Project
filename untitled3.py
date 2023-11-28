Sub TraitementDonnees()

    ' Déclaration des variables
    Dim ws As Worksheet
    Dim cheminRepertoire As String
    Dim dossierMois As String
    Dim fichier As String
    Dim dateFichier As Date
    Dim wb As Workbook
    Dim wsFichier As Worksheet
    Dim lastRow As Long
    Dim bloquants As Long
    Dim importants As Long
    
    ' Référence à la feuille de travail actuelle
    Set ws = ThisWorkbook.Sheets("VotreFeuille")
    
    ' Récupérer les dates dans la plage E1:AA1
    For Each cell In ws.Range("E1:AA1")
        If IsDate(cell.Value) Then
            ' Récupérer la date
            dateFichier = cell.Value
            
            ' Construire le chemin du répertoire
            cheminRepertoire = "C:\Votre\Chemin\Repertoire\" ' Mettez votre chemin de répertoire ici
            dossierMois = Format(dateFichier, "mm-mmmm")
            cheminRepertoire = cheminRepertoire & dossierMois & "\"
            
            ' Ouvrir le classeur dans le répertoire
            fichier = Dir(cheminRepertoire & "ecacouQP_D" & Format(dateFichier, "yymmdd") & "*.xlsx")
            
            Do While fichier <> ""
                ' Ouvrir le classeur
                Set wb = Workbooks.Open(cheminRepertoire & fichier)
                
                ' Utiliser la première feuille du classeur ouvert
                Set wsFichier = wb.Sheets(1)
                
                ' Filtrer la colonne AE
                wsFichier.AutoFilterMode = False ' Supprimer les filtres existants
                wsFichier.Range("AE:AE").AutoFilter Field:=1, Criteria1:="<>Pas d'intervention auto"
                
                ' Compter le nombre de lignes Bloquants et Importants
                bloquants = Application.WorksheetFunction.CountIf(wsFichier.Range("A:A"), "Bloquant")
                importants = Application.WorksheetFunction.CountIf(wsFichier.Range("A:A"), "Important")
                
                ' Fermer le classeur sans sauvegarder les modifications
                wb.Close SaveChanges:=False
                
                ' Mettre à jour les données sur la feuille principale
                ws.Cells(29, ws.Columns(dateFichier).Column).Value = bloquants
                ws.Cells(30, ws.Columns(dateFichier).Column).Value = importants
                
                ' Trouver le prochain fichier
                fichier = Dir
            Loop
        End If
    Next cell

End Sub

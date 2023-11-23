Sub MettreAJourFichier()

    Dim ws As Worksheet
    Dim col As Range
    Dim cell As Range
    Dim dateCell As Range
    Dim sourceFileName As String
    Dim sourceFilePath As String
    Dim sourceWorkbook As Workbook
    Dim sourceWS As Worksheet
    Dim titre As String
    Dim correspondance As Variant
    Dim i As Long

    ' Spécifiez ici la feuille de calcul que vous utilisez
    Set ws = ThisWorkbook.Sheets("NomDeVotreFeuille")

    ' Spécifiez ici la plage de colonnes E à Z
    Set col = ws.Range("E1:Z1")

    ' Boucle sur les colonnes de la première ligne
    For Each dateCell In col
        ' Générer le nom du fichier source en fonction de la date
        sourceFileName = "Cokpit_BASE" & Format(dateCell.Value, "YYYYMMDD")
        
        ' Spécifiez ici le chemin du répertoire où se trouvent les fichiers source
        sourceFilePath = "C:\Chemin\Vers\Votre\Repertoire\" & sourceFileName & ".xlsx"

        ' Vérifier si le fichier source existe
        If Dir(sourceFilePath) <> "" Then
            ' Ouvrir le fichier source
            Set sourceWorkbook = Workbooks.Open(sourceFilePath)
            Set sourceWS = sourceWorkbook.Sheets(1)

            ' Initialisation de la boucle (commence à la deuxième ligne et se termine à la ligne 35)
            For i = 2 To 35
                ' Récupération du titre dans la colonne C
                titre = ws.Cells(i, 3).Value

                ' Recherche de correspondance dans le fichier source
                correspondance = Application.Match(titre, sourceWS.Columns(3), 0)

                ' Gestion des correspondances
                If Not IsError(correspondance) Then
                    ' Correspondance trouvée, extraire la valeur de la colonne G dans le fichier source
                    ws.Cells(i, dateCell.Column).Value = sourceWS.Cells(correspondance, 7).Value
                End If
            Next i

            ' Fermer le fichier source
            sourceWorkbook.Close SaveChanges:=False
        Else
            ' Afficher un message si le fichier source n'est pas trouvé
            MsgBox "Le fichier source " & sourceFileName & " n'a pas été trouvé.", vbExclamation
        End If
    Next dateCell

End Sub

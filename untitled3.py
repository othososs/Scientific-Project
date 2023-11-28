Sub MiseAJourFichiers()
    Dim ws As Worksheet
    Dim col As Range
    Dim dateCol As Range
    Dim sourceFilePath As String
    Dim currentDate As Date
    Dim sumValue As Double
    
    ' Spécifiez ici le répertoire où se trouvent vos fichiers sources
    Const sourceDirectory As String = "C:\CheminetDeVotreDossier\"

    ' Spécifiez ici la ligne où se trouvent les dates et la ligne où vous souhaitez placer les sommes
    Const datesRow As Integer = 1
    Const sumRow As Integer = 18

    ' Obtenez la feuille de calcul active (vous pouvez également spécifier une feuille spécifique)
    Set ws = ActiveSheet

    ' Boucle sur les colonnes de la première ligne (E à AA)
    For Each col In ws.Range("E:AA").Columns
        ' Récupère la date de la colonne actuelle
        currentDate = ws.Cells(datesRow, col.Column).Value

        ' Génère le nom de fichier source
        sourceFilePath = sourceDirectory & "Cokpit_BASE" & Format(currentDate, "YYYYMMDD") & ".xlsx"

        ' Vérifie si le fichier source existe
        If Dir(sourceFilePath) <> "" Then
            ' Ouvre le fichier source
            Workbooks.Open sourceFilePath

            ' Fait la somme des lignes 10 à 12 de la colonne G
            sumValue = Application.WorksheetFunction.Sum(Range("G10:G12"))

            ' Place la somme dans le fichier d'origine à la colonne de la date correspondante et à la ligne 18
            ws.Cells(sumRow, col.Column).Value = sumValue

            ' Ferme le fichier source sans sauvegarder les modifications
            ActiveWorkbook.Close False
        Else
            ' Affiche un message d'avertissement si le fichier source n'est pas trouvé
            MsgBox "Le fichier source pour la date " & Format(currentDate, "YYYYMMDD") & " n'a pas été trouvé.", vbExclamation
        End If
    Next col
End Sub

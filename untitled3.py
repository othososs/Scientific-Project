Sub RemplirFichierDestination()
    Dim wsDest As Worksheet
    Dim wsSource As Worksheet
    Dim dateCible As Date
    Dim titreCokpit As String
    Dim valeurCokpit As Variant
    Dim colTitreDest As Long
    Dim colTitreSource As Long
    Dim i As Long, lastRowDest As Long
    Dim fichierSource As String

    ' Définir la feuille de destination
    Set wsDest = ThisWorkbook.Sheets("FeuilleDestination")

    ' Déterminer la dernière ligne dans la feuille de destination
    lastRowDest = wsDest.Cells(wsDest.Rows.Count, 1).End(xlUp).Row

    ' Boucler à travers les colonnes de dates dans la première ligne du tableau de destination
    For i = 4 To wsDest.Cells(1, wsDest.Columns.Count).End(xlToLeft).Column
        ' Récupérer la date cible
        dateCible = wsDest.Cells(1, i).Value

        ' Générer le nom du fichier source basé sur la date
        fichierSource = "Cokpit_BASE" & Format(dateCible, "yyyymmdd") & ".xlsx"

        ' Vérifier si le fichier source existe
        If Dir(fichierSource) <> "" Then
            ' Ouvrir le fichier source correspondant
            Set wsSource = Workbooks.Open(fichierSource).Sheets(1)

            ' Trouver la colonne correspondante au titre du cockpit dans le fichier source
            colTitreSource = Application.Match("Titre cockpit", wsSource.Rows(1), 0)

            ' Boucler à travers les lignes dans le fichier de destination
            For j = 2 To lastRowDest
                ' Récupérer le titre du cockpit à partir du fichier de destination
                titreCokpit = wsDest.Cells(j, 2).Value

                ' Trouver la ligne correspondante au titre dans le fichier source
                ligneTitreSource = Application.Match(titreCokpit, wsSource.Range(wsSource.Cells(1, colTitreSource), wsSource.Cells(wsSource.Rows.Count, colTitreSource).End(xlUp)), 0)

                ' Copier la valeur du cockpit dans le fichier destination
                If Not IsError(ligneTitreSource) Then
                    valeurCokpit = wsSource.Cells(ligneTitreSource, colTitreSource + 5).Value ' Colonne G dans l'exemple
                    wsDest.Cells(j, i).Value = valeurCokpit
                End If
            Next j

            ' Fermer le fichier source
            wsSource.Parent.Close SaveChanges:=False
        End If
    Next i
End Sub

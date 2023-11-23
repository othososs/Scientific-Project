Sub RemplirFichierDestination()
    Dim wsDest As Worksheet
    Dim wsSource As Worksheet
    Dim dateCible As Date
    Dim titreCokpit As String
    Dim valeurCokpit As Variant
    Dim colTitreSource As Long
    Dim i As Long, lastRowDest As Long

    ' Définir la feuille de destination
    Set wsDest = ThisWorkbook.Sheets("FeuilleDestination")

    ' Déterminer la dernière ligne dans la feuille de destination
    lastRowDest = wsDest.Cells(wsDest.Rows.Count, 1).End(xlUp).Row

    ' Boucler à travers les colonnes de dates dans la première ligne du tableau de destination
    For i = 4 To wsDest.Cells(1, wsDest.Columns.Count).End(xlToLeft).Column
        ' Récupérer la date cible
        dateCible = wsDest.Cells(1, i).Value

        ' Boucler à travers les lignes dans le fichier de destination
        For j = 2 To lastRowDest
            ' Récupérer le titre du cockpit à partir du fichier de destination
            titreCokpit = wsDest.Cells(j, 2).Value

            ' Ouvrir le fichier source correspondant
            Set wsSource = Workbooks.Open("Cokpit_BASE" & Format(dateCible, "yyyymmdd") & ".xlsx").Sheets(1)

            ' Trouver la ligne correspondante au titre dans le fichier source
            ligneTitreSource = Application.Match(titreCokpit, wsSource.Columns("C"), 0)

            ' Copier la valeur du cockpit dans le fichier destination
            If Not IsError(ligneTitreSource) Then
                valeurCokpit = wsSource.Cells(ligneTitreSource, 7).Value ' Colonne G dans le fichier source
                wsDest.Cells(j, i).Value = valeurCokpit
            End If

            ' Fermer le fichier source
            wsSource.Parent.Close SaveChanges:=False
        Next j
    Next i
End Sub

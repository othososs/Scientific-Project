Sub FiltrerEtCompter()
    Dim sourceWorkbook As Workbook
    Dim sourceWorksheet As Worksheet
    Dim lastRow As Long
    Dim countAControler As Long

    ' Assurez-vous que le classeur est ouvert ou ouvrez-le
    Set sourceWorkbook = Workbooks("SourceWorkbook.xlsx")

    ' Spécifiez la feuille de calcul à l'intérieur du classeur
    Set sourceWorksheet = sourceWorkbook.Sheets("NomDeVotreFeuille")

    ' Obtenez la dernière ligne dans la colonne E de cette feuille
    lastRow = sourceWorksheet.Cells(sourceWorksheet.Rows.Count, "E").End(xlUp).Row

    ' Appliquer le filtre
    sourceWorksheet.Range("E1:E" & lastRow).AutoFilter Field:=1, Criteria1:="A controler"

    ' Compter le nombre de lignes filtrées
    countAControler = sourceWorksheet.AutoFilter.Range.Columns(1).SpecialCells(xlCellTypeVisible).Cells.Count - 1

    ' Afficher le résultat
    MsgBox "Nombre de lignes à contrôler : " & countAControler

    ' Supprimer le filtre
    sourceWorksheet.AutoFilterMode = False
End Sub

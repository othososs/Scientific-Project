Sub CalculateMetrics()
    Dim ws As Worksheet
    Dim weekInput As String
    Dim weekCol As Long
    Dim i As Long
    Dim meanLast3Weeks As Double
    Dim lastWeekValue As Double
    Dim previousWeekValue As Double
    Dim variationComparedMean As Double
    Dim lastWeek As String
    
    ' Set worksheet
    Set ws = ThisWorkbook.Sheets("Feuil1")
    
    ' Get the input for the week
    weekInput = InputBox("Enter the date for the week (dd/mm/yyyy):")
    
    ' Find the column for the input week
    On Error Resume Next
    weekCol = ws.Rows(1).Find(What:=weekInput, LookIn:=xlValues, LookAt:=xlWhole).Column
    On Error GoTo 0
    
    If weekCol = 0 Then
        MsgBox "The entered week is not found in the data range. Please check the date format and try again.", vbExclamation
        Exit Sub
    End If
    
    ' Get the actual date for the last week (input week)
    lastWeek = ws.Cells(1, weekCol).Value
    
    ' Loop through each variable (rows 2 to 6 in the input section, rows 12 to 16 in the output section)
    For i = 2 To 6
        ' Calculate mean of last 3 weeks
        meanLast3Weeks = Application.WorksheetFunction.Average(ws.Cells(i, weekCol - 2), ws.Cells(i, weekCol - 1), ws.Cells(i, weekCol))
        
        ' Get last week value
        lastWeekValue = ws.Cells(i, weekCol).Value
        
        ' Get previous week value
        previousWeekValue = ws.Cells(i, weekCol - 1).Value
        
        ' Calculate variation compared to mean of last 3 weeks
        variationComparedMean = (lastWeekValue - meanLast3Weeks) / meanLast3Weeks
        
        ' Fill in the output sheet
        ws.Cells(i + 10, 2).Value = meanLast3Weeks
        ws.Cells(i + 10, 3).Value = lastWeekValue - previousWeekValue
        ws.Cells(i + 10, 4).Value = variationComparedMean
    Next i
    
    ' Fill in the last week date in the output sheet
    ws.Cells(11, 1).Value = "Last Week"
    ws.Cells(12, 1).Value = lastWeek
End Sub

Function MoisEnFrancais(dateValue As Date) As String
    Dim mois As String
    mois = Format(dateValue, "mmmm")
    
    Select Case mois
        Case "January": MoisEnFrancais = "Janvier"
        Case "February": MoisEnFrancais = "Février"
        Case "March": MoisEnFrancais = "Mars"
        Case "April": MoisEnFrancais = "Avril"
        Case "May": MoisEnFrancais = "Mai"
        Case "June": MoisEnFrancais = "Juin"
        Case "July": MoisEnFrancais = "Juillet"
        Case "August": MoisEnFrancais = "Août"
        Case "September": MoisEnFrancais = "Septembre"
        Case "October": MoisEnFrancais = "Octobre"
        Case "November": MoisEnFrancais = "Novembre"
        Case "December": MoisEnFrancais = "Décembre"
        Case Else: MoisEnFrancais = mois
    End Select
End Function

Option Explicit

Sub RecupererValeurs()

    Dim wbSource As Workbook
    Dim wsSource As Worksheet
    Dim wsDestination As Worksheet
    Dim cheminDossier As String
    Dim fichier As String
    Dim dateChoisie As Date
    Dim dernierLigneSource As Long
    Dim i As Long
    
    ' Définir le dossier source
    cheminDossier = "V:\Dossier\ABC\"
    
    ' Sélectionner la date
    dateChoisie = Application.InputBox("Choisissez une date", Type:=1)
    
    ' Construire le nom du fichier en fonction de la date choisie
    fichier = "Cokpit_BASE" & Format(dateChoisie, "yyyymmdd") & ".xlsx"
    
    ' Ouvrir le fichier source
    Set wbSource = Workbooks.Open(cheminDossier & fichier)
    Set wsSource = wbSource.Sheets(1) ' Supposons que les données sont dans la première feuille
    
    ' Référence à la feuille de destination (où se trouve le tableau avec Titre, Valeur, Source)
    Set wsDestination = ThisWorkbook.Sheets("Feuille1") ' Remplace "Feuille1" par le nom réel de ta feuille
    
    ' Trouver la dernière ligne avec des données dans la feuille source
    dernierLigneSource = wsDestination.Cells(wsDestination.Rows.Count, "A").End(xlUp).Row
    
    ' Parcourir les lignes du tableau dans la feuille destination
    For i = 2 To dernierLigneSource ' On suppose que la première ligne contient des en-têtes
        
        ' Trouver la valeur correspondante dans le fichier source
        Dim titre As String
        Dim valeur As Variant
        
        titre = wsDestination.Cells(i, 1).Value ' Colonne A
        valeur = Application.VLookup(titre, wsSource.Range("C:G"), 4, False) ' Colonne G
        
        ' Mettre à jour la valeur dans la feuille destination
        If Not IsError(valeur) Then
            wsDestination.Cells(i, 2).Value = valeur
        Else
            wsDestination.Cells(i, 2).Value = "Non trouvé"
        End If
        
    Next i
    
    ' Fermer le fichier source
    wbSource.Close SaveChanges:=False

End Sub

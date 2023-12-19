Sub SauvegarderFeuille()
    Dim chemin As String
    Dim nomFichier As String
    
    ' Spécifiez le chemin du répertoire où vous souhaitez sauvegarder la feuille
    chemin = "C:\Chemin\vers\le\répertoire\"
    
    ' Spécifiez le nom du fichier
    nomFichier = "NomDuFichier.xlsx"
    
    ' Vérifiez si le répertoire existe, sinon créez-le
    If Dir(chemin, vbDirectory) = "" Then
        MkDir chemin
    End If
    
    ' Sauvegarde de la feuille dans le répertoire spécifié avec le nom spécifié
    ThisWorkbook.SaveAs chemin & nomFichier
    
    ' Affiche un message indiquant que la sauvegarde a été effectuée avec succès
    MsgBox "Feuille sauvegardée avec succès dans : " & chemin & nomFichier, vbInformation
End Sub

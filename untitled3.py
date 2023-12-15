VotreMesure =
VAR TotalCol24 =
    CALCULATE(
        SUMX(
            FILTER(
                'NomDeVotreTable',
                'NomDeVotreTable'[Colonne95] = "FR34" ||
                'NomDeVotreTable'[Colonne95] = "FR53" ||
                'NomDeVotreTable'[Colonne95] = "FR134" ||
                'NomDeVotreTable'[Colonne95] = "FR64"
            ),
            'NomDeVotreTable'[Colonne24]
        )
    )

VAR ValeurCol5 = VALUES('NomDeVotreTable'[Colonne5])

RETURN
DIVIDE(TotalCol24, ValeurCol5)

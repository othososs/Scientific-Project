=IF(AND(D23="Good (green)"; D24="Good (green)"); "Good (green)"; IF(AND(D23="Mixed (orange)"; D24="Mixed (orange)"); "Mixed (orange)"; IF(AND(D23="Bad (red)"; D24="Bad (red)"); "Bad (red)"; IF(OR(AND(D23="Good (green)"; D24="Mixed (orange)"); AND(D23="Mixed (orange)"; D24="Good (green)")); "Mixed (orange)"; "Bad (red)"))))

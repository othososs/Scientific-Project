=IF(AND(D23="Good (green)"; D24="Good (green)"); "Good (green)"; IF(AND(OR(D23="Good (green)"; D23="Mixed (orange)"); OR(D24="Good (green)"; D24="Mixed (orange)")); "Mixed (orange)"; IF(AND(D23="Bad (red)"; D24="Bad (red)"); "Bad (red)"; "Other")))

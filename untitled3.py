=IF(AND(NOT(ISBLANK(E23)), ISBLANK(E24)), E23&":OPC/", IF(AND(ISBLANK(E23), NOT(ISBLANK(E24))), E24&":Custody", IF(AND(NOT(ISBLANK(E23)), NOT(ISBLANK(E24))), E23&":OPC/"&E24&":Custody", "")))

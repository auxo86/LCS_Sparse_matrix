from algorism import fxStrSimilarity

strCharForEliminated = ' ()[]{}!@#$^&*_-+/\'\"\t\r\n'
# listScoreAndCS = fxStrSimilarity('abcbcdgz', 'abcdgz', strCharForEliminated)
# listScoreAndCS = fxStrSimilarity('!marcaine 0.5% spinal 4ML INJ      ', 'MARCAINE (R) SPINAL 0.5% HEAVY_中國化學製藥股份有限公司_ASTRA PHARMACEUTICALS. INTERNATIONAL AB (AB A STRA)', strCharForEliminated)
# listScoreAndCS = fxStrSimilarity('!marcaine 0.5% 20ML INJ', 'LIGNOCAINE 2% CHLORHEXIDINE 0.05% GEL,10ML SYRINGE_鴻晟實業有限公司_PHARMACIA (PERTH) PTY LIMITED', strCharForEliminated)
listScoreAndCS = fxStrSimilarity('!ketalar 500mg 10ml inj #3           ', 'KETALAR INJECTION 50MG/ML_輝瑞大藥廠股份有限公司_聯亞藥業股份有限公司新竹廠', strCharForEliminated)

print(listScoreAndCS)

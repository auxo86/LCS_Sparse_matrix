def fxStrSimilarity(str1, str2, strCharForEliminated):
    listStrings = [str1, str2]
    # 縱橫軸匹配到的禁區做list
    listXAxisRestrictedZone = []
    listYAxisRestrictedZone = []
    # 定義回傳相似度list
    listResult = []
    # 定義比對到的字串
    strCS = ''
    # 幫字串去前後空白，並且轉小寫，再去掉點，例如40i.u. -> 40iu
    for itemIDX in range(len(listStrings)):
        listStrings[itemIDX] = listStrings[itemIDX].strip().lower().replace('.', '')

    # 當前後元素不相等的時候就先去掉雜七雜八的字元還有空白，然後幫字段加上區隔符號
    if listStrings[0] != listStrings[1]:
        for stringIDX in range(len(listStrings)):
            for char in listStrings[stringIDX]:
                if char in strCharForEliminated:
                    listStrings[stringIDX] = listStrings[stringIDX].replace(char, '|')
        # 相似分數的分母是str1去掉空白和奇奇怪怪符號後剩下字串長度的平方
        numSimilarityScoreDenominator = len(listStrings[0]) ** 2
        # 相似分數的分子預設為0
        numSimilarityScoreNumerator = 0
        # 如果str1的長度大於str2，就交換。一定要把短的放在X軸
        if len(listStrings[0]) > len(listStrings[1]):
            strTemp = listStrings[0]
            listStrings[0] = listStrings[1]
            listStrings[1] = strTemp
        # 前置處理完比對的字串後，判斷分母是否為0，也就是沒有要比對的藥品名稱
        # 如果沒有藥名，直接回傳 listResult = [0, '']
        if len(listStrings[0]) == 0:
            listResult = [0, '']
            return listResult

        coordinateCommonChar = {'x': None, 'y': None}
        # 相同字元構成的list
        listCommonChars = []
        # 先建立evaluation metrics，建立2-dimention時要注意python特有的深淺複製的問題
        listMetrics = [[0] * len(listStrings[0]) for i in range(len(listStrings[1]))]
        # 用雙層迴圈填入比對字元後的結果填入Metrics(相同為1，不同為0)
        for idxY in range(len(listStrings[1])):
            for idxX in range(len(listStrings[0])):
                if listStrings[0][idxX] == listStrings[1][idxY]:
                    listMetrics[idxY][idxX] = 1
                    coordinateCommonChar['x'] = idxX
                    coordinateCommonChar['y'] = idxY
                    # 紀錄矩陣中比對到相同字元的座標還有預留diff的欄位[dict(coordinateCommonChar), diff]
                    listCommonChars.append([dict(coordinateCommonChar), 0])
        # 幫listCommonChars中的每個元素產生diff
        listCommonChars = list(map(fxRowColDiff, listCommonChars))
        # 找出對角線，只要diff相同就是在同一個矩形內，如果這些元素的集合彼此間差1，那這就是一條對角線
        setOfDiagIDs = set(map(lambda cc: cc[1], listCommonChars))
        # 用來形成對角線，是一串連續字元的集合
        tempDiag = []
        # 是對角線的集合。
        listDiags = []
        # 當這些在同一個矩形對角線上的點有連續時設為同一條對角線。這些點形成的對角線不一定只有一條。
        for numDiagID in setOfDiagIDs:
            diagsPotential = list(filter(lambda CC: CC[1] == numDiagID, listCommonChars))
            if len(diagsPotential) < 2:
                continue
            # TODO:找出為什麼不同矩形的點會被串成同一條線
            for idxCC, CC in enumerate(diagsPotential):
                try:
                    if listStrings[0][CC[0]['x']] != '|' and diagsPotential[idxCC + 1][0]['x'] - CC[0]['x'] == 1:
                        # 往對角線加字元
                        tempDiag.append(CC)
                    # 遇到分隔符號，於是這個字元不加，中斷形成對角線
                    elif listStrings[0][CC[0]['x']] == '|':
                        if len(tempDiag) < 2:
                            tempDiag = []
                            continue
                        # 直接在對角線集合加對角線
                        listDiags.append(tempDiag)
                        # 因為後面字元還有所以把暫時對角線清空重來
                        tempDiag = []
                        continue
                    else:
                        # 跟下一個字元的x座標差距不是1，把這個字元加入對角線
                        tempDiag.append(CC)
                        # 把對角線加入對角線集合
                        if len(tempDiag) < 2:
                            tempDiag = []
                            continue
                        listDiags.append(tempDiag)
                        # 因為後面字元還有所以把暫時對角線清空重來
                        tempDiag = []
                # 走到對角線的最後一格
                except IndexError as e:
                    # 往對角線加字元
                    if listStrings[0][CC[0]['x']] == '|' and len(tempDiag) > 1:
                        # 對角線集合加線，然後應該迴圈結束產生完整的對角線集合
                        listDiags.append(tempDiag)
                        tempDiag = []
                    elif listStrings[0][CC[0]['x']] == '|' and len(tempDiag) < 1:
                        tempDiag = []
                    elif listStrings[0][CC[0]['x']] != '|':
                        tempDiag.append(CC)
                        if len(tempDiag) > 1:
                            listDiags.append(tempDiag)
                            tempDiag = []
                        else:
                            tempDiag = []
        # 跑到這裡表示已經蒐集了所有的對角線。
        while len(listDiags) > 0:
            # 去掉長度<=1的對角線
            listDiags = list(filter(lambda diag: len(diag) > 1, listDiags))
            # 如果已經沒有對角線了就跳出迴圈
            if len(listDiags) == 0:
                break
            # 找出最長的對角線
            TheLongestDiag = max(listDiags, key=lambda diag: len(diag))
            # 設定橫軸禁區
            listXAxisRestrictedZone += list(map(lambda chrInDiag: chrInDiag[0]['x'], TheLongestDiag))
            # 設定縱軸禁區
            listYAxisRestrictedZone += list(map(lambda chrInDiag: chrInDiag[0]['y'], TheLongestDiag))
            # 算分子並且記錄到有效對角線的strCS
            numSimilarityScoreNumerator += len(TheLongestDiag) ** 2
            strCS = strCS + listStrings[0][TheLongestDiag[0][0]['x']:TheLongestDiag[0][0]['x'] + len(TheLongestDiag)] + '|'
            listTmpDiags = []
            # 根據禁區裁切對角線
            for diag in listDiags:
                diag = list(filter(lambda chrInDiag: chrInDiag[0]['x'] not in listXAxisRestrictedZone, diag))
                # 處理完X軸處理Y軸
                diag = list(filter(lambda chrInDiag: chrInDiag[0]['y'] not in listYAxisRestrictedZone, diag))
                if len(diag) < 2:
                    continue
                listTmpDiags.append(diag)
            listDiags = listTmpDiags
        # 跑完比對迴圈後算分
        numSimilarityScore = numSimilarityScoreNumerator / numSimilarityScoreDenominator
    else:
        numSimilarityScore = 1
        strCS = listStrings[0] + '|'

    # 再加入結果之前先判斷到底對到什麼，如果什麼都沒有對到，就維持listStrCS為''；如果有對到，移除最後一個|
    if strCS != '':
        strCS = strCS[:-1]
    listResult = [numSimilarityScore, strCS]
    return listResult

def fxRowColDiff(CommChar):
    CommChar[1] = CommChar[0]['x'] - CommChar[0]['y']
    return CommChar
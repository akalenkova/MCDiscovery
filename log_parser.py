def parse(log, k):
    for i in range(0, len(log)):
        occur = {}
        for j in range(0,len(log[i])):
            if log[i][j]['concept:name'] in occur:
                if occur[log[i][j]['concept:name']] < k:
                    occur[log[i][j]['concept:name']] += 1
            else:
                occur[log[i][j]['concept:name']] = 1
            log[i][j]['concept:name'] = log[i][j]['concept:name'] + '_' + str(occur[log[i][j]['concept:name']])
    return log
    

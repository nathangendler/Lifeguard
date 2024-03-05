def main():
    events = ["USCALA3F1ALT1","USCALAA1M1","USCALAA1M0","USCALAA1M2"]
    ilt, m3 = findILT(events)
    print(f"ilt: {ilt}")
    print(f"m3: {m3}")

def findILT(events):
    EVENTORDER = ["LT", "M3", "M2", "M1", "M0"]


    #for i in range(len(data)):
        #if data[i]['stats'] is not None:
            #events.append(data[i]['eventCode'])
        #else:
            #events.append(None)

    # Correct the last two characters check
    for i in range(len(events)):
        if events[i] is not None and len(events[i]) >= 3 and events[i][-2] == "T" and events[i][-3] == "L":
            events[i] = "LT"
        else:
            events[i] = events[i][-2:] if events[i] is not None else None
    counter = 0
    ilt = 0
    m3 = 0
    # Iterate over EVENTORDER
    for i in range(len(EVENTORDER) - 1):
        if EVENTORDER[i] in events:
            z = EVENTORDER[i]
            for g in range(len(events)):
                if counter == 2:
                    return ilt, m3
                elif events[g] == z and counter == 0:
                    ilt = g
                    counter += 1
                elif events[g] == z and counter == 1:
                    m3 = g
                    counter += 1

if __name__ == "__main__":
    main()
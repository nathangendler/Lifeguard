def main():
    events = ["USCALA3F1ALT1", "USCALAA1M1","USCALACMP1","USCALAA1M0","USCALAA1M2"]
    champ = findChamps(events)
    print(f"index: {champ}")


def findChamps(data):

    EVENTORDER = ["MP","LT", "M3", "M2", "M1", "M0"]
    events = data

    for i in range(len(events)):
        if events[i] is not None and len(events[i]) >= 2 and events[i][-2] == "T" and events[i][-3] == "L":
            events[i] = "LT"
        elif events[i] is not None and len(events[i]) >= 2 and events[i][-2] == "P" and events[i][-3] == "M":
            events[i] = "MP"
        else:
            events[i] = events[i][-2:] if events[i] is not None else None

    print(events)

    for i in range(len(EVENTORDER) - 1):
        if EVENTORDER[i] in events:
            z = EVENTORDER[i]
            for g in range(len(events)):
                if events[g] == z:
                    return g

if __name__ == "__main__":
    main()
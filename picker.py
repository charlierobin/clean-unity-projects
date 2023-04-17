def picker(places, caption):

    done = False

    selected = []

    while not done and len(places) > 0:

        print("")

        number = 1

        for place in places:

            if selected.count(number - 1) == 0:
                print("   " + str(number) + ": " + str(place) + "   ")
            else:
                print(">  " + str(number) + ": " + str(place) + "  <")

            number = number + 1

        print("")

        command = input(
            "❓ " + caption + " (Enter a number or pattern or “*” (all), prefix “-” (minus) to deselect, 0 to finish) ")

        if command == "":
            continue

        if command == "0":
            break

        remove = False

        if command[0] == "-":
            remove = True
            command = command[1:]

        if command == "*":

            if remove:
                selected = []
            else:
                for x in range(len(places)):
                    if selected.count(x) == 0:
                        selected.append(x)

            continue

        if command.isnumeric():

            command = int(command)
            command = command - 1

            if command <= len(places):

                if remove:
                    if selected.count(command) > 0:
                        selected.remove(command)
                else:
                    if selected.count(command) == 0:
                        selected.append(command)
        else:

            if remove:

                for x in range(len(places)):

                    if command in places[x]:
                        if selected.count(x) > 0:
                            selected.remove(x)
            else:

                for x in range(len(places)):

                    if command in places[x]:
                        selected.append(x)

    return selected

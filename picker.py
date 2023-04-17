def picker(options, caption):

    done = False

    selected = []

    while not done and len(options) > 0:

        print("")

        number = 1

        for option in options:

            if selected.count(number - 1) == 0:
                print("   " + str(number) + ": " + str(option) + "   ")
            else:
                print(">  " + str(number) + ": " + str(option) + "  <")

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
                for x in range(len(options)):
                    if selected.count(x) == 0:
                        selected.append(x)

            continue

        if command.isnumeric():

            command = int(command)
            command = command - 1

            if command <= len(options):

                if remove:
                    if selected.count(command) > 0:
                        selected.remove(command)
                else:
                    if selected.count(command) == 0:
                        selected.append(command)
        else:

            if remove:

                for x in range(len(options)):

                    if command in options[x]:
                        if selected.count(x) > 0:
                            selected.remove(x)
            else:

                for x in range(len(options)):

                    if command in options[x]:
                        selected.append(x)

    return selected

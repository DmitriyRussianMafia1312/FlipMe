

def AddCard(name,surname,grade):
    import csv
    with open('classmates.csv') as file:
        reader = csv.DictReader(file,
                                delimiter='|')
        result = []
        for row in reader:
            result.append(row)
        result.append({"name": f"{name}", "surname": f"{surname}", "grade": f"{grade}"})

    with open('classmates.csv', 'w', newline='') as file:
        fieldnames = ['name','surname','grade']
        writer = csv.DictWriter(file,
                                fieldnames=fieldnames,
                                delimiter='|')
        writer.writeheader()

        for row in result:
            writer.writerow(row)

AddCard('7','8','9')

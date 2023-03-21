import random

def crossover(person1, person2):
    # crossoverSite = len(str(bin(person1)))-1

    # The string containing 1's and 0's are then converted to array
    arrP1 = list(person1)
    arrP2 = list(person2)

    # Two temps store the last two digits of the binary code from both persons 
    temp1 = [person1[len(person1)-2], person1[len(person1)-1]]
    temp2 = [person2[len(person2)-2], person2[len(person2)-1]]

    # The last two digits of the binary code are interchange with the other person
    arrP1[len(person1)-2] = temp2[0]
    arrP1[len(person1)-1] = temp2[1]
    arrP2[len(person2)-2] = temp1[0]
    arrP2[len(person2)-1] = temp1[1]

    tempStr1 = ""
    tempStr2 = ""

    # Converts the array back to string
    for e in arrP1:
        tempStr1 += e
    
    for x in arrP2:
        tempStr2 += x

    person1 = tempStr1
    person2 = tempStr2

    return [person1, person2]

def initialPopulation(maxPop, rangeLow, rangeHigh):
    ratio = rangeHigh/maxPop

    population = [rangeLow]
    temp = rangeLow

    while(len(population)<maxPop and temp <= rangeHigh):
        temp += ratio
        population.append(temp)

    print(population)

    return population


def selection(maxPop, rangeLow, rangeHigh, numGeneration):
    population = initialPopulation(maxPop, rangeLow, rangeHigh)
    ratio = rangeHigh/maxPop

    genPop = []

    genPop.append(population)
    numPairings = int(len(population)/2)

    shuffleIndex = []

    for x in range(0, len(population)):
        shuffleIndex.append(x)
    
    for x in range(1, numGeneration):
        random.shuffle(shuffleIndex)
        print(shuffleIndex)

        newPopulation = []
        binaryPop = binaryCodeGenerator(len(population))

        print(binaryPop)

        temp = 0

        while(temp < len(binaryPop)):
            newPopulation += crossover(binaryPop[shuffleIndex[temp]], 
            binaryPop[shuffleIndex[temp+1]])
            temp += 2

        print(newPopulation)

        convertedPop = []

        for x in newPopulation:
            num = int(x,2)

            if(num < len(population)):
                convertedPop.append(population[num])
            else:
                numMinusMax = num - (len(population)-1)
                outValue = population[len(population)-1] + (numMinusMax*ratio)
                convertedPop.append(outValue)

        print(convertedPop)

        genPop.append(convertedPop)

    print(genPop)
    
def binaryCodeGenerator(maxPop):
    temp = 0

    binaryPopulation = []

    while(temp < maxPop):
        temp2 = list(bin(temp).replace("0b", ""))

        while(len(temp2)<5):
            temp2.insert(0,"0")

        tempStr = ""

        # Converts the array back to string
        for x in temp2:
            tempStr += x


        binaryPopulation.append(tempStr)
        temp+=1
    
    return binaryPopulation


firstGeneration = initialPopulation(10,1,5)

selection(10,1,5,5)

# x = 10.5
# x = bin(x).replace("0b", "")
# print(x)
# x = int(x, 2)
# print(x)
# print(type(x))

# print(binaryCodeGenerator(10))
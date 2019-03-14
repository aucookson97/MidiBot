from random import randint

class SimpleMarkovChain():

    def __init__(self):
        self.events = []

    def addChainEvent(self, data1, data2):
        found_event1 = False
        found_event2 = False

        event1 = None
        event2 = None

        for event in self.events:
            if event.data == data1:
                event1 = event
                found_event1 = True
            if event.data == data2:
                event2 = event
                found_event2 = True

        if not found_event1:
            event1 = Event(data1)
            self.events.append(event1)
        if not found_event2:
            event2 = Event(data2)
            self.events.append(event2)

        event1.addEventOccurance(event2.data)

    def getRandomEvent(self):
        if (len(self.events) == 0):
            return None
        choice = randint(0, len(self.events)-1)

        return self.events[choice].data

    def getNextEvent(self, data):
        for event in self.events:
            if event.data == data:
                return event.getNextEvent()
        print ("Error Finding Event {}".format(data))

    def printChain(self):
        print ("Chain: ")
        for event in self.events:
            event.printEvent()

class Event():

    def __init__(self, data):
        self.events = []
        self.data = data
        self.probability_table = {}

    def addEventOccurance(self, data):
        if data in self.probability_table.keys():
            self.probability_table[data] += 1
        else:
            self.probability_table[data] = 1

    def printEvent(self):
        print ("\nTable of Event {}".format(self.data))
        print ("\tTotal Events Recorded: {}".format(self.getEventTotal()))
        for key in self.probability_table.keys():
            print ("\tEvent: {}, Occurances: {}".format(key, self.probability_table[key]))
        
    def getNextEvent(self):
        total = self.getEventTotal()
        choice = randint(0, total)
        count = 0
        index = 0

        while count < choice:
            count += self.probability_table[list(self.probability_table.keys())[index]] 
            index += 1

        if index == 0:
            index = 1

        return list(self.probability_table.keys())[index-1]
        

    def getEventTotal(self):
        total = 0
        for value in self.probability_table.values():
            total += value
        return total
    



if __name__=="__main__":
    chain = SimpleMarkovChain()

    chain.addChainEvent("A", "B")
    chain.addChainEvent("A", "B")
    chain.addChainEvent("A", "C")
    chain.addChainEvent("C", "C")
    chain.addChainEvent("C", "A")
    chain.addChainEvent("B", "A")

    chain.printChain()


    for _ in range(10):
        e = chain.getNextEvent("C")
        #print ("Choice: {}".format(e))
        print(chain.getRandomEvent())




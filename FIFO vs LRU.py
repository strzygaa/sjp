import random

#funkcja generująca ciąg odwołań o długości 20 do stron z zakresu od 1 do 9 i zapisująca je do pliku
def generator(saving_file, f):
    file =open(saving_file, 'w')
    file1 = open(f, 'a')
    for i in range(0,20):
        line =str(random.randint(1,9))
        file.write(line+ "\n")
        file1.write(line+"\n")
    file1.write("\n")
    file.close()
    file1.close()



# funkcja odczytująca dane testowe z pliku
def readfile(testedfile):
    file1 = open(testedfile, 'r')
    global data
    data = file1.readlines()
    file1.close()
    data = [int(i) for i in data]
    #zmienna data przechowuje ciąg odwołań do stron
    print(data)
    return data

# funkcja wyświetlająca w ramkach aktualny stan przechowywanych stron
def fifo(order):
    frames = []
    global hit_fifo
    global miss_fifo
    hit_fifo = []
    miss_fifo = []

    foo = len(order)

    print("1"+ " Hit: - " + "  Miss:"+ str(order[0]))
    miss_fifo.append(order[0])

    for i in range(0, foo-1):
        print(str(i+2)+" ",end="") #wyświetlenie numeru kroku
        if (len(frames) < 3):
            frames.append(order[i]) #dodanie stron do listy frames
            miss_fifo.append(order[i])
            print(frames,end=" " + " Hit: - " + "  Miss:"+ str(order[i]))
            print("")
        else:
            #jeśli strona już znajduje się w ramce, pomijamy wymienianie strony
            if (order[i] == frames[0] or order[i] == frames[1] or order[i] == frames[2]):
                hit_fifo.append(order[i])
                print(frames, end=" " + "   Hit:"+ str(order[i]) + "  Miss: - " )
                print("")
            else: #w "ostatnią" ramkę wpisujemy brakującą stronę, pozostałe wartości przesuwając
                #strona z pierwszej ramki jest usuwana
                foo1 = frames[1]
                foo2 = frames[2]
                frames[0] = foo1
                frames[1] = foo2
                frames[2] = order[i]
                miss_fifo.append(order[i])
                print(frames,end=" "+ "   Hit: - "  + "  Miss:" + str(order[i]) )
                print("")



def lru(order):
    frame = []
    foo = len(order)
    global dict
    global hit_lru
    global miss_lru
    hit_lru = []
    miss_lru = []

    #zmienna dict jest słownikiem, przechowującym kolejność ciągu odwołań oraz same wyrazy ciągu
    dict = {i+1: order[i] for i in range(0, foo)}

    # zmienna keys jest listą kluczy zczytaną ze słownika,
    # czyli przechowuje moment "użycia" danej strony
    keys = list(dict.keys())

    print("1"+ " Hit: - " + "  Miss:"+ str(order[0]))
    miss_lru.append(order[0])

    for i in range(0, foo-1):

        if (len(frame) < 3):
            print(str(i + 2),end=" ")#wyświetlenie numeru kroku
            frame.append(keys[i]) #dodanie klucza do listy frame
            miss_lru.append(order[i])

            for j in range(0,len(frame)):
                #wyświetlamy stronę oraz jej "moment użycia"
                print(str(dict[frame[j]])+"("+ str(frame[j])+")",end=" ")
            print("   Hit: - " + "  Miss:"+ str(dict[keys[i]]))

        else:

            before1 = dict[frame[0]]
            before2 = dict[frame[1]]
            before3 = dict[frame[2]]
            # zmienna index przechowuje indeks ramki najdawniej używanej
            # czyli o najmniejszej (najwcześniejszej) wartości
            index = frame.index(min(frame))



            # do ramki o najmniejszej wartości przypisujemy teraz kolejną numerację strony
            frame[index] = keys[i]

            # jeśli "trafimy", dodajemy jedynie numerację, czy też moment użycia
            if (before1 == dict[frame[0]] and before2 == dict[frame[1]] and before3 == dict[frame[2]]):
                hit_lru.append(dict[keys[i]])
                print(str(i + 2) + " " + str(dict[frame[0]]) + "(" + str(frame[0]) + ") "
                      + str(dict[frame[1]]) + "(" + str(frame[1]) + ") "
                      + str(dict[frame[2]]) + "(" + str(frame[2]) + ")",end=" "
                      + "   Hit:" + str(dict[keys[i]]) + "  Miss: - " )

            else:
                #jeśli "nie trafimy" wyświetlamy kolejny nr strony
                miss_lru.append(dict[keys[i]])
                print(str(i + 2) + " " + str(dict[frame[0]]) + "(" + str(frame[0]) + ") "
                      + str(dict[frame[1]]) + "(" + str(frame[1]) + ") "
                      + str(dict[frame[2]]) + "(" + str(frame[2]) + ")",end=" "
                      +"   Hit: - " + "  Miss:"+ str(dict[keys[i]]) )

            print("")


#wyświetlanie procentu trafień i nietrafień
def rate(hit, miss, all, f):
    hit_rate=len(hit)/len(all)*100
    print("The hit rate is: "+ str(hit_rate) +"%")
    miss_rate=len(miss)/len(all)*100
    print("The miss rate is: "+str(miss_rate) +"%")

    file1 = open(f, 'a')
    file1.write(str(miss_rate)+"\n")
    file1.close()


generator("pages.txt", "page_sequences.txt")
print("Pages sequence: ")
readfile("pages.txt")
print("\nNumber of step and pages sequence in each available frame, using First In First Out Method (FIFO): ")
fifo(data)
rate(hit_fifo, miss_fifo, data, "test_fifo.txt")
print("\nNumber of step and pages sequence in each available frame, using Least Recently Used Method (LRU): ")
lru(data)
rate(hit_lru, miss_lru, data, "test_lru.txt")








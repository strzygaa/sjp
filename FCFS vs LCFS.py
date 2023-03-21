import random

#funkcja generująca czasy czekania i czasy wykonywania procesów
def generator(saving_file, key_file):
    file =open(saving_file, 'w')

#losujemy 10 czasów wykonywania się z przedziału 1 do 200 i zapisujemy je do pliku
    for i in range(0,10):
        line =str(random.randint(1,200))
        file.write(line+ "\n")
    file.close()

    filek = open(key_file, 'w')
#losujemy 10 niepowtarzalnych czasów czekania z zakresu od 1 do 20 i zapisujemy do pliku
    foo = random.sample(range(1, 20), 10)
    for i in range(0, len(foo)):
        filek.write(str(foo[i])+"\n")
    filek.close()

# funkcja odczytująca dane testowe z plików
def readfile(testedfile, ktestedfile):
    file1 = open(testedfile, 'r')

    # lista przechowująca dane odczytane z pliku
    global data
    data = file1.readlines()
    file1.close()

    # konwersja na typ integer
    data = [int(i) for i in data]


    file2 =open(ktestedfile, 'r')

#lista przechowująca czasy czekania
    global data_k
    data_k = file2.readlines()
    file2.close()
#konwersja na typ integer
    data_k = [int(i) for i in data_k]


    return data


# funkcja konwertująca listę z odczytanymi danymi do postaci zmiennej oraz słownika
def convert(list1,list_k):

    # zmienna wyrażająca ilość procesów które będą poddawane analizie
    global amount

    # słownik zawierający nr procesu oraz odpowiadający mu czas wykonywania się
    global dict
    foo = len(list1)

# tworzymy słownik z listy ale pojawia się protest ponieważ klucze się nam powtarzają mając rand generowane liczby
    dictionary = {list_k[i]: list1[i] for i in range(0, foo)}

# lista keys zawiera czasy przybycia, sortujemy czasy przybycia
    global keys
    keys=list(dictionary.keys())
    keys.sort()

#dict jest już posortowanym wg czasów przybycia słownikiem
    dict = {keys[i]: dictionary[keys[i]] for i in range(0,len(keys))}
    amount = len(dict)

    return dict, amount


# funkcja zliczająca czas czekania dla każdego procesu FCFS
def count_waiting_time_fcfs(a, d, f):
    # lista przechowująca czasy czekania dla poszczególnych procesów
    global wt
    wt = []

    wt.append(0)
    for i in range(1, a):
        #nasz czas czekania = czas czekania poprzedniego procesu + czas oczekiwania poprzedniego procesu
        # + różnica naszego czasu czekania i poprzedniego procesu
        var = wt[i-1] + d[keys[i-1]] - (keys[i]-keys[i-1])
        wt.append(var)
    file1 = open(f, 'a')
    file1.write(str(wt) + "\n")
    file1.close()
    print(wt)
    return(wt)


# funkcja zliczająca czas czekania dla każdego procesu FCFS
def count_waiting_time_lcfs(a, d, f):
    # lista przechowująca czasy czekania dla poszczególnych procesów
    global wtl
    wtl = []
    wtl.append(0)

    # zmienna przechowująca "aktualny" czas
    timer = 0
    highest = d[keys[a-1]]
    foo = d[keys[a-1]]
    while (len(wtl) < a):

# pętla przechodzi przez wszystkie procesy, wyszukuje ten który przyszedł najpóźniej
# i dodaje go do listy czasu czekania (proces zostaje "wykonany")
# z uwzględnieniem naszego "czasu" mierzonego przez timer

        for i in (1, a-1):

            if (keys[i] <= timer):
                highest = d[keys[i]]
                foo = highest + wtl[len(wtl)-1]

        timer = timer + highest
        wtl.append(foo)
    file1=open(f, 'a')
    file1.write(str(wtl)+"\n")
    file1.close()
    print(wtl)
    return (wtl)

# funkcja licząca średni czas czekania
def average_waiting_time(times,f):
    sum1 = sum(times)
    awt = sum1/len(times)
    print(awt)
    file_af=open(f, 'a')
    file_af.write(str(awt))
    file_af.write("\n")
    file_af.close
    return(awt)


generator("data.txt", "key_data.txt")
readfile("data.txt", "key_data.txt")
convert(data, data_k)

print("Processes and their execution time: ")
print(dict)
#dopisujemy czsy przybycia i czasy czekania procesów do slownika
file_s = open("slownik1.txt", 'a')
file_s.write(str(dict))
file_s.write("\n")
file_s.close

print("\nWaiting time for each process, using First Come First Serve Scheduling (FCFS): ")
count_waiting_time_fcfs(amount, dict, "waiting_time_fcfs1.txt")
print("Average waiting time for FCFS: ")
average_waiting_time(wt, "average_fcfs1.txt")

print("\nWaiting time for each process, using Last Come First Serve Scheduling (LCFS): ")
count_waiting_time_lcfs(amount, dict, "waiting_time_lcfs1.txt")
print("Average waiting time for LCFS: ")
average_waiting_time(wtl, "average_lcfs1.txt")




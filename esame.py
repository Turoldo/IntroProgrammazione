class ExamException(Exception):
        pass

class CSVTimeSeriesFile:
    def __init__(self, name):    
        # Setto il nome del file
        self.name = name
        
    def get_data(self):
        # Inizializzo una lista vuota di output per salvare tutti i dati, e una per effettuare le pulizie
        data = []
        operative_data= []
            # Apro il file
        try: 
            my_file = open(self.name, 'r')
            next(my_file) #salto header
        except: 
            raise ExamException('Non è stato possibile aprire il file.')    
        # Leggo il file linea per linea
        for line in my_file:
            # Faccio lo split di ogni linea sulla virgola
            elements = line.split(',')
            # Posso anche pulire il carattere di newline 
            # dall'ultimo elemento con la funzione strip():
            elements[-1] = elements[-1].strip()
            # Aggiungo alla lista gli elementi di questa linea
            operative_data.append(elements)
          # Chiudo il file
        my_file.close()
               # ho importati i dati grezzi su operative_data. facciamo pulizia
        for element in operative_data:
            if len(element)==2:
                try:      #controllo se il valore di passeggeri è un numero valido. se no salto la linea            
                    x =int(element[1])
                    element[1]=x
                    if x<0:    
                        continue 
                except:
                    continue
                try:             #controllo se le date sono valide. se no salto la linea.
                    year, month =element[0].split('-')
                    year= int(year)
                    month= int(month)
                    if (year<1903) or (month<1) or (month>12): #il primo volo dei fratelli wright è del 17 dicembre 1903. 
                        continue
                except:
                    continue
            if len(element)<=1: #se la linea non ha almeno due valori è sicuramente incompleta, la saltiamo. 
                continue
            if len(element)>=3: 
            #se la linea ha campi aggiuntivi, controllo se data e passeggeri (i primi due campi) sono validi. 
            #se sono validi la importo, se no la salto. 
                temp=[]
                try: 
                    year, month=element[0].split('-')
                    year=int(year)
                    month=int(month)
                    if (year<1903) or (month<1) or (month>12):
                        continue
                except:
                    continue
                try: 
                    z= int(element[1])
                    element[1]=z
                    if z<=0:
                        continue
                except:
                    continue
                temp=[element[0], element[1]]
                data.append(temp)
                continue #importante questo continue se no aggiungerei la linea due volte.
            data.append(element)
        for i in range(0,len(data)-1): #controlla il -1
        #per tutti i dati puliti, controllo se ci sono date non ordinate o ripetute. In tal caso non si può procedere.
            year, month= data[i][0].split('-')
            nyear, nmonth= data[i+1][0].split('-')
            year=int(year)
            month=int(month)
            nyear=int(nyear)
            nmonth=int(nmonth)
            if (year>nyear) or (year==nyear and (month>nmonth)):
                raise ExamException('Errore: le date non sono ordinate')
            if (year==nyear and month==nmonth):
                raise ExamException('Errore: ci sono date ripetute')
        return data #NB: il testo dell'esame voleva che la data nell'output fosse di tipo stringa. 

def detect_similar_monthly_variations(time_series, years):
    #rendiamo la lista numerica, dividendo anni e mesi
    mytimeseries= time_series
    for element in mytimeseries:
        element[0]=element[0].split('-')
        element[0][0]=int(element[0][0])
        element[0][1]=int(element[0][1])
        #ora ogni riga del database mytimeseries ha due elementi: 
        #una lista di due elementi numerici (anno e mese) e un elemento numerico (passeggeri)
   
    #calcolo la differenza tra mesi consecutivi dell'anno 1-> 11 elementi salvati in differences1
    year1=[]
    differences1=[]
    #trovo le righe corrispondenti al primo anno da analizzare
    for element in mytimeseries:
        if element[0][0]==years[0]:
            year1.append(element)
    if len(year1)==0:
        raise ExamException('Errore: il primo anno selezionato per le analisi non è valido.')
    #per ogni mese dell'anno selezionato, cerco i rispetti valori dei passeggeri.
    for i in range(1,12):
        flag1= 0
        flag2= 0
        for el in year1:
            if el[0][1]==i:
                x=el[1]
                flag1= 1
            if el[0][1]==i+1:
                y=el[1]
                flag2= 1
        if (flag1==0) or (flag2==0): 
            #se non trovo un mese, non si può calcolare la differenza tra quel mese e il successivo, 
            #nè la differenza tra il mese precedente e il mese mancante. 
            differences1.append('NA')
        else:    
            differences1.append(x-y) #conta solo la differenza in valore assoluto?
            #visto il contesto credo abbia più senso la differenza con segno. 

    #calcolo la differenza tra mesi consecutivi dell'anno 2-> 11 elementi salvati in differences2
    year2=[]
    differences2=[]
    #trovo le righe corrispondenti al secondo anno da analizzare
    for element in mytimeseries:
        if element[0][0]==years[1]:
            year2.append(element)
    if len(year2)==0:
        raise ExamException('Errore: il secondo anno selezionato per le analisi non è valido.')
    #per ogni mese dell'anno selezionato, cerco i rispettivi valori dei passeggeri.
    for i in range(1,12):
        flag1= 0
        flag2= 0
        for el in year2:
            if el[0][1]==i:
                x=el[1]
                flag1= 1
            if el[0][1]==i+1:
                y=el[1]
                flag2= 1
        if (flag1==0) or (flag2==0): 
            #se non trovo un mese, non si può calcolare la differenza tra quel mese e il successivo, 
            #nè la differenza tra il mese precedente e il mese mancante. 
            differences2.append('NA')
        else:    
            differences2.append(x-y) #conta solo la differenza in valore assoluto?
            #visto il contesto credo abbia più senso la differenza con segno. 

    #ora ho i due vettori differences1 e differences2.         
    #faccio la differenza tra gli 11 elementi, inserisco i risultati in differencesBool. 
    differencesBool=[]
    for t in range(0,11):
        #se uno dei due vettori di differenze ha dato missing, non posso calcolare la differenza tra i due valori. 
        if (differences1[t]=='NA') or (differences2[t]=='NA'):
            differencesBool.append(False)
        else:   
            if abs(differences1[t]-differences2[t])<2: 
                differencesBool.append(True)
            else:
                differencesBool.append(False)
    #et voilà!
    return differencesBool
            
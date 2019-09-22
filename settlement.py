
#Example data, from Ibestad kommune, 2019 election:
votetotals_ibestad = {'Høyre':7876,'Arbeiderpartiet':4562,'Senterpartiet':3028}
number_of_seats_ibestad = 19

votetotals_lillestrøm = {'Arbeiderpartiet':648350,'Høyre':424811,'Senterpartiet':258324,'Fremskritsspartiet':230864,'Miljøpartiet De grønne':138608,
'Folkets røst by og bygdeliste':109443,'Sosialistisk venstreparti':107511,'Venstre':62553,'Rødt':56114,
'Kristelig folkeparti':51909,'Pensjonistpartiet':37137,'Helsepartiet':17781,'Demokratene':14081,'Liberalistene':10119}
number_of_seats_lillestrøm = 55

def distribute_seats(votetotals,number_of_seats,first_divisor = 1.4, wait = False):

    print('Calculating election result from vote totals.')
    print('Number of seats to be distributed: ',number_of_seats)
    print('First divisor:',first_divisor)
    print('Vote totals:')
    print(votetotals)


    #Create variable to keep track of how many seats have been filled
    awardedseats_total = 0


    #Initialize dictionary for quotients 
    quotients = votetotals.copy() #probably here?

      
    #Calculate initial quotients (divide vote total by first divisor)
    for key in quotients:
        quotients[key] = quotients[key] / first_divisor

    
    #Set the initial divisors
    print('Setting initial divisors...')
    divisors = dict.fromkeys(votetotals, first_divisor)
    print('Initial divisors')
    print(divisors)
    

    #Make an (empty) list of awarded seats
    seats = []

    #Create dict to keep track of how many seats have been won by each party
    party_seats = dict.fromkeys(votetotals, 0)
      
    while awardedseats_total < number_of_seats:
        if wait == True:
            print('Ready to award seat #',awardedseats_total+1)
            userinput = input('Press Enter to proceed to next seat. Press E + Enter to proceed to end. ')
            if userinput.lower() == 'e':
                wait = False
            print('Input:',userinput)
        
        print('Awarding seat #',awardedseats_total+1,'...')
        #Award the seat to the party with the highest current quotient
        print('Current quotients:',quotients)
        seatwinner = max(quotients, key=quotients.get)
        print('Winner of seat #',awardedseats_total+1,': ',seatwinner)

     
        #Update the list of awarded seats
        seats.append(seatwinner)
        print('Seats awarded so far:')
        print(seats)
        #Keep track of how many seats won by each party
        party_seats[seatwinner] = party_seats[seatwinner] + 1
        #Set the new divisor for the seatwinner
        divisors[seatwinner] = 2*party_seats[seatwinner] + 1

        print('New divisor for ',seatwinner,':')
        print(divisors[seatwinner])
        #Calculate the new quotient for the seatwinner:
        quotients[seatwinner] = votetotals[seatwinner] / divisors[seatwinner]
        print('New quotient for ',seatwinner,':')
        print(quotients[seatwinner])
        #Keep track of how many seats have been filled
        awardedseats_total  = len(seats)
        print('Seats awarded: ',awardedseats_total)

        
    print('SEAT DISTRIBUTION FINISHED.')
    print('Total number of seats awarded:',awardedseats_total)
    print('Seats per party:')
    print(party_seats)
    
    return

distribute_seats(votetotals_ibestad,number_of_seats_ibestad,wait = False)


distribute_seats(votetotals_lillestrøm,number_of_seats_lillestrøm,wait = False)

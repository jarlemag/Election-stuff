
#Example data from Ibestad kommune, 2019 election. From election protocol, available at: https://github.com/elections-no/elections-no.github.io/blob/master/docs/2019/Troms_og_Finnmark/Ibestad%20kommune%2C%20Troms%20og%20Finnmark%20fylke%20-%20kommune%2010-09-2019.pdf
votetotals_ibestad = {'Høyre':7876,'Arbeiderpartiet':4562,'Senterpartiet':3028}
number_of_seats_ibestad = 19

#Example data from Lillestrøm kommune, 2019 election. From election protocol, available at: https://github.com/elections-no/elections-no.github.io/blob/master/docs/2019/Viken/Kommunestyrevalget%20-%20valgstyrets%20møtebok%20Lillestrøm.pdf
votetotals_lillestrøm = {'Arbeiderpartiet':648350,'Høyre':424811,'Senterpartiet':258324,'Fremskritsspartiet':230864,'Miljøpartiet De grønne':138608,
'Folkets røst by og bygdeliste':109443,'Sosialistisk venstreparti':107511,'Venstre':62553,'Rødt':56114,
'Kristelig folkeparti':51909,'Pensjonistpartiet':37137,'Helsepartiet':17781,'Demokratene':14081,'Liberalistene':10119}
number_of_seats_lillestrøm = 55

def distribute_seats(votetotals,number_of_seats,first_divisor = 1.4, wait = False,Verbose = False):

    print('Calculating election result from vote totals.')
    print('Number of seats to be distributed: ',number_of_seats)
    print('First divisor:',first_divisor)
    print('Vote totals:')
    print(votetotals)


    #Create variable to keep track of how many seats have been filled
    awardedseats_total = 0


    #Initialize dictionary for quotients 
    quotients = votetotals.copy()

      
    #Calculate initial quotients (divide vote total by first divisor)
    for key in quotients:
        quotients[key] = quotients[key] / first_divisor

    
    #Set the initial divisors
    if Verbose:
        print('Setting initial divisors...')
    divisors = dict.fromkeys(votetotals, first_divisor)
    if Verbose:
        print('Initial divisors')
        print(divisors)
    

    #Make an (empty) list of awarded seats
    seats = []

    #Create dict to keep track of how many seats have been won by each party
    party_seats = dict.fromkeys(votetotals, 0)
      
    result_table = 'Seat #\tWinning party\tDivisor\tQuotient\n'
    result_table = result_table.expandtabs(32)

    while awardedseats_total < number_of_seats:
        if wait == True:
            print('Ready to award seat #',awardedseats_total+1)
            userinput = input('Press Enter to proceed to next seat. Press E + Enter to proceed to end. ')
            if userinput.lower() == 'e':
                wait = False
            print('Input:',userinput)

        if Verbose:
            print('Awarding seat #',awardedseats_total+1,'...')
        #Award the seat to the party with the highest current quotient
        if Verbose:
            print('Current quotients:',quotients)
        seatwinner = max(quotients, key=quotients.get)
        if Verbose:
            print('Winner of seat #',awardedseats_total+1,': ',seatwinner)

        #Update the list of awarded seats
        seats.append(seatwinner)
        if Verbose:
            print('Seats awarded so far:')
            print(seats)

        #Keep track of how many seats have been filled
        awardedseats_total  = len(seats)

        new_line = str(awardedseats_total)+'\t'+str(seatwinner)+'\t'+str(divisors[seatwinner])+'\t'+'%.3f'%(quotients[seatwinner])+'\n'
        new_line = new_line.expandtabs(32)
        result_table = result_table + new_line
        
                            
        #Keep track of how many seats won by each party
        party_seats[seatwinner] = party_seats[seatwinner] + 1
        #Set the new divisor for the seatwinner
        divisors[seatwinner] = 2*party_seats[seatwinner] + 1

        if Verbose:
            print('New divisor for ',seatwinner,':')
            print(divisors[seatwinner])
        #Calculate the new quotient for the seatwinner:
        quotients[seatwinner] = votetotals[seatwinner] / divisors[seatwinner]
        if Verbose:
            print('New quotient for ',seatwinner,':')
            print(quotients[seatwinner])
        
        if Verbose:
            print('Seats awarded: ',awardedseats_total)

               
    print('SEAT DISTRIBUTION FINISHED.')
    print('Total number of seats awarded:',awardedseats_total)
    print('Seats per party:')
    print(party_seats)

    print(result_table)
    
    return

distribute_seats(votetotals_ibestad,number_of_seats_ibestad,wait = False)


distribute_seats(votetotals_lillestrøm,number_of_seats_lillestrøm,wait = False)



def leastvotechange(votetotals,number_of_seats):
    #Find the smallest difference in votes which can lead to a changed election result

    #let "n" be the number of seats to be distributed.
    #Assume party X wins the last seat, seat n, and party Y would have won seat n +1:    
    #Calculate the winning quotients for n+1 seats.

    #take the difference in quotients for seats n and n+1 and divide by the divisor for the winning quotient for seat n+1
    #to determine how many additional votes (not changing any existing votes) party Y would need to win seat n
        #If seats n and n+1 are won by the same party (party X), find the next seat not won by party X and do the same calculation
    #take the difference in quotients for seats n and n+1 and divide by the divisor for the winning quotient for seat n
    #to determine how many votes party X would need to lose (not changing any existing votes) in order to lose seat n
        #If seats n and n+1 are won by the same party (party X), find the next seat not won by party X and do the same calculation


    #Take the smallest amount of votes that party X would have to lose or party Y would have to gain while not changing any other votes, in order for party Y to win seat n.
    #Divide this number by two to determine the smallest number of votes who could change the result by switching their vote from party X to party Y. (??)
    return



def neededvotes(votetotals,number_of_seats,party):
    #find out how many additional votes (not changing any existing votes) a party not currently represented would need in order to win 1 seat.

    #check that the party is not currently represented
    #get the difference between the (initial) quotient for the non-represented party, and the quotient that won the last seat., and divide by the first divisor.

    return
    

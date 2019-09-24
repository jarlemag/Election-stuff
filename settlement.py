
import math

#Example data from Ibestad kommune, 2019 election. From election protocol, available at: https://github.com/elections-no/elections-no.github.io/blob/master/docs/2019/Troms_og_Finnmark/Ibestad%20kommune%2C%20Troms%20og%20Finnmark%20fylke%20-%20kommune%2010-09-2019.pdf
votetotals_ibestad = {'Høyre':7876,'Arbeiderpartiet':4562,'Senterpartiet':3028}
number_of_seats_ibestad = 19

#Example data from Lillestrøm kommune, 2019 election. From election protocol, available at: https://github.com/elections-no/elections-no.github.io/blob/master/docs/2019/Viken/Kommunestyrevalget%20-%20valgstyrets%20møtebok%20Lillestrøm.pdf
votetotals_lillestrøm = {'Arbeiderpartiet':648350,'Høyre':424811,'Senterpartiet':258324,
                         'Fremskritsspartiet':230864,'Miljøpartiet De grønne':138608,
                         'Folkets røst by og bygdeliste':109443,'Sosialistisk venstreparti':107511,'Venstre':62553,'Rødt':56114,
                         'Kristelig folkeparti':51909,'Pensjonistpartiet':37137,'Helsepartiet':17781,'Demokratene':14081,'Liberalistene':10119}
number_of_seats_lillestrøm = 55


#Example data from Oslo kommune, 2019 election.
votetotals_oslo =  {'Alliansen':23736,'Arbeiderpartiet':4315487,'Demokratene':57166,'Feministisk Initiativ':34705,'Folkeaksjonen Nei til mer bompenger':1258733,
                    'Fremskrittspartiet':1137175,'Helsepartiet':50227,'Høyre':5477649,'Kristelig Folkeparti':375020,'Kystpartiet':9411,'Liberalistene':47967,
                    'Miljøpartiet De Grønne':3288756,'Norges Kommunistiske Parti':15697,'Partiet De Kristne':36120,'Pensjonistpartiet':131046,'Piratpartiet':40999,
                    'Rødt':1550902,'Selvstendighetspartiet':33786,'Senterpartiet':471025,'SV - Sosialistisk Venstreparti':1960947,'Venstre':1245999}
number_of_seats_oslo = 59

#Example data from Drammen kommune, 2019 election.
votetotals_drammen = {'Alliansen':13714,'Folkestyre':9152,'Helsepartiet':15222,'Høyre':697348,'KrF':61126,'Liberalistene':5474,'Nei til bomring':208012,'Partiet De Kristne':8948,'Rødt':68365,'Senterpartiet':216284,'SV':121984,'Venstre':56860,'Arbeiderpartiet':710950,'Fremskrittspartiet':290897,'Miljøpartiet de grønne':233538}
number_of_seats_drammen = 57

votetotals_bergen = {'Partiet De Kristne':74558,'Senterpartiet':534887,'Venstre':387477,'Pensjonistpartiet':150044,'Demokratene':57058,
                                          'Norges Kommunistiske Parti':6112,'Liberalistene':20914,'Kristelig Folkeparti':310008,'Piratpartiet':14405,
                                          'Folkeaksjonen Nei til mer bompenger':1677902,'SV':866352,'Arbeiderpartiet':1992486,'Fremskrittspartiet':469259,
                                          'Høyre':2016633,'Miljøpartiet De Grønne':998929,'Rødt':491334}
number_of_seats_bergen = 67

votetotals_bergen_modified = votetotals_bergen.copy()
votetotals_bergen_modified['SV'] = 838949

#Example data from Gjøvik kommune, 2019 election.
votetotals_gjovik = {'Sp':131218,'KrF':14215,'Ap':194647,'SV':30329,'Liberalistene':1566,'Venstre':16619,'Høyre':110985,'Rødt':36019,'Partiet De Kristne':4181,
                     'MdG':22645,'FrP':22031}



number_of_seats_gjovik = 41


#Example data from Gaustad kommune, 2019 election.
votetotals_gaustad = {'Bygdalista i Gausdal':6791,'Arbeiderpartiet':26031,'Tverrpolitisk liste for Fremskrittspartiet, Høyre og Venstre':4194,
                      'Senterpartiet':31602,'Miljøpartiet De Grønne':3004}

number_of_seats_gaustad = 23

#Example data from Evenes kommune, 2019 election.

votetotals_evenes = {'Evenes tverrpolitiske liste':3824,'Fremskrittspartiet':518,'Senterpartiet':2481,'Høyre':3297,'Arbeiderpartiet':3654,'SV':523}
number_of_seats_evenes = 17


def distribute_seats(votetotals_in,number_of_seats,first_divisor = 1.4, wait = False,Verbose = False,adjustments = {}):
    #Note: The numbers used in votetotals should in most cases be "Stemmelistetall", the number of votes cast multiplied by the number of seats to be distributed,
    #and further modified (subtractions and additions) by personal votes. However, the function will also return correct result if the actual numbers of votes (ballots) cast are used
    #and there are no personal votes considered.
    votetotals = votetotals_in.copy()
    print('Calculating election result from vote totals.')
    print('Number of seats to be distributed: ',number_of_seats)
    print('First divisor:',first_divisor)
    print('Vote totals:')
    print(votetotals)


    #Perform adjustments to vote totals, if any:
    if adjustments:
        for key in adjustments:
            print('Adjusting vote totals for:',key)
            votetotals[key] =  votetotals[key] + adjustments[key]
            print('Vote total for',str(key),'adjusted by',str(adjustments[key]))
            print('New vote total for ',str(key),':',votetotals[key])

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
    
    #Make a list of the winning quotient for each seat
    winning_quotients = []
    
    #Make a list of the divisors used to calculate the winning quotient for each seat
    winning_quotient_divisors = []

    #Create dict to keep track of how many seats have been won by each party
    party_seats = dict.fromkeys(votetotals, 0)

    #Create a printable results table  
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

        #Update the lists of awarded seats, winning quotients and their divisors
        seats.append(seatwinner)
        winning_quotients.append(quotients[seatwinner])
        winning_quotient_divisors.append(divisors[seatwinner])
        
        if Verbose:
            print('Seats awarded so far:')
            print(seats)

        #Keep track of how many seats have been filled
        awardedseats_total  = len(seats)

        #Append the printable results table
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
    
    return [seats,winning_quotient_divisors,winning_quotients,party_seats]



#ibestad_result = distribute_seats(votetotals_ibestad,number_of_seats_ibestad,wait = False)

#print('Valgresultat Ibestad:')
#print(ibestad_result)

#lillestrøm_result = distribute_seats(votetotals_lillestrøm,number_of_seats_lillestrøm,wait = False)



def leastvotechange(votetotals,number_of_seats):
    #Find the smallest difference in votes which can lead to a changed election result
    print('Finding smallest change in voting required to change election result.')
    #let "n" be the number of seats to be distributed.
    n = number_of_seats
    #Assume party X wins the last seat, seat n, and party Y would have won seat n +1:    


    #Calculate the winning quotients for n+1 seats.
    expanded_result = distribute_seats(votetotals,n + 1)

    print('Final seat awarded:')

    result_table = 'Seat #\tWinning party\tDivisor\tQuotient\n'
    result_table = result_table.expandtabs(32)

    divisor_seat_n = expanded_result[1][-2]
    divisor_seat_n_plus_one = expanded_result[1][-1]

    winner_seat_n = expanded_result[0][n-1]
    winner_seat_n_plus_one = expanded_result[0][n]
    
    
    #Take the difference in quotients for seats n and n+1
    quotient_seat_n = expanded_result[2][-2]
    quotient_seat_n_plus_one = expanded_result[2][-1]
    
    quotient_difference = quotient_seat_n  - quotient_seat_n_plus_one

    #to determine how many additional votes (not changing any existing votes) party Y would need to win seat n
    #divide the quotient difference by the divisor for the winning quotient for seat n+1
    required_vote_total_increase = quotient_difference * divisor_seat_n_plus_one   #should be multiply, not divide?
    #TODO: If seats n and n+1 are won by the same party (party X), find the next seat not won by party X and do the same calculation

    #to determine how many votes party X would need to lose (not changing any existing votes) in order to lose seat n
    #divide the quotient difference by the divisor for the winning quotient for seat n
    required_vote_total_decrease = quotient_difference * divisor_seat_n
    #TODO: If seats n and n+1 are won by the same party (party X), find the next seat not won by party X and do the same calculation

    required_votes_cast_decrease = required_vote_total_decrease/number_of_seats
    required_votes_cast_increase = required_vote_total_increase/number_of_seats

    quotient_loss_per_vote_total_transfer = 1 / divisor_seat_n
    quotient_gain_per_vote_total_transfer = 1 / divisor_seat_n_plus_one
    total_quotient_gap_change_per_vote_total_transfer = quotient_loss_per_vote_total_transfer + quotient_gain_per_vote_total_transfer

    print('quotient_loss_per_vote_total_transfer','%.5f'%quotient_loss_per_vote_total_transfer)
    print('quotient_gain_per_vote_total_transfer','%.5f'%quotient_gain_per_vote_total_transfer)
    print('total_quotient_gap_change_per_vote_total_transfer:','%.5f'%total_quotient_gap_change_per_vote_total_transfer)
    required_vote_total_transfer = quotient_difference / total_quotient_gap_change_per_vote_total_transfer
    required_votes_transfer = required_vote_total_transfer/number_of_seats

    new_line1 = str(n)+'\t'+str(winner_seat_n)+'\t'+str(divisor_seat_n)+'\t'+'%.3f'%(quotient_seat_n)+'\n'
    new_line1 = new_line1.expandtabs(32)
    new_line2 = str(n+1)+'\t'+str(winner_seat_n_plus_one)+'\t'+str(divisor_seat_n_plus_one)+'\t'+'%.3f'%(quotient_seat_n_plus_one)+'\n'
    new_line2 = new_line2.expandtabs(32)
    result_table = result_table + new_line1 + new_line2

    print(result_table)
 
    print('quotient_difference: ','%.3f'%quotient_difference)
    print('\n')
    print('Increase in vote total (listestemmetall) (not changing any existing votes) to party',winner_seat_n_plus_one,'needed to change election result:','%.3f'%required_vote_total_increase)
    print('Increase in votes cast (not changing any existing votes) for party',winner_seat_n_plus_one,'needed to change election result:',math.ceil(required_votes_cast_increase),',rounded up from','%.3f'%required_votes_cast_increase)
    print('\n')
    print('Decrease in vote total (listestemmetall) (not changing any existing votes) to party',winner_seat_n,'needed to change election result:','%.3f'%required_vote_total_decrease)
    print('Decrease in votes cast (not changing any existing votes) for party',winner_seat_n,'needed to change election result:',math.ceil(required_votes_cast_decrease),',rounded up from','%.3f'%required_votes_cast_decrease)

          
   
    print('\n')
    print('Vote total (listestemmetall) transferred from party',winner_seat_n,'to party',winner_seat_n_plus_one,'needed to change election result:','%.3f'%required_vote_total_transfer)
    print('Votes (stemmer) transferred from party',winner_seat_n,'to party',winner_seat_n_plus_one,'needed to change election result:',math.ceil(required_votes_transfer),',rounded up from','%.3f'%required_votes_transfer)

    
    return


#distribute_seats(votetotals_lillestrøm,number_of_seats_lillestrøm,wait = False)

#leastvotechange(votetotals_lillestrøm,54)
#leastvotechange(votetotals_lillestrøm,55)
#leastvotechange(votetotals_ibestad,19)


#distribute_seats(votetotals_drammen,number_of_seats_drammen,wait = False)
#leastvotechange(votetotals_drammen,57)

#distribute_seats(votetotals_oslo,number_of_seats_oslo,wait = False)
#leastvotechange(votetotals_oslo,number_of_seats_oslo)


#print('ready to perform Bergen vote adjustment test.')




#print('Bergen #1:')
#print('votetotals_bergen:')
#print(votetotals_bergen)
#distribute_seats(votetotals_bergen,number_of_seats_bergen,wait = False)

#print('Bergen #2:')
#print('votetotals_bergen:')
#print(votetotals_bergen)
#distribute_seats(votetotals_bergen_modified,number_of_seats_bergen,wait = False)

#print('Bergen #3:')
#print('votetotals_bergen:')
#print(votetotals_bergen)
#distribute_seats(votetotals_bergen,number_of_seats_bergen,wait = False, adjustments = {'SV': -409*number_of_seats_bergen})


#print('Votetotals_bergen after Bergen #3:')
#print(votetotals_bergen)

#leastvotechange(votetotals_bergen,number_of_seats_bergen)

 
def neededvotes(votetotals,number_of_seats,party, divisor = 1.4):
    #find out how many additional votes (not changing any existing votes) a party not currently represented would need in order to win 1 seat.
    result = distribute_seats(votetotals,number_of_seats, first_divisor = divisor)
    seats = result[0]
    winning_quotients = result[2]
    if party in seats:
        print(party,'won one or more seats in the election.')
    else:
        party_quotient = votetotals[party] / divisor
        print(party,'quotient:',party_quotient)
        last_winning_quotient = winning_quotients[-1]
        print('Last winning quotient:',last_winning_quotient)
        quotient_difference = last_winning_quotient - party_quotient
        required_votetotal_increase = quotient_difference * divisor
        required_vote_increase = required_votetotal_increase / number_of_seats 

        print(party,'Needs to increase vote total by',required_votetotal_increase,'to win one seat.')
        print(party,'Needs',math.ceil(required_vote_increase),'additional votes to win one seat.')
        

    return


def compareresults(result1,result2):
    #Compare two election results. Determine if the election outcome (number of seats awarded to each party) is different.

    party_seats1 = result1[-1]
    party_seats2 = result2[-1]

    if party_seats1 == party_seats2:
        print('Election outcomes are identical.')
        return True
    else:
        print('Election outcomes are different.')
        return False

#print('Create result1 and result2:')
#print('Votetotals_bergen:')
#print(votetotals_bergen)
#result1 = distribute_seats(votetotals_bergen,number_of_seats_bergen,wait = False)
#result2 = distribute_seats(votetotals_bergen,number_of_seats_bergen,wait = False, adjustments = {'SV': -409*number_of_seats_bergen}) #Får SV en plass mindre? Virker som resultatet ikke alltid blir likt. Må sjekke igjen.

#print('Compare result1 to result1:')
#compareresults(result1,result1)
#print('Compare result1 to result2:')
#compareresults(result1,result2)


#distribute_seats(votetotals_gjovik,number_of_seats_gjovik,wait = False)
#leastvotechange(votetotals_gjovik,number_of_seats_gjovik)


#distribute_seats(votetotals_evenes,number_of_seats_evenes,wait = False)
#leastvotechange(votetotals_evenes,number_of_seats_evenes)

neededvotes(votetotals_lillestrøm,number_of_seats_lillestrøm,'Helsepartiet')

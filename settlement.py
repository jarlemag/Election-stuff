
#Example data, from Ibestad kommune, 2019 election:
votetotals = {'Høyre':7876,'Arbeiderpartiet':4562,'Senterpartiet':3028}
number_of_seats = 19

def distribute_seats(votetotals,number_of_seats,first_divisor = 1.4):

    print('Calculating election result from vote totals.')
    print('Number of seats to be distributed: ',number_of_seats)
    print('First divisor:',first_divisor)
    print('Vote totals:')
    print(votetotals)


    #Create variable to keep track of how many seats have been filled
    awardedseats_total = 0


    #Initialize dictionary for quotients 
    quotients = votetotals

      
    #Calculate initial quotients (divide vote total by first divisor)
    for key in quotients:
        quotients[key] = quotients[key] / first_divisor
      
    #Set the initial divisors
    divisors = dict.fromkeys(votetotals, first_divisor)

    #Make an (empty) list of awarded seats
    seats = []

    #Create dict to keep track of how many seats have been won by each party
    party_seats = dict.fromkeys(votetotals, 0)
      
    while awardedseats_total < number_of_seats:
        print('Awarding seat #',awardedseats_total+1,'...')
        #Award the seat to the party with the highest current quotient
        print('Current quotients:',quotients)
        seatwinner = max(quotients, key=votetotals.get)
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

distribute_seats(votetotals,number_of_seats)

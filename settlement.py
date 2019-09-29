
import math
from collections import Counter
import io
import sys
import json


data_dict = json.load(open('data.json'))

#https://bytes.com/topic/python/answers/724534-stopping-fucntion-printing-its-output-screen
class NullWriter(object):
    def write(self, arg):
        pass




def distribute_seats_wrapper(data_dictionary,data_dictionary_key,first_divisor = 1.4, wait = False,verbose = False,adjustments = {}, silent = False,output_path = "output.json"):
    #Wraps the distribut_seats() function in order to allow data to be retrieved from a dictionary
    #Extracts desired data from a dictionary and passes to the distribute_seats function.

    #Rename the arguments to be passed on in case using e.g "first_divisor = first_divisor" in distribute_seats() function call is a problem
    first_divisor_out = first_divisor
    wait_out = wait
    verbose_out =verbose
    adjustments_out = adjustments
    silent_out = silent
    output_path_out = output_path

    sub_dictionary = data_dictionary[data_dictionary_key]
    votetotals = sub_dictionary["voteTotals"].copy()
    number_of_seats = sub_dictionary["numberOfSeats"]
    description_out = sub_dictionary["contestDescription"]

    stemmer_out = sub_dictionary.get('stemmer') #Returns None if no ballot numbers included in the data source
    

    return distribute_seats(votetotals,number_of_seats,ballot_numbers = stemmer_out,first_divisor = first_divisor_out, wait = wait_out,verbose = verbose_out,
                            adjustments = adjustments_out, silent = silent_out,output_path = output_path_out,description = description_out)
    

def distribute_seats(votetotals_in,number_of_seats,ballot_numbers = None,first_divisor = 1.4, wait = False,verbose = False,
                     adjustments = {}, silent = False,output_path = "output.json",description = "Unknown"):
    if silent:
        out = NullWriter()
    else:
        out = sys.stdout
    
    #Note: The numbers used in votetotals should in most cases be "Stemmelistetall", the number of votes cast multiplied by the number of seats to be distributed,
    #and further modified (subtractions and additions) by personal votes. However, the function will also return correct result if the actual numbers of votes (ballots) cast are used
    #and there are no personal votes considered.
    
    votetotals = votetotals_in.copy()
   
    print('Calculating election result from vote totals for',description,file=out)
    print('Number of seats to be distributed: ',number_of_seats,file=out)
    print('First divisor:',first_divisor,file=out)
    print('Vote totals:',file=out)
    print(votetotals,file=out)


    #Perform adjustments to vote totals, if any:
    if adjustments:
        for key in adjustments:
            print('Adjusting vote totals for:',key,file=out)
            votetotals[key] =  votetotals[key] + adjustments[key]
            print('Vote total for',str(key),'adjusted by',str(adjustments[key]),file=out)
            print('New vote total for ',str(key),':',votetotals[key],file=out)

    #Create variable to keep track of how many seats have been filled
    awardedseats_total = 0
    
    #Initialize dictionary for quotients 
    quotients = votetotals.copy()

    #Calculate initial quotients (divide vote total by first divisor)
    for key in quotients:
        quotients[key] = quotients[key] / first_divisor

    #Set the initial divisors
    if verbose:
        print('Setting initial divisors...',file=out)
    divisors = dict.fromkeys(votetotals, first_divisor)
    if verbose:
        print('Initial divisors',file=out)
        print(divisors)
    
    #Make an (empty) list of awarded seats
    seats = []
    
    #Make a list of the winning quotient for each seat
    winning_quotients = []
    
    #Make a list of the divisors used to calculate the winning quotient for each seat
    winning_quotient_divisors = []

    #Create dict to keep track of how many seats have been won by each party
    party_seats_numbers = dict.fromkeys(votetotals, 0)

    #Create a printable results table  
    result_table = 'Seat #\tWinning party\tDivisor\tQuotient\n'
    result_table = result_table.expandtabs(32)

    while awardedseats_total < number_of_seats:
        if wait == True:
            print('Ready to award seat #',awardedseats_total+1,)
            userinput = input('Press Enter to proceed to next seat. Press E + Enter to proceed to end. ')
            if userinput.lower() == 'e':
                wait = False
            print('Input:',userinput)

        if verbose:
            print('Awarding seat #',awardedseats_total+1,'...',file=out)
        #Award the seat to the party with the highest current quotient
        if verbose:
            print('Current quotients:',quotients,file=out)

            
        seatwinner = max(quotients, key=quotients.get)
        #check if there are multiple parties that have the max quotient:
        maxquotientkeys = []
        for key, value in quotients.items():
            if value == quotients[seatwinner]:
                maxquotientkeys.append(key)

        #Possible to do more succintly, with a list comprehension, for example the below?
        #maxkeys = [key for key in quotients.items() if (key == quotients[seatwinner])]

        if len(maxquotientkeys) > 1:
            print('Multiple identical quotients applicable to the same seat.')
            if ballot_numbers == None:
                print('Unable to resolve result, as ballot numbers have not been provided. Aborting!')
                return None
            else:
                seatwinner = max(ballot_numbers, key=ballot_numbers.get)
                maxballot_numberkeys = []
                for key, value in ballot_numbers.items():
                    if value == ballot_numbers[seatwinner]:
                        maxballot_numberkeys.append(key)
                if len(maxballot_numberkeys) >1:
                    print('Unable to resolve result, as ballot numbers are identical. Seat winner must be determined by drawing lots. Aborting!')
                    return None

                else:
                    print(seatwinner,'wins the seat by virtue of largest ballot number: ',ballot_numbers[seatwinner],' ballots.')
                
                
        if verbose:
            print('Winner of seat #',awardedseats_total+1,': ',seatwinner,file=out)

        #Update the lists of awarded seats, winning quotients and their divisors
        seats.append(seatwinner)
        winning_quotients.append(quotients[seatwinner])
        winning_quotient_divisors.append(divisors[seatwinner])
        
        if verbose:
            print('Seats awarded so far:',file=out)
            print(seats,file=out)

        #Keep track of how many seats have been filled
        awardedseats_total  = len(seats)

        #Append the printable results table
        new_line = str(awardedseats_total)+'\t'+str(seatwinner)+'\t'+str(divisors[seatwinner])+'\t'+'%.3f'%(quotients[seatwinner])+'\n'
        new_line = new_line.expandtabs(32)
        result_table = result_table + new_line
                             
        #Keep track of how many seats won by each party
        party_seats_numbers[seatwinner] = party_seats_numbers[seatwinner] + 1
        
        #Set the new divisor for the seatwinner
        divisors[seatwinner] = 2*party_seats_numbers[seatwinner] + 1

        if verbose:
            print('New divisor for ',seatwinner,':',file=out)
            print(divisors[seatwinner],file=out)
        #Calculate the new quotient for the seatwinner:
        quotients[seatwinner] = votetotals[seatwinner] / divisors[seatwinner]
        if verbose:
            print('New quotient for ',seatwinner,':',file=out)
            print(quotients[seatwinner],file=out)
        
        if verbose:
            print('Seats awarded: ',awardedseats_total,file=out)

               
    print('SEAT DISTRIBUTION FINISHED.',file=out)
    print('Total number of seats awarded:',awardedseats_total,file=out)
    print('Seats per party:',file=out)
    print(party_seats_numbers,file=out)

    print(result_table,file=out)

   

    summary ={'Election':description,'Seats':seats,'Winning quotient divisors':winning_quotient_divisors,'Winning quotients':winning_quotients,'Party seat numbers':party_seats_numbers}

    with open(output_path, 'w') as outfile:
        json.dump(summary, outfile)


    return [seats,winning_quotient_divisors,winning_quotients,party_seats_numbers]


def leastvotechange(votetotals,number_of_seats,count_type = "listestemmetall"):

    #check that a valid election result type has been specified:
    valid_count_type = (("listestemmetall" in count_type) or ("stemmer" in count_type))
    if not valid_count_type:
        print('Error. Unknown result type. Valid result types are "listestemmetall" (vote totals) and "stemmer" (votes). Aborting.')
        return
    
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

    if count_type == "listestemmetall":
        required_votes_cast_decrease = required_vote_total_decrease/number_of_seats
        required_votes_cast_increase = required_vote_total_increase/number_of_seats
    elif count_type == "stemmer":
        required_votes_cast_decrease = required_vote_total_decrease
        required_votes_cast_increase = required_vote_total_increase

    quotient_loss_per_vote_total_transfer = 1 / divisor_seat_n
    quotient_gain_per_vote_total_transfer = 1 / divisor_seat_n_plus_one
    total_quotient_gap_change_per_vote_total_transfer = quotient_loss_per_vote_total_transfer + quotient_gain_per_vote_total_transfer

    print('quotient_loss_per_vote_total_transfer','%.5f'%quotient_loss_per_vote_total_transfer)
    print('quotient_gain_per_vote_total_transfer','%.5f'%quotient_gain_per_vote_total_transfer)
    print('total_quotient_gap_change_per_vote_total_transfer:','%.5f'%total_quotient_gap_change_per_vote_total_transfer)
    required_vote_total_transfer = quotient_difference / total_quotient_gap_change_per_vote_total_transfer

    if count_type == "listestemmetall":
        required_votes_transfer = required_vote_total_transfer/number_of_seats
    elif count_type == "stemmer":
        required_votes_transfer = required_vote_total_transfer
    else:
        Print('Unknown count type (Valid types are ''listestemmetall'' (vote totals) and ''stemmer'' (votes). Aborting.')
        return

    new_line1 = str(n)+'\t'+str(winner_seat_n)+'\t'+str(divisor_seat_n)+'\t'+'%.3f'%(quotient_seat_n)+'\n'
    new_line1 = new_line1.expandtabs(32)
    new_line2 = str(n+1)+'\t'+str(winner_seat_n_plus_one)+'\t'+str(divisor_seat_n_plus_one)+'\t'+'%.3f'%(quotient_seat_n_plus_one)+'\n'
    new_line2 = new_line2.expandtabs(32)
    result_table = result_table + new_line1 + new_line2

    print(result_table)
 
    print('quotient_difference: ','%.3f'%quotient_difference)
    print('\n')

    if count_type == "listestemmetall":
        print('Increase in vote total (listestemmetall) (not changing any existing votes) to party',winner_seat_n_plus_one,'needed to change election result:','%.3f'%required_vote_total_increase)
    print('Increase in votes cast (not changing any existing votes) for party',winner_seat_n_plus_one,'needed to change election result:',math.ceil(required_votes_cast_increase),',rounded up from','%.3f'%required_votes_cast_increase)
    print('\n')
    if count_type == "listestemmetall":
        print('Decrease in vote total (listestemmetall) (not changing any existing votes) to party',winner_seat_n,'needed to change election result:','%.3f'%required_vote_total_decrease)
    print('Decrease in votes cast (not changing any existing votes) for party',winner_seat_n,'needed to change election result:',math.ceil(required_votes_cast_decrease),',rounded up from','%.3f'%required_votes_cast_decrease)

    print('\n')
    if count_type == "listestemmetall":
        print('Vote total (listestemmetall) transferred from party',winner_seat_n,'to party',winner_seat_n_plus_one,'needed to change election result:','%.3f'%required_vote_total_transfer)
    print('Votes (stemmer) transferred from party',winner_seat_n,'to party',winner_seat_n_plus_one,'needed to change election result:',math.ceil(required_votes_transfer),',rounded up from','%.3f'%required_votes_transfer)
        
        
    return


#print('Bergen #1:')
#print('votetotals_bergen:')
#print(votetotals_bergen)
#distribute_seats(votetotals_bergen,number_of_seats_bergen,wait = False)

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

    party_seats_numbers1 = result1[-1]
    party_seats_numbers2 = result2[-1]

    if party_seats_numbers1 == party_seats_numbers2:
        print('Election outcomes are identical.')
        return True
    else:
        print('Election outcomes are different.')
        return False



def comparecounts(data_dictionary,data_dictionary_key):

    sub_dict = data_dictionary[data_dictionary_key]
    votes_precast_prelim = sub_dict["votesPrecastPrelim"]
    votes_electionday_prelim = sub_dict["votesElectionDayPrelim"]
    votes_precast_final =  sub_dict["votesPrecastFinal"]
    votes_electionday_final =  sub_dict["votesElectionDayFinal"]
    votes_final = sub_dict["votesElectionDayPrelim"]
    number_of_seats = sub_dict["numberOfSeats"]
    votetotals_final = sub_dict["voteTotals"]
    description = data_dictionary_key

    votes_sum_prelim = Counter(votes_precast_prelim) + Counter(votes_electionday_prelim)
    votes_sum_final = Counter(votes_precast_final) + Counter(votes_electionday_final)

    print('\n\n\n\n\nCalculating results for ',data_dictionary_key,'.')
    print('Result from preliminary vote counts:')
    result_prelim = distribute_seats(votes_sum_prelim,number_of_seats)
    print('From final vote totals (including personal votes):')
    result_final =  distribute_seats(votetotals_final,number_of_seats)
    print('From final vote counts (excluding personal votes):')
    result_final_no_personal_votes = distribute_seats(votes_sum_final,number_of_seats)


    print('Comparing ',description,'preliminary result to ',description,'final result:')
    is_identical1 = compareresults(result_prelim,result_final)

    
    print('Comparing ',description,'preliminary result to ',description,'final result WITHOUT PERSONAL VOTES (votetotal = #of ballots):')
    is_identical2 = compareresults(result_prelim,result_final_no_personal_votes)

    print('\n\n\n\n\nLeast vote change that would change ',description,'final result:')
    leastvotechange(votetotals_final,number_of_seats)


    print('\n\n\n\n\nLeast vote change that would change ',description,'preliminary result:')
    leastvotechange(votes_sum_prelim,number_of_seats,count_type = "stemmer")
    #leastvotechange(votes_sum_prelim,number_of_seats)
    return

#test_result = distribute_seats_wrapper(data_dict,"Drammen")

#comparecounts(data_dict,"Gjesdal")

comparecounts(data_dict,"Øksnes")


#Example data, from Ibestad kommune, 2019 election:
votecounts = {'Høyre':7876,'Arbeiderpartiet':4562,'Senterpartiet':3028}
number_of_seats = 19

def distribute_seats(votecounts,number_of_seats,first_divisor = 1.4):


print('Calculating election result from vote totals.')
print('Number of seats to be distributed: ',number_of_seats
print('First divisor':first_divisor)

awardedseats_total = 0
quotients = votecounts
divisors = dict.fromkeys(votecounts, 0)
seats = []
while awardedseats_total < number_of_seats:
    seatwinner = max(quotients, key=votecounts.get)
    seats.append(seatwinner)
    
    



distribute_seats(votecounts,number_of_seats)

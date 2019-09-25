# Election-stuff
Scripts for verifying/calculating election results, etc.

# Contents
This repository currently contains the following:

## notes.txt:
Personal notes and calculations/examples related to the question:
Given an election result (vote totals and resulting seat distribution), how to determine the smallest change in voting that would change
the seat distribution?

## settlement.py:
Functions for calculating and analyzing election results (seat distributions) according to Sainte Lagues (modified) method (https://en.wikipedia.org/wiki/Webster/Sainte-Lagu%C3%AB_method#Modified_Sainte-Lagu%C3%AB_method), plus example data.

Contains the following functions:
 
### distribute_seats()

Syntax:
```
distribute_seats(votetotals_in,number_of_seats,first_divisor = 1.4, wait = False,Verbose = False,adjustments = {})
```

#### Input:
Takes as input a dictionary of vote totals ("listestemmetall", or just votes/ballots if personal votes ("slengere") are not taken into account.) and the number of seats to be distributed.

Optionally, adjustments to the vote totals ("adjustments")  and the first divisor ("first_divisor") may be input.
Parameters 'Verbosity" adjusting amount of print output (True/False, default False) and 'Wait' (True/False, default False) enabling prompt for user input to proceed between awarding seats 

#### Output:
Prints a table of awarded seats, which party won the seat and the relevant divisors and quotients.
returns the following list: [seats,winning_quotient_divisors,winning_quotients,party_seats]
where:
seats: List of which party won each seat from first to last.
winning_quotient_divisors: List of the relevant divisor used to calculate the winning quotient for each seat. 
winning_quotients: List of the winning quotient for each seat.
party_seats: Dictionary containing the number of seats won by each party.
        
### leastvotechange()

Syntax: 
```
leastvotechange(votetotals,number_of_seats)
```
#### Input:
As for distribute_seats, but limited to vote totals and number of seats.
      
#### Output:
Runs distribute_seats() for number_of_seats (n) + 1 seats and determines how many votes must be added/subtracted/changed
for the winner of the n+1th seat to win the nth (last) seat. Prints the results.
      
### neededvotes()

Syntax: 
```
neededvotes(votetotals,number_of_seats,party, divisor = 1.4)
```
Determines how many additional votes (not changing any existing votes) a party not currently represented would need in order to win 1 seat.)

#### input:
votetotals,number_of_seats as for distribute_seats(). "Party" is a string containing a party name matching a key in the votetotals dictionary.
#### output:
Prints how many additional votes the party needs to win 1 seat, or a message if the party is already represented.
      
### compareresults()

Syntax: 
```
compareresults(result1,result2)
```
#### Input: 
Two election results (distribute_seats() return values).
#### Output: 
Determines if the election results (number of seats awarded to each party) are identical. Prints the result.
      

## Excel spreadsheets: Calculations and manually determined vote results (seat distributions) for a couple of local elections.


# TODO:
Might want to add support for reading data from and to files, for example JSON, or EML (Election Markup Language)?

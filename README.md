# Election-stuff
Scripts for verifying/calculating election results, etc. for norwegian elections. The functions are designed for use with data for municipial elections (kommunestyrevalg), but may also potentially be applicable to regional (fylkestingsvalg) and parliamentary (stortingsvalg) elections.


# Acknowledgements
* JSON input/output adapted from HNygards fork at https://github.com/HNygard/Election-stuff
* Much election results data was collected by HNygard: https://github.com/HNygard/valgprotokoller

# References

Lov om valg til Stortinget, fylkesting og kommunestyrer (valgloven): https://lovdata.no/dokument/NL/lov/2002-06-28-57

# Contents
This repository currently contains the following:

## data.json

Results from real local elections. Contains vote totals (listestemmetall) and the number of seats (to be) distributed in each election. Also contains additional data (e.g. preliminary and final vote counts) for some elections. 

## test_data.json 

Fictional data for test use.

## notes.txt:
Personal notes and calculations/examples related to the question:
Given an election result (vote totals and resulting seat distribution), how to determine the smallest change in voting that would change
the seat distribution?

## settlement.py:
Functions for calculating and analyzing election results (seat distributions) according to Sainte Lagues (modified) method (https://en.wikipedia.org/wiki/Webster/Sainte-Lagu%C3%AB_method#Modified_Sainte-Lagu%C3%AB_method), plus example data.

Contains the following functions:

### distribute_seats_wrapper()

Syntax:
```
distribute_seats_wrapper(data_dictionary,data_dictionary_key,first_divisor = 1.4, wait = False,verbose = False,adjustments = {}, silent = False,output_path = "output.json"):
```
Wraps the distribut_seats() function in order to allow data to be retrieved from a dictionary with data for multiple elections. Extracts desired data from a dictionary and passes to the distribute_seats function.

### distribute_seats()

Syntax:
```
distribute_seats(votetotals_in,number_of_seats,ballot_numbers = None,first_divisor = 1.4, wait = False,verbose = False,
                     adjustments = {}, silent = False,output_path = "output.json",description = "Unknown")
```

#### Input:

Mandatory arguments:
* votetotals_in:  dictionary of vote totals ("listestemmetall", or just votes/ballots if personal votes ("slengere") are not taken into account.)
* number_of_seats: the number of seats to be distributed

Optional arguments (default values):

* ballot_numbers (None). Dictionary of votes (ballots) recived by each party.
* first_divisor (1.4). The first divisor to be used in the modified Saint Lagues method.
* wait (False): Wait for user input to proceed between awarding seats.
* verbose (False): Display more printed output while processing.
* adjustments ({}): Dictionary of adjustments to vote totals to be applied to one or more parties, in relative numbers (e.g -100).
* silent (False): Perform the function with no printed output.
* output_path ("output.json"): Output file path.
* description ("Unknown"): A description of the data to be displayed when processing.


#### Output:
Prints a table of awarded seats, which party won the seat and the relevant divisors and quotients.

returns: [seats,winning_quotient_divisors,winning_quotients,party_seats_numbers]

where:
seats: List of which party won each seat from first to last.
winning_quotient_divisors: List of the relevant divisor used to calculate the winning quotient for each seat. 
winning_quotients: List of the winning quotient for each seat.
party_seats_numbers: Dictionary containing the number of seats won by each party.
        
### leastvotechange()

Syntax: 
```
leastvotechange(votetotals,number_of_seats,count_type = "listestemmetall")
```
#### Input:

Mandatory arguments:

* votetotals
* number_of_seats

Optional arguments (default values):

* count_type ("listestemmetall"): String specifying how votetotals shall be interpreted: As vote totals ("listestemmetall") 
 including adjustments for personal votes or as the number of votes (ballots) received ("stemmer"). Valid values are "listestemmetall" and "stemmer".
      
#### Output:
Runs distribute_seats() for number_of_seats (n) + 1 seats and determines how many votes must be added/subtracted/changed
for the winner of the n+1th seat to win the nth (last) seat. Prints the results.
  
 Returns: [required_vote_total_increase,required_votes_cast_increase,required_vote_total_decrease,required_votes_cast_decrease,required_vote_total_transfer] 
 
  
### neededvotes()

Syntax: 
```
neededvotes(votetotals,number_of_seats,party, divisor = 1.4)
```
Determines how many additional votes (not changing any existing votes) a party not currently represented would need in order to win 1 seat.)

#### input:

Mandatory arguments:

* votetotals
* number_of_seats
* party: String containing a party name matching a key in the votetotals dictionary.

Optional arguments (default values):

* divisor (1.4)

#### output:
Prints how many additional votes the party needs to win 1 seat, or a message if the party is already represented.

Returns: [required_votetotal_increase,required_vote_increase]

### compareresults()

Syntax: 
```
compareresults(result1,result2)
```
#### Input: 
Two election results (distribute_seats() return values).

Mandatory arguments:

* result1: First result to be compared.
* result2: Second result to be compared.

#### Output: 
Determines if the election results (number of seats awarded to each party) are identical. Returns True if yes, False if no. Prints the result.
     
 Returns: None (unable to compare results), True (results are identical) or False (results are not identical).
      
### comparecounts()

Syntax: 
```
comparecounts(data_dictionary,data_dictionary_key)
```

#### Input:

Mandatory arguments:

* data_dictionary
* data_dictionary_key

#### Output:

Returns: [is_identical1,is_identical2]


### personalvotesimpact()

Syntax: 
```
personalvotesimpact(data_dictionary,data_dictionary_key)
```

#### Input:

As for distribute_seats_wrapper(), but limited to data_dictionary and data_dictionary_key.

Data_dictionary must contain data for "slengere".


#### Output:


Returns TRUE if the election result is NOT changed by deleting personal votes (slengere).


## testing.py

Test code for automatic testing (unit tests) of the functions in settlement.py.

To run tests and generate test coverage report with coverage.py, use the following commands:
```
coverage run --include settlement.py testing.py
coverage report
coverage html
```

## electionclasses.py

Classes and methods to implement (some of) the same functionality in settlement.py

Includes the following classes:

### Contest

Represents a local election, for example "Kommunevalget i Drammen". 

 #### Important attributes
 
 * validcontestreport: The currently valid reported election data (votes).
 
 * number_of_seats: Number of seats (mandates) to be distributed in the election.
 
 #### Important methods
 
 * perform_settlement(): Calculates election result based on the current validcontestreport.

### Contestreport

Represents reported election data (votes).

#### Important attributes

* votetotals: Dictionary in format {party: votetotal (listestemmetall)}.

### Settlement

Represents and enables calculation of election result (distribution of seats). 

#### Important attributes

* votetotals

* number_of_seats

* awardedseats_total

* awardedseats

* first_divisor

#### Important methods

* distributeseats

### Candidateseat

Represents an awarded seat/mandate.

#### Important attributes

* seatwinner
* winning_quotient

## testing_objects.py

Test code for automatic testing (unit tests) of the classes/methods in electionclasses.py.

## Excel spreadsheets: 
Calculations and manually determined vote results (seat distributions) for a couple of local elections.

# TODO:
* Create Ipython/Jupyter notebook for easier/interactive use.

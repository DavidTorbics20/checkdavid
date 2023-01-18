# User story enter flight time

The user enters the time (a date) when it wants to make a trip. 
The are two options:
- the user enters two dates and from-to
  - bidirectional flight is automatically on
- the user enters one date
  - bidirectional flight is automatically off

## Actors 

+ User

## Input

Two or one dates are added to the table with the previous search results

## Internal state chage 

Table with previous searches saves flight times.

## Output

The table with the previous flights now also has the times for the flights

## Errors

+ Table not exists
+ No time given
+ Inpossible time given A
+ Inpossible time given B
+ Department is later than arrival
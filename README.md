# march-smart-coin

Small project based on the concept of flipping a coin to fill out a March Madness bracket. But I like to add a little twist, since certain matchups like the 1-16 don't feel right as a 50/50 coin flip.


Added rules are as follows: 
  * 1/16 chance for 16 to beat 1 seed.
  * 1/8 chance for 15 to beat 2 seed.
  * 1/4 chance for 14 to beat 3 seed.
  * 1/4 chance for 8 to beat 1 seed (if 1 seed survives 1st round).
  * All other matches are 1/2 for each seed to win.
  

Initial thought on output of this will be a string of 1's and 0's with 0 representing the team on the top of the matchup winning as viewed when looking at the bracket (not necessarily the top seeded team).
There would then be 4 of these strings with 15 numbers each, one for each section/division of the bracket. Then a final 3 number string for the Final Four and Championship.
(If this changes I'll totally remember to update this).

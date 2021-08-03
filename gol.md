I am making a food game where the goal of the game is to use up all the empty land and having at least 50% food and water may be a bonus goal. 

The game has a total of 6 states but is **initialized** to exclude the last state (food). States 0-5 are:

	0. Empty land = grey [p=0.35]

	1. Water = blue  [p=0.3]

	2. Plants = green [p=0.2]

	3. Chicken = orange [p=0.1]

	4. Cow = brown [p=0.05]

	5. Food = beige [p=0]

The probability of getting the states decreases as you move up in states so generating a cow is much more rare than generating land, until the final state (food) which has 0 probability of being generated in the initial data. 

**Rules** are as follows:

	• Animal cells without both food and water nearby dies and becomes a food cell :(

	• Plant cells without water nearby dies and becomes a food cell :(

	• Empty cells can become: 

		○ plants if it has at least 1 neighbor plant because of the neighbor's seeds

		○ chickens or cows if it has at least 2 neighbor chickens or cows because of reproduction. 

		○ In the case that more than 1 condition is met, the empty cell takes the highest state within the met conditions

	• Otherwise, cells remain unchanged

The **neighbors** are defined as a square around our cell (copied from previous part in lifeStu.py)

The global variable **states** is set to 6

The **grid size** is set to 60x60
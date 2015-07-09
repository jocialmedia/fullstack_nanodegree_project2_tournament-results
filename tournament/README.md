# Project 2 - Tournament Results

## Description

This is a script which simulates one to several tournaments in either elimination or swiss mode. All esults are saved in a postgres database and can be statisticaly analyzed.


This is the Startmenu:
![alt tag](https://raw.githubusercontent.com/jocialmedia/fullstack_nanodegree_project2_tournament-results/tournament_simulator_startmenu.png)

# Option 1. Run a new tournament.
This is an example for a Eliminaton tournament with 4 players:
![alt tag](https://raw.githubusercontent.com/jocialmedia/fullstack_nanodegree_project2_tournament-results/tournament_simulator_example-tournament-elimination.png)

If there are no players in the database, 32 players are created from a wide range of names and ages. They receive a random gender and random birthday:
![alt tag](https://raw.githubusercontent.com/jocialmedia/fullstack_nanodegree_project2_tournament-results/tournament_simulator_auto-create-players.png)

This is an example for a Swiss tournament with 4 players:
![alt tag](https://raw.githubusercontent.com/jocialmedia/fullstack_nanodegree_project2_tournament-results/tournament_simulator_example-tournament-swiss_1.png)
![alt tag](https://raw.githubusercontent.com/jocialmedia/fullstack_nanodegree_project2_tournament-results/tournament_simulator_example-tournament-swiss_2.png)


# Option 4. Install or reset the database.
It is easy to delete the whole data:
![alt tag](https://raw.githubusercontent.com/jocialmedia/fullstack_nanodegree_project2_tournament-results/tournament_simulator_database-reset.png)

# Option 2. Take a look at the statistics of tournaments.
![alt tag](https://raw.githubusercontent.com/jocialmedia/fullstack_nanodegree_project2_tournament-results/tournament_simulator_tournament_statistics.png)

# Option 3. Take a look at the statistics of players.
![alt tag](https://raw.githubusercontent.com/jocialmedia/fullstack_nanodegree_project2_tournament-results/tournament_simulator_player_statistics.png)

# Option 5. Show info about this project.
Self-explanatory without Screenshot.

# Option 6. Quit the simulator.
Self-explanatory without Screenshot.



## Installation

1. Make sure you have Git and Python installed on your computer. In case, you run into trouble getting Git, Python, Vagrant and Postgresql to run on your computer please take a look at this [detailed instructions](https://docs.google.com/a/knowlabs.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true) by udactiy.

2. Clone the original code from the Udacity Git-Repository to your local machine:
```
git clone https://github.com/udacity/fullstack-nanodegree-vm.git
```

3. Clone the code from this repository to your local machine:
```
git clone jocialmedia/fullstack_nanodegree_project2_tournament-results.git
```

4. Now copy the following files from fullstack_nanodegree_project2_tournament/tournament/
to the directory vagrant/tournament from udacity:
```
tournament.py
tournament.sql
tournament_ressources.json
tournament_test.py
```

5. Go to the directory with the file **Vagrantfile** and start the vagrant server with:
```
vagrant up
```

6. Log in to the server with:
```
vagrant ssh
```

7. Go to the directory of the project tournament 
```
cd /vagrant/tournament
```

8. Log in to the Postgresql-Database:
```
psql
``` 

9. The following command imports the whole content of **tournament.sql** into the database:
```
\i tournament.sql
```

10. Now you can log out of psql
```
\q
```

11. And when you are still in the right project directory you can start the program with python:
```
python tournament.py
```

12. The same way you can start the testing file:
```
python tournament_test.py
```


## Testing

In order to work with the large modifications to the code base I had to do some changes on the tournament_test.py as well. I also had to use a little trick because every time I imported tournament.py into tournament_test.py the automatic menu function started before the testing process. That is why I copied the file tournament.py to tournament_for_testing.py and deactivated the last two lines to prevent the menu from starting.

This is the testing after a successful run:
![alt tag](https://raw.githubusercontent.com/jocialmedia/fullstack_nanodegree_project2_tournament-results/tournament_simulator_testing_successful.png)


This is the testing after one of the tests was manipulated to fail:
![alt tag](https://raw.githubusercontent.com/jocialmedia/fullstack_nanodegree_project2_tournament-results/tournament_simulator_testing_not-successful.png)


##### Which additional resources did you use?
* [Udacity](https://www.udacity.com/course/nd004) (Code fragments)
 

 
## This was done for [Project 2 - Movie Trailer Website]
as part of the [Full Stack Web Developer Nanodegree at Udacity.com](https://www.udacity.com/course/nd004) 
June 2015
More Information at [Github](https://github.com/jocialmedia/fullstack_nanodegree_project2_tournament-results)
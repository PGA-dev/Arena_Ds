# Arena_Ds

### MVC Battlegame for python
## PGA

### Concept
This project began as a merging of two simple ideas: 
1. How can I make a version of our NuCamp intro to Python game, that doesn't suck
2. How can I incorporate MVC design patterns into the game

Origally I developed the basic design from G. Debidda's MVC patterns article series (originally a simple 3 field--table--usage, but fairly useful as a character creation approach if re-designed...so a nod to GD for the great insight on how to use this useful design pattern in a simple, practical way to understand at the intermediate level): https://www.giacomodebidda.com/posts/mvc-pattern-in-python-dataset/  4-15-2017 (date of article) However, I really wanted to take this approach a step further and customize the calls a bit. This version thus becomes a variation to practice PostGreSQL and SQLAlchemy; making a few necessary changes in the overall design pattern. The original DB adaptation, based upon a use of SQLite3 and Dataset, is only relevant as a basic design, requiring the structure of the connections and the overall call design to change rather dramatically as the call adaptation patterns are employed. The other design issue that is changed is the initial seeding of the database; in this new version, it will be done as a separate proceedure.
### Technology Used
* Python
* Basic MVC design pattern 
* PostGreSQL
* SQLAlchemy

#### Files included/ Separation of Concerns:
1. Original Battlegame.py from NuCamp's week1 python classes (for README reference ease)
2. This README
3. The Arena game's driver code
4. dunder init file (my favorite)
5. basic helper methods file: arena_method.py
6. Backend CRUD
7. Exceptions file
8. Controller
9. Model
10. View
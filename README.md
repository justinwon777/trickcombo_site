# TrickCombo
Link: https://trickcombo.herokuapp.com/

## About

TrickCombo is a site for exploring tricking combos in ways you may have never thought of before. The main feature is a combo generator that is personalizable with numerous settings and uses the rules of tricking to form logical combos instead of randomly putting tricks together.

### Features
- Generate combos by selecting your favorite tricks, stances, and transitions
- Extra options include starting trick, finishing trick, spin limit, and combo length
- Save trick sets and combos in your profile
- Edit combos by hand or regenerating individual parts of it
- Combo builder that lets you see all possible combinations and make your own combos from scratch

### Technical Highlights
- Bidirectional, cyclic graph implemented with dictionaries using data parsed from a spreadsheet
- Depth-first search algorithm used to traverse graphs forwards, backwards, and finish incomplete paths
- Full stack, dynamic website created with the tech stack below

### Tech Stack
- Django (Python) backend
- JavaScript, jQuery, Bootstrap, HTML, and CSS frontend
- PostgreSQL
- Heroku for deployment
- Newer version uses Vue.js for frontend (work in progress)


## Quick tricking theory for non-trickers
Tricking is a sport made of different movements called "tricks", which can be put together with "stances" and "transitions" in a sequence to make a combo. Combos follow a structure like this: (trick -> stance -> transition -> trick -> stance -> transition -> repeat). Not all tricks, stances, and transitions can follow each other. There are rules that determine what can follow what, which is where the generator comes into play.

## Combo Generator

The key points for the generator are its customizability and use of a graph traversal algorithm to create combos. Using a spreadsheet containing tricks and their properties, a graph is implemented using dictionaries. Generator settings from user input can manipulate the graph to optimize efficiency of the search algorithm. With the custom graph, a DFS algorithm finds a path (if possible) within it and returns it to the user.

## Combo Builder

The buidler serves as a rudimentary visualization of the graph. Users can select tricks and the builder shows all possibilties that can come after it, letting the user pick every part of the combo.
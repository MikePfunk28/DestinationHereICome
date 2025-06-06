#!/bin/bash
python main.py <<EOF
go north
go east
look
go west
go south
look
go somewhere
take something_nonexistent
go down
look
attack diseased rat
a
a
a
go up
go north
go west
look
look at wall
look at marking
look at rubble
look at ceiling
talk old man hemlock
go east
go further west
attack scrawny thug
a
a
a
a
a
a
quit
EOF

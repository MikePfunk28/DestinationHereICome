#!/bin/bash
python main.py <<EOF
look
talk wary informant
accept package
status
go down
look
attack diseased rat
a
a
a
look
take sealed package
inv
go up
look
talk wary informant
complete package
status
go north
go east
look
upgrade hideout
status
go west
go further west
look
attack scrawny thug
a
a
a
a
a
a
look
take 5_coins
take crude_shiv
inv
go east
go south
look
talk wary informant
status
quit
EOF

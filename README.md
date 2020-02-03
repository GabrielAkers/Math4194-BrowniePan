# Math4194-BrowniePan

Set color grades to 8 for the Z, 125 for everything else
Set the correct params 'poly' or 'rr' where the Sim instance is created. I've provided some example polygons, EQ_TRI, SQ, PENT, HEX, Z
The radius slider controls the radius of the rounded rects

N-ew image (this starts the simulation on that geometry)

S-top the simulation

G-ather data

Accessing pixels is super innefficient so for high color grade values the simulation runs really slowly. Given more time I'd rewrite it to use PixelArray instead, but this was just easier to do in a day.

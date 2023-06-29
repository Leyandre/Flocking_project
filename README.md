# Flocking_project

This project simulate the natural behavior of birds and other herd-type animals
For each "bird", the program calculate the evolution of direction and velocity depending on what it sees.

The stirring on the direction follows 3 values, concerning all the birds in sight (the flock) :

  - Firstly, the barycenter of the flock
  - Secondly, the average direction the flock
  - Thirdly, the barycenter's opposite of the birds in its vital space

The acceleration depends on the distance to the aims, such as the flock where it wants to go and the walls and birds (individually)
where that it doesn't want to hit.


I set a bird's coloration so that we can observe what one can see. The deep blue one is the subject, the light blue ones are in sight, the green ones are in its vital space and the red ones does are not taking care of.

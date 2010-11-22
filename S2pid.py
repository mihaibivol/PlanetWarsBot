#!/usr/bin/env python
#

"""
// The DoTurn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist. Inside this function, you issue orders using the
// pw.IssueOrder() function. For example, to send 10 ships from planet 3 to
// planet 8, you would say pw.IssueOrder(3, 8, 10).
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own. Check out the tutorials and articles on the contest website at
// http://www.ai-contest.com/resources.
"""

from PlanetWars import PlanetWars

NEUTRAL = 0
MYSELF = 1
ENEMY = 2

#returns number of ships from enemy fleets heading to a planet
#arguments PlanetWars pw, Planet p
def IncomingShips(pw, p):
  enemy_fleets = pw.EnemyFleets()
  r = 0;
  for f in enemy_fleets:
    if f.DestinationPlanet() == p.PlanetID():
      r += f.NumShips()
  return r;

#returns number of ships from my fleets heading to a planet
#arguments PlanetWars pw, Planet p
def OutgoingShips(pw, p):
  my_fleets = pw.MyFleets()
  r = 0;
  for f in my_fleets:
    if f.DestinationPlanet() == p.PlanetID():
      r += f.NumShips()
  return r;
                   
def DoTurn(pw):
 
  my_planets = pw.MyPlanets()
  enemy_planets = pw.EnemyPlanets()
  not_my_planets = pw.NotMyPlanets()

  #returns distance between 2 planet objects
  def distance(planet1, planet2):
    return pw.Distance(planet1.PlanetID(), planet2.PlanetID())

  #returns the number of NumShips needed to take over a planet
  #arguments Planet p
  def Cost(p):
    r = 0
    my_fleets = pw.MyFleets()
    if p.Owner() == NEUTRAL:
      r = p.NumShips() - OutgoingShips(pw, p)
    if p.Owner() == ENEMY:
      minD = 100000.0
      for mp in my_planets:
        if distance(mp,p) < minD:
          planet = mp
          minD = distance(mp,p)
      r = p.NumShips() + p.GrowthRate() * minD - OutgoingShips(pw, p)
    r += 0.001
    return r
  
  #returns the time needed to take over a planet
  #arguments Planet p
  def Time(p):
    my_planets_sorted = sorted(my_planets, key = lambda mp: distance(mp,p))
    deployed_ships = 0
    cost = Cost(p)
    r = -1
    for mp in my_planets_sorted:
      num_ships = mp.NumShips()
      num_ships -= IncomingShips(pw,mp)
      if p.Owner() == NEUTRAL:
        num_ships = min(cost + num_ships/10 ,num_ships / 2)
      else:
        num_ships/=2
      deployed_ships += num_ships
      if deployed_ships > cost:
        r = distance(p,mp)
        break
    r += 0.001
    return r
    
  #not my planets sorted
  nmp_sorted = sorted(not_my_planets, key = lambda fct: Cost(fct))
##  frontier_planets = []
##  support_planets = []
  for nmp in nmp_sorted:
    cost = Cost(nmp)
    my_planets_sorted = sorted(my_planets, key = lambda mp1: distance(mp1,nmp))
    for mp in my_planets_sorted:
      if cost < 0:
        break
##      if not mp in frontier_planets:
##        frontier_planets.append(mp)
      num_ships = mp.NumShips()
      num_ships -= IncomingShips(pw,mp)
      if nmp.Owner() == NEUTRAL:
        if num_ships / 2 > cost / 4:
          num_ships /= 2
        else:
          num_ships = 0
      else:
        if num_ships / 2 > cost / 3:
          num_ships /= 2
        else:
          num_ships = 0
      if num_ships > 1:
        pw.IssueOrder(mp.PlanetID(),nmp.PlanetID(),num_ships)
        mp._num_ships -= num_ships
        cost -= num_ships
##  for mp in my_planets:
##    if not mp in frontier_planets:
##      support_planets.append(mp)
##  frontier_planets = sorted(frontier_planets, key = lambda fp: fp.NumShips())
##  for fp in frontier_planets:
##    for sp in support_planets:
##      pw.IssueOrder(sp.PlanetID(),fp.PlanetID(),sp.NumShips()/2)
  return



def main():
  map_data = ''
  while(True):
    current_line = raw_input()
    if len(current_line) >= 2 and current_line.startswith("go"):
      pw = PlanetWars(map_data)
      DoTurn(pw)
      pw.FinishTurn()
      map_data = ''
    else:
      map_data += current_line + '\n'


if __name__ == '__main__':
  try:
    import psyco
    psyco.full()
  except ImportError:
    pass
  try:
    main()
  except KeyboardInterrupt:
    print 'ctrl-c, leaving ...'

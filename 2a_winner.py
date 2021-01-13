import collections
import re
import math
 
class player:
    def __init__(self, splayer_name):
        self.splayer_name = splayer_name
        self.point = 0
        self.rounds = {}
    
    def add_point(self, round, npoint):
        self.point = self.point + npoint
        self.rounds[round] = npoint
        #print(round, ' in2 ', npoint)
        
    def find_first_round(self, npoint):
        ntmp_point = 0
        nres = 9999
        for nround, point in self.rounds.items():
            ntmp_point = ntmp_point + point
            #print (ntmp_point)
            if ntmp_point >= npoint:
                nres = nround
                break
        #print (nres)
        return nres
    
    def __gt__ (self, other):
        return (self.point > other.point) or (self.point == other.point and self.find_first_round(self.point) < other.find_first_round(other.point))
    def __lt__ (self, other):
        return (self.point < other.point) or (self.point == other.point and self.find_first_round(self.point) > other.find_first_round(other.point))
    def __eq__ (self, other):
        return self.point == other.point and self.find_first_round(self.point) == other.find_first_round(other.point)
 
def find_best_player(players):
    sbst_player_name = ''
    players_val = players.values()
    players_val = sorted(players_val, key=lambda player: player)
    sbst_player_name = players_val[len(players_val)-1].splayer_name
    return sbst_player_name
    
    
players = {}
 
sstorage_path = 'params_2a'
nrounds = int(input())
    
for nround in range(1,nrounds+1,1):
    line = input()
    match = re.findall(r'(\S+)', line)
    rate1 = match[0]
    rate2 = int(match[1])
    if players.get(rate1) is None:
        tmpPlayer = player(rate1)
        players[rate1] = tmpPlayer
    #print(nround, ' in1 ', rate2)
    players[rate1].add_point(nround, rate2)
print(find_best_player(players))
 
#f.close()
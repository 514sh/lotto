
class Entries:
    def __init__(self, sender="", all=[]):
        self.__sender = sender
        self.__all = all

    @property
    def sender(self):
        return self.__sender
    
    @property
    def all(self):
        return self.__all
    
    def __guesses(self, line, winning_number):
        combinations = line.split(",")
        combinations = combinations[0:3]
        guesses = 0
        for number in winning_number:
            for combination in combinations:
                if number == int(combination):
                    guesses += 1
        return guesses
    
    def result_raw(self, winning_number):
        my_winners = list()
        my_tie = list()
        total_bet = 0
        for entry in self.all:
            split = entry.split("@$")
            key = split[4]
            total_bet += int(split[5])
            guesses = self.__guesses(line=key, winning_number=winning_number)
            if guesses == 2:
                my_tie.append(entry)
            elif guesses > 2:
                my_winners.append(entry)
        return my_winners, my_tie, total_bet, [ str(i) for i in winning_number ]

    def result(self, winning_number, limit, other_entries):
        if other_entries.sender == "agustin":
            pasok = self.get_pasok_for_laban_agustin(other_entries, limit)
        else:
            pasok = self.pasok(limit=limit)
        my_winners = list()
        my_tie = list()
        total_bet = 0
        for key in pasok:
            guesses = self.__guesses(line=key, winning_number=winning_number)
            total_bet += int (pasok[key])
            if guesses == 2:
                my_tie.append(f"{key}{pasok[key]}")
            elif guesses > 2:
                my_winners.append(f"{key}{pasok[key]}")
        return my_winners, my_tie, total_bet, [ str(i) for i in winning_number ]

    @property 
    def __keys(self):
        my_dict = dict()
        my_pasok = dict()
        for entry in self.all:
            split = entry.split("@$")
            key = split[4]
            if key in my_dict:
                my_dict[key].append(entry)
                my_pasok[key] += int(split[5])
            else:
                my_dict[key] = [entry]
                my_pasok[key] = int(split[5])
        return my_dict, my_pasok
    
    @property
    def my_pasok_no_limit(self):
        return self.__keys[1]
    
    # SPECIAL CASE: PASOK FOR LABAN_AGUSTIN PREVIOUS VERSION
    def get_pasok_for_laban_agustin_previous(self, other_entries, limit: int):
        other_pasok = other_entries.my_pasok_no_limit
        pasok = self.my_pasok_no_limit
        new_pasok = dict()
        for entry in pasok:
            if entry in other_pasok:
                if pasok[entry] > limit:
                    new_pasok[entry] = min(10, pasok[entry] - limit)
            else:
                new_pasok[entry] = min(pasok[entry], 10)
        return new_pasok
    
    def get_pasok_for_laban_agustin(self, other_entries, limit: int):
        limit = 10  #limit is hardcoded to 10
        pasok = self.my_pasok_no_limit
        new_pasok = dict()
        for entry in pasok:
            if pasok[entry] > limit:
                new_pasok[entry] = min(limit, pasok[entry] - limit)
            else:
                new_pasok[entry] = min(pasok[entry], limit)
        return new_pasok
        
    @property
    def bookies(self):
        my_bookies = dict()
        for entry in self.all:
            split = entry.split("@$")
            bookie = split[6].replace("@", "").strip()
            bet = int(split[5])
            if bookie in my_bookies:
                my_bookies[bookie] += bet
            else:
                my_bookies[bookie] = bet
        return my_bookies

    def pasok(self, limit):
        my_pasok = self.__keys[1]
        if not limit:
          return my_pasok
        else:
          for key in my_pasok:
              if limit < my_pasok[key]: 
                my_pasok[key] = limit
        return my_pasok

    @property
    def duplicates(self):
        my_dict = self.__keys[0]
        duplicates = list()
        for key in my_dict:
            if len(my_dict[key]) > 1:
                duplicates.append(my_dict[key])
        return duplicates

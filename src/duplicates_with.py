from entries import *
from datetime import *
today = datetime.now()

class DuplicatesWith:
    def __init__(self, entries=Entries, other=Entries):
        self.__entries = entries
        self.__other = other

    @property
    def entries(self):
        return self.__entries
    
    @property
    def other(self):
        return self.__other

    def lines(self, limit):
        pasok = self.entries.pasok(limit)
        other_pasok = self.other.pasok(limit)
        lines = [f"DUPLICATES: {self.__timestr}"]
        lines.append(f"{self.entries.sender:<20}{self.other.sender}")
        total_bet1, total_bet2 = 0, 0
        for key in pasok:
            if key in other_pasok:
                left, right = f"{key}{pasok[key]}" , f"{key}{other_pasok[key]}"
                lines.append(f"{self.__formatted_line(line=left):<20}{self.__formatted_line(line=right)}")
                total_bet1 += pasok[key]
                total_bet2 += other_pasok[key]    
        lines.append(f"TOTAL BET: {total_bet1:<9}TOTAL BET: {total_bet2}")
        return lines, total_bet1, total_bet2
    
    def __formatted_line(self, line):
        numbers = line.split(',')
        formatted_numbers = [f'{int(num):02}' for num in numbers]
        return ' '.join(formatted_numbers)

    def write(self, limit,  base_dir=""):
        filename = f"{base_dir}duplicates/{self.__timestr}_duplicates_{self.entries.sender}_{self.other.sender}.txt"
        lines = self.lines(limit)[0]
        with open(filename, "w", encoding="utf-8") as my_file:
          for line in lines:
              my_file.write(line)
              my_file.write("\n")

    @property
    def __timestr(self):
        return today.strftime("%m_%d_%Y")
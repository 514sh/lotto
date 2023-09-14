import re
from datetime import *
today = datetime.now()

class Status:
    CORRECT = "CORRECT"
    WRONG_LENGTH = "WRONG_LENGTH"
    WRONG_COMBINATION_FORMAT = "WRONG_COMBINATION_FORMAT"
    WRONG_BET_FORMAT = "WRONG_BET_FORMAT"
    BOOKIE = "BOOKIE"
    NO_NUMBER = "NO_NUMBER"
    ON_ANOTHER_FILE = "ON_ANOTHER_FILE"

class FileProcessor:
    def __init__(self, base_dir="", sender=""):
        self.__base_dir = base_dir
        self.__wrong_input = list()
        self.__sender = sender
        #key = 0:status , 1:line number , 2:entry , 3:sender, 4:combination key , 5:bet, 6:bookie

    @property
    def sender(self):
        return self.__sender

    @property
    def base_dir(self):
        return self.__base_dir

    def read_input(self):
        filename = f"{self.base_dir}input/{self.__timestr}_{self.sender}.txt"
        line_number = 0
        my_list = list()
        with open(filename, encoding="utf-8") as my_file:
            current_bookie = ""
            for line in my_file:
                line_number += 1
                line = line.rstrip()
                status = self.status(line)
                if status == Status.NO_NUMBER:
                    continue
                key = f"{status}@${line_number}@${line}@${self.sender}"
                if status == Status.CORRECT:
                    key += f"@${self.__key(line)}@${current_bookie}"
                    my_list.append(key)
                    continue
                if status == Status.BOOKIE:
                    current_bookie = line
                    continue
                self.__wrong_input.append(key)
        return my_list
    
    def print_wrong_input(self):
        if len(self.__wrong_input) == 0:
            print(f"No wrong input for {self.sender}\n")
        else:
            print(f"WRONG INPUT ON {self.sender}")
            for entry in self.__wrong_input:
                split = entry.split("@$")
                print(f"  - {self.sender} @ Line number {split[1]} : '{split[2]}' with status: {split[0]}")
            print("\n")

    def write_tulog(self, duplicates):
        filename = f"{self.base_dir}tulog/{self.__timestr}_tulog_{self.sender}.txt"
        prev_tulog = self.__read_tulog(filename=filename)
        with open(filename, "w", encoding="utf-8") as my_file:
          my_file.write(f"Latest update: Tulog Entries for {self.sender}\n\n")   
          for key in duplicates:
            for entry in key:
                entry = entry.split("@$")
                if entry[2] not in prev_tulog and len(prev_tulog) != 0:
                    my_file.write("***NEW***\n")
                my_file.write(entry[2])
                my_file.write("\n")
            my_file.write("\n")

    def write_kabo(self, bookies):
        filename = f"{self.base_dir}kabo/{self.__timestr}_kabo_{self.sender}.txt"
        total = 0
        with open(filename, "w", encoding="utf-8") as my_file:
            my_file.write(f"KABO ENTRIES: {self.sender} {self.__timestr}\n\n")
            
            for key in bookies:
                my_file.write(f"{key:<20}:  {bookies[key]}\n")
                total += int(bookies[key])
            my_file.write(f"TOTAL{' ':<15}:  {total}")

    def __read_tulog(self, filename):
        prev_tulog = set()
        try:
          with open(filename, encoding="utf-8") as my_file:
            for line in my_file:
                line = line.rstrip()
                if line == "":
                    continue
                prev_tulog.add(line)
        except FileNotFoundError:
          with open(filename, "w", encoding="utf-8") as my_file:
              pass  
        return prev_tulog
    
    def write_result_raw(self, result):
        filename = f"{self.base_dir}result/{self.__timestr}_result_raw_{self.sender}.txt"
        winner_total, tie_total = 0, 0
        with open(filename, "w", encoding="utf-8") as my_file:
            my_file.write(f"RESULT: {self.sender} {self.__timestr}\n")
            my_file.write(f"WINNING COMBINATION: {'-'.join(result[3])}\n\n")
            my_file.write("WINNERS\n")
            for winner in result[0]:
                split = winner.split("@$")
                my_file.write(f"{split[2]:<25}KABO: {split[6].replace('@', '').strip()}\n")
                winner_total += int(split[5])
            my_file.write(f"\nTOTAL BET :  {winner_total}\n")
            my_file.write("\n\n")
            my_file.write("DRAW\n")
            for tie in result[1]:
                split = tie.split("@$")
                my_file.write(f"{split[2]:<25}KABO: {split[6].replace('@', '').strip()}\n")
                tie_total += int(split[5])
            my_file.write(f"\nTOTAL BET :  {tie_total}\n\n\n")

            my_file.write(f"REMIT: {self.sender} {self.__timestr}\n")
            remit = result[2] * 0.55 - tie_total
            my_file.write(f"{result[2]} * 0.55 - {tie_total} = {remit:.2f}")


    def write_result(self, result, minus_sender, total_duplicates_with=0):
        filename = f"{self.base_dir}result/{self.__timestr}_result_{self.sender}.txt"
        winner_total, tie_total = 0, 0
        with open(filename, "w", encoding="utf-8") as my_file:
            my_file.write(f"RESULT: {self.sender} {self.__timestr}\n")
            my_file.write(f"WINNING COMBINATION: {'-'.join(result[3])}\n\n")

            my_file.write("WINNERS\n")
            for winner in result[0]:
                line = winner.split(",")
                bet = int(line[3])
                line = self.__formatted_line(line=winner)
                my_file.write(f"{line}\n")
                winner_total += bet
            my_file.write(f"\nTOTAL BET :  {winner_total}\n")
            my_file.write("\n\n")
            my_file.write("DRAW\n")
            for tie in result[1]:
                line = tie.split(",")
                bet = int(line[3])
                line = self.__formatted_line(line=tie)
                my_file.write(f"{line}\n")
                tie_total += bet
            my_file.write(f"\nTOTAL BET :  {tie_total}\n\n\n")
            my_file.write(f"REMIT: {self.sender} {self.__timestr}\n")
            if minus_sender == self.sender and self.format != 42:
              remit = (result[2] - total_duplicates_with) * 0.55 - tie_total
              my_file.write(f"({result[2]} - {total_duplicates_with} ) * 0.55 - {tie_total} = {remit:.2f}")
            elif minus_sender != self.sender and self.format != 42:
              remit = result[2]  * 0.55 - tie_total
              my_file.write(f"{result[2]} * 0.55 - {tie_total} = {remit:.2f}")
            elif minus_sender != self.sender and self.format == 42:
              remit = result[2]  * 0.55
              my_file.write(f"{result[2]} * 0.55 = {remit:.2f}")
            else:
              remit = (result[2] - total_duplicates_with) * 0.55
              my_file.write(f"({result[2]} - {total_duplicates_with} ) * 0.55 = {remit:.2f}")


    def __formatted_line(self, line):
        numbers = line.split(',')
        formatted_numbers = [f'{int(num):02}' for num in numbers]
        return ' '.join(formatted_numbers)

    @property
    def format(self):
        if self.__weekday in [0,2,4]:
            return 45
        elif self.__weekday in [1,3,6]:
            return 49
        else:
            return 42
        
    def status(self, line):
        entry = self.__split_entry(line)
        if line.startswith("@"):
            return Status.BOOKIE
        elif len(entry) == 0 or len(entry) == 1:
          return Status.NO_NUMBER
        elif len(entry) != 4:
            return Status.WRONG_LENGTH
        elif self.__wrong_combination_format(entry):
            return Status.WRONG_COMBINATION_FORMAT
        elif int(entry[3]) % 5 != 0:
            return Status.WRONG_BET_FORMAT
        else:
            return Status.CORRECT

    def __key(self, line):
        split_entry = self.__split_entry(line)
        split_entry = [int(i) for i in split_entry]
        combination = sorted(split_entry[0:3])
        key = ""
        for number in combination:
            key += f"{number},"
        key += f"@${split_entry[3]}"
        return key

    @property
    def __weekday(self):
        return today.weekday()
    
    def __split_entry(self, line):
        split_entry = re.split("[^0-9]", line)
        split_entry = [i for i in split_entry if i!= ""]
        return split_entry
    
    def __wrong_combination_format(self, entry):
        combination = [int(i) for i in entry]
        combination = set(combination[0:3])
        if len(combination) != 3:
            return True
        for number in combination:
            if number > self.format or number <= 0:
                return True
        return False

    @property
    def __timestr(self):
        return today.strftime("%m_%d_%Y")
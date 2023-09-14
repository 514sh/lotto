from file_processor import *
from entries import *
from duplicates_with import *
from whatsapp_bot import *
from datetime import *
today = datetime.now()


def choose():
    print("What output do you want to get?")
    print("  -- 1: Tulog")
    print("  -- 2: Duplicates and Kabo Entries")
    print("  -- 3: Result")
    
    try:
        choice = int(input("Enter your choice (1/2/3): "))
        return choice
    except ValueError:
        print("Invalid input. Please enter 1, 2, or 3.")
        return choose()

def get_winning_number():
    print("Enter winning numbers for today...")

    my_numbers = list()
    for i in range(1,7):
        number = int(input(f"Winning number {i}: "))
        my_numbers.append(number)
    return my_numbers

def to_continue():
    answer = input(f"Would you like to continue? y/n: ")
    answer = answer.strip()
    if answer.lower() == "y" or answer.lower() == "yes":
        return True
    else:
        return False
    
def send_to_whatsapp():
    answer = input(f"Would you like send to whatsapp automatically? y/n: ")
    answer = answer.strip()
    if answer.lower() == "y" or answer.lower() == "yes":
        return True
    else:
        return False

def send_now(contact_name, file_path):
    whatsapp_bot = WhatsAppBot()
    whatsapp_bot.send_messages_from_file(contact_name, file_path)
    whatsapp_bot.close() 

def timestr():
    return today.strftime("%m_%d_%Y")

def main():
    senders = ["agustin", "bryan", "laban_bryan"]
    winning_number = [12, 41, 30, 22, 43, 24]
    contacts = ['"Astig group👋 A.K.A 🤫BOY TABAS"',
                '"👊laban"',
                '"Balik duplicate"'
                ]
    while True:
        chosen = choose()
        all_entries = []
        all_analyzer = []
        auto_send = send_to_whatsapp()
        for sender in senders:
            
            analyzer = FileProcessor(sender=sender)
            all = analyzer.read_input()
            entries = Entries(all=all, sender=sender)
            if chosen == 1:
              analyzer.print_wrong_input()

            duplicates = entries.duplicates
            analyzer.write_tulog(duplicates=duplicates)

            all_entries.append(entries)
            all_analyzer.append(analyzer)

            if auto_send and chosen == 1:
                file_path = f"tulog/{timestr()}_tulog_{sender}.txt"
                if sender == "laban_bryan":
                  send_now(contact_name=contacts[1], file_path=file_path)
                else:
                  send_now(contact_name=contacts[0], file_path=file_path)
            
        if chosen == 2 or chosen == 3:
            limit = int(input("What is the limit? "))
            duplicates_with = DuplicatesWith(entries=all_entries[0], other=all_entries[1])
            duplicates_with.write(limit=limit)  
            total_duplicates_with = min(duplicates_with.lines(limit=limit)[1], duplicates_with.lines(limit=limit)[2])
            
            if auto_send and chosen == 2:
                file_path = f"duplicates/{timestr()}_duplicates_{senders[0]}_{senders[1]}.txt"
                send_now(contact_name=contacts[2], file_path=file_path)

            
            bookies = all_entries[2].bookies
            all_analyzer[2].write_kabo(bookies=bookies)
            if auto_send and chosen == 2:
                file_path = f"kabo/{timestr()}_kabo_{senders[2]}.txt"  # Replace with the path to your message file
                send_now(contact_name=contacts[1], file_path=file_path)

            if chosen == 3:
                winning_number = get_winning_number()
                
                for index in range(len(all_entries)):
                    if index == 2:
                        limit = False
                    result = all_entries[index].result(winning_number=winning_number, limit=limit)
                    all_analyzer[index].write_result(result= result, minus_sender="agustin", total_duplicates_with=total_duplicates_with)
                    
                    if auto_send:
                      file_path = f"result/{timestr()}_result_{senders[index]}.txt"
                      if index == 2:
                        send_now(contact_name=contacts[1], file_path=file_path)
                      else:
                        send_now(contact_name=contacts[0], file_path=file_path)
                      
                    if index == 2:
                        result_raw = all_entries[index].result_raw(winning_number=winning_number)
                        all_analyzer[index].write_result_raw(result=result_raw)

                        if auto_send:
                          file_path = f"result/{timestr()}_result_raw_{senders[index]}.txt"  # Replace with the path to your message file
                          send_now(contact_name=contacts[1], file_path=file_path)

        if not to_continue():
            break
                    

main()

# analyzer.print_wrong_input()
# other_analyzer.print_wrong_input()

# duplicates = entries.duplicates
# other_duplicates = other_entries.duplicates

# analyzer.write_tulog(duplicates=duplicates)
# other_analyzer.write_tulog(duplicates=duplicates)

# duplicates_with = DuplicatesWith(entries=entries, other=other_entries)
# duplicates_with.write(limit=15)
# total_duplicates_with = min(duplicates_with.lines(limit=15)[1], duplicates_with.lines(limit=15)[2])

# laban_analyzer = FileProcessor(sender="laban_bryan")
# output = laban_analyzer.read_input()
# laban_entries = Entries(all=output, sender="laban_bryan")
# bookies = laban_entries.bookies
# laban_analyzer.write_kabo(bookies=bookies)
# result_raw = laban_entries.result_raw(winning_number=winning_number)

# laban_analyzer.write_result_raw(result=result_raw)


# other_analyzer.write_result(result=result, total_duplicates_with=total_duplicates_with, minus_sender="agustin")
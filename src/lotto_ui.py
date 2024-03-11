from file_processor import *
from entries import *
from duplicates_with import *
from whatsapp_bot import *
from datetime import *
import os
from dotenv import load_dotenv
load_dotenv()

today = datetime.now()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def choose():
    print("What output do you want to get?")
    print("  -- 1: Tulog")
    print("  -- 2: Duplicates and Kabo Entries")
    print("  -- 3: Result")
    
    try:
        choice = int(input("Enter your choice (1/2/3): "))
        if choice not in [1,2,3]:
            raise ValueError("")
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
    answer = input(f"Would you like to send the output to whatsapp automatically? y/n: ")
    answer = answer.strip()
    if answer.lower() == "y" or answer.lower() == "yes":
        return True
    else:
        return False

def send_now(contact_name, file_path):
    base_dir = os.getenv('BASE_DIR')
    user_data_dir = os.getenv('USER_DATA_DIR')
    whatsapp_bot = WhatsAppBot(base_dir=base_dir, user_data_dir=user_data_dir)
    whatsapp_bot.send_messages_from_file(contact_name, file_path)
    whatsapp_bot.close() 

def timestr():
    return today.strftime("%m_%d_%Y")

def main():
    senders = ["agustin", "bryan", "laban_agustin", "laban_bryan"]
    contacts = ['"Astig group👋 A.K.A 🤫BOY TABAS"',
                '"👊laban"',
                '"Balik duplicate"',
                '"😊😊😊 Duran-Agus bakas😊😊😊"'
                ]
    base_dir = os.getenv('BASE_DIR')
    while True:
        clear_terminal()
        chosen = choose()
        all_entries = []
        all_analyzer = []
        auto_send = send_to_whatsapp()
        for sender in senders:
            
            analyzer = FileProcessor(sender=sender,base_dir=base_dir)
            all = analyzer.read_input()
            entries = Entries(all=all, sender=sender)
            
            analyzer.print_wrong_input()

            duplicates = entries.duplicates
            analyzer.write_tulog(duplicates=duplicates)

            all_entries.append(entries)
            all_analyzer.append(analyzer)

            if auto_send and chosen == 1:
                file_path = f"tulog/{timestr()}_tulog_{sender}.txt"
                if sender == "laban_bryan":
                  send_now(contact_name=contacts[1], file_path=file_path)
                elif sender == "laban_agustin":
                  send_now(contact_name=contacts[3], file_path=file_path)
                else:
                  send_now(contact_name=contacts[0], file_path=file_path)
            
        if chosen == 2 or chosen == 3:
            limit = int(input("What is the limit? "))
            duplicates_with = DuplicatesWith(entries=all_entries[0], other=all_entries[1], base_dir=base_dir)
            duplicates_with.write(limit=limit)  
            total_duplicates_with = min(duplicates_with.lines(limit=limit)[1], duplicates_with.lines(limit=limit)[2])
            
            if auto_send and chosen == 2:
                file_path = f"duplicate/{timestr()}_duplicates_{senders[0]}_{senders[1]}.txt"
                send_now(contact_name=contacts[2], file_path=file_path)

            
            bookies = all_entries[3].bookies
            all_analyzer[3].write_kabo(bookies=bookies)
            if auto_send and chosen == 2:
                file_path = f"kabo/{timestr()}_kabo_{senders[3]}.txt"
                send_now(contact_name=contacts[1], file_path=file_path)

            if chosen == 3:
                winning_number = get_winning_number()
                
                for index in range(len(all_entries)):
                    if index == 3:
                        limit = False  # NO LIMIT FOR LABAN BRYAN
        
                    if index != 2:
                        result = all_entries[index].result(winning_number=winning_number, limit=limit, other_entries=Entries()) 
                    else: 
                        result = all_entries[index].result(winning_number=winning_number, limit=limit, other_entries=all_entries[0])
                    all_analyzer[index].write_result(result= result, minus_sender="agustin", total_duplicates_with=total_duplicates_with)
                    
                    if auto_send:
                      file_path = f"result/{timestr()}_result_{senders[index]}.txt"
                      if index == 3:
                        send_now(contact_name=contacts[1], file_path=file_path)
                      elif index == 2:
                        send_now(contact_name=contacts[3], file_path=file_path)  
                      else:
                        send_now(contact_name=contacts[0], file_path=file_path)
                      
                    if index == 3:
                        result_raw = all_entries[index].result_raw(winning_number=winning_number)
                        all_analyzer[index].write_result_raw(result=result_raw)

                        if auto_send:
                          file_path = f"result/{timestr()}_result_raw_{senders[index]}.txt"
                          send_now(contact_name=contacts[1], file_path=file_path)
        print("Done...")
        if not to_continue():
            break
                    

main()

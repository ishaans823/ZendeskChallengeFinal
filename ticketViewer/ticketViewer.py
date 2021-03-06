import pip._vendor.requests
import getpass


def getTicketData(option, ticket, url, user, pwd):
    #divider
    print("---------------------------------------------------------------------------")

    #creating full url with the given subdomain
    url = 'https://' + url + '.zendesk.com/api/v2/tickets?page[size]=25'
    # do the http get request
    response = pip._vendor.requests.get(url, auth=(user, pwd))

    # error connecting
    if response.status_code != 200:
        print('status:', response.status_code, 'error with the request, exiting.')
        print("Make sure you entered the correct subdomin and just the subdomain (https://{subdomain}.zendesk.com)")
        exit()

    data = response.json()

    # print ticket(s)
    if option == "2":
        #user enters ticket outside of range
        if len(data['tickets']) < ticket or ticket < 1:
            print("Invalid ticket: Make sure you enter the correct ticket id [1 to num of tickets]")
        else:
            print( 'Ticket ID: ', data['tickets'][ticket - 1]['id'] )
            print( 'Subject: ', data['tickets'][ticket - 1]['subject'] )
            print( 'Descripton: ', data['tickets'][ticket - 1]['description'] )
            print( 'Status: ', data['tickets'][ticket - 1]['status'] )
            print( 'Submitted by ', data['tickets'][ticket - 1]['submitter_id'], " on ", data['tickets'][ticket - 1]['created_at'] )
    else:
        #print all tickets, 25 at a time
        while url:
            response = pip._vendor.requests.get(url, auth=(user, pwd))
            data = response.json()
            for ind_tix in data['tickets']:
                print("---------------------------------------------------------------------------")
                print( 'Ticket ID: ', ind_tix['id'] )
                print( 'Subject: ', ind_tix['subject'] )
                print( 'Descripton: ', ind_tix['description'] )
                print( 'Status: ', ind_tix['status'] )
                print( 'Submitted by ', ind_tix['submitter_id'], " on ", ind_tix['created_at'] )
            if data['meta']['has_more']:
                url = data['links']['next']
            else:
                url = None
    #divider
    print("---------------------------------------------------------------------------")

def main():
    userInput = " "
    #introduction
    print("Hello! Welcome to the ticket viewer! Please enter the following credentials to continue: ")
    print("---------------------------------------------------------------------------")

    #collecting credentials
    subdomain = input("Please provide the subdomain: ")
    email = input("Please provide the email address associated with the account: ")
    password = getpass.getpass("Please provide the password of the associated account(it is hidden): ")

    print("---------------------------------------------------------------------------")

    #requesting user input
    while userInput != "q":
        print("Press 1 to view all tickets")
        print("Press 2 to view individual tickets")
        print("Press q to quit")
        userInput = input("Enter an option: ")

        if userInput == "1":
            print("All tickets")
            getTicketData(userInput, -1, subdomain, email, password)
        elif userInput == "2":
            ticketNum = input("Which ticket would you like to view: ")
            ticketNum = int(ticketNum)
            getTicketData(userInput, ticketNum, subdomain, email, password)
            #print that ticket
        elif userInput == "q":
            continue
        else:
            print("Invalid Command! Please type one of the commands shown above.")

if __name__ == "__main__":
    main()
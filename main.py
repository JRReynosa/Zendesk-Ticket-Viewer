import sys
import requests
import json
from unittest import main

# Credentials to access API
user = "jonathanreynosa19@gmail.com/token"
token = "fPnKjhcBjmstx5ycHK8nVtjT557XBgic5q1apDsP"


def get_multiple_tickets(page_url=""):
    """
    Prints multiple tickets from the Zendesk API in pages of 25 tickets, and returns URLs to previous/next pages of tickets if available. It is assumed a valid URL is always passed to this method.
  
    Parameters:
    page_url (str): Takes in a valid Zendesk pagination URL for a previous or next page of tickets
  
    Returns:
    str, str: Returns URLs of previous or next page of tickets if available; null otherwise
  
    """
    if page_url == "":
        url = "https://zccreynosa.zendesk.com/api/v2/tickets.json?page[size]=25"
    else:
        url = page_url

    response = requests.get(url, auth=(user, token))

    if response.status_code != 200:
        print("Error Status Code: " + str(response.status_code))
    else:
        json_data = json.loads(response.text)

        prev_url = json_data["links"]["prev"]
        next_url = json_data["links"]["next"]

        if len(
                json.loads(requests.get(prev_url,
                                        auth=(user,
                                              token)).text)['tickets']) == 0:
            prev_url = ""

        if len(
                json.loads(requests.get(next_url,
                                        auth=(user,
                                              token)).text)['tickets']) == 0:
            next_url = ""

        return json_data, prev_url, next_url


def get_ticket_by_id(id):
    """
    Gets the information for an individual ticket by searching by ticker ID
  
    Parameters:
    id (int): Ticket ID to be searched for
  
    """
    url = "https://zccreynosa.zendesk.com/api/v2/tickets/" + id + ".json"
    response = requests.get(url, auth=(user, token))

    if response.status_code != 200:
        return None
    else:
        json_data = json.loads(response.text)
        return json_data


def print_ticket(json_data):
    """
    Prints information for a ticket given the ticket information in its JSON form
  
    """
    print("\nSubject: " + json_data["ticket"]["subject"])
    print("Created: " + json_data["ticket"]["created_at"])
    print("Last Updated: " + json_data["ticket"]["updated_at"])
    print("Submitted By: " + str(json_data["ticket"]["submitter_id"]))
    print("Assigned To: " + str(json_data["ticket"]["assignee_id"]))
    print("\nDescription: " + json_data["ticket"]["description"])
    print("\nStatus: " + json_data["ticket"]["status"])


def print_ticket_list(json_data):
    """
    Prints list of tickets given the ticket list in its JSON form
  
    """
    print(
        "ID   |   Subject   |   Submitted By   |   Date Created   |   Last Updated   |   Status   "
    )
    for ticket in json_data["tickets"]:
        print(ticket['id'], " | ", ticket['subject'], " | ",
              ticket['submitter_id'], " | ", ticket['created_at'], " | ",
              ticket['updated_at'], " | ", ticket['status'])


def print_main_menu():
    """
    Prints main menu options for Zendesk Ticket Viewing System
  
    """
    print("\nWelcome to the Zendesk Ticket Viewing System!\nInstructions:")
    print("~ Enter '1' to view all tickets")
    print("~ Enter '2' to view a certain ticket")
    print("~ Enter '3' to view these options again")
    print("To exit the ticketing system enter 'quit'")


def print_paging_menu():
    """
    Prints pagination options for Zendesk Ticket Viewing System
  
    """
    print("\n~ Enter 'n' to view next page of tickets")
    print("~ Enter 'p' to view previous page of tickets")
    print("~ Enter 'q' to quit viewing list of tickets")


#main(module='unit_tests', exit=False)
# To run unit tests, uncomment the line above and delete everything below this line

print_main_menu()
user_input = input()



while user_input != "quit":
    if int(user_input) == 1:
        json_data, prev_url, next_url = get_multiple_tickets()
        print_ticket_list(json_data)
        print_paging_menu()
        user_input = input()

        while user_input != "q":

            if user_input == "n":
                if next_url == "":
                    print("No more tickets available to show")
                    print_paging_menu()
                else:
                    json_data, prev_url, next_url = get_multiple_tickets(next_url)
                    print_ticket_list(json_data)
                    print_paging_menu()
                user_input = input()

            elif user_input == "p":
                if prev_url == "":
                    print("No previous page")
                    print_paging_menu()
                else:
                    json_data, prev_url, next_url = get_multiple_tickets(prev_url)
                    print_ticket_list(json_data)
                    print_paging_menu()
                user_input = input()

            else:
                print("Input is invalid, please review your options")
                print_paging_menu()
                user_input = input()

        user_input = input()

    elif int(user_input) == 2:
        given_id = input("Please enter the ticket ID number: ")
        json_data = get_ticket_by_id(given_id)
        if json_data == None:
          print("Resource was not found or error was thrown")
        else:
          print_ticket(json_data)
        user_input = input()

    elif user_input == "3":
        print_main_menu()
        user_input = input()

    else:
        print("Input is invalid, please review your options")
        print_main_menu()
        user_input = input()

sys.exit("Thank you for using the Zendesk ticketing system!")

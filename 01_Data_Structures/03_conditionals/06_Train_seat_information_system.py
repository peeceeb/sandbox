Ticket_type=input(f"Enter the type of ticket (general, ac, sleeper, luxury) ").lower()


match Ticket_type:
    case "sleeper":
        print("Sleeper - No AC, Beds available")
    case "ac":
        print("AC - Air conditioned, comfy ride")
    case "Luxury":
        print("Luxury - Premium seats with meals!")
    case "General":
        print("General - Cheapest option, no reservation")
    case _:
        print("Invalid seat type")



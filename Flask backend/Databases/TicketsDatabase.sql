-- TRANSPORT OPTIONS TABLE --
CREATE TABLE IF NOT EXISTS TransportOptions {
    TicketID INTEGER PRIMARY KEY, --unique value of the ticket
    TransportCompany TEXT NOT NULL, --name of transport company (peoria, amtrak, etc)
    TransportType TEXT NOT NULL, --type of vehicle (bus, train, etc)
    StartTime TEXT NOT NULL, --time of departure given as string in hr:min format
    ArrivalTime TEXT NOT NULL, --time of arrival given as string in hr:min format
    Price FLOAT NOT NULL, --price of ticket given as float
    PickUpLocation TEXT NOT NULL, --pickup location given as string
    Destination TEXT NOT NULL, --dropoff location given as string
    NumberOfAvailableTickets INTEGER NOT NULL, --total tickets available
    NumberOfPurchasedTickets INTEGER NOT NULL --tickets already purchased
};
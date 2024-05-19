import Ticket
import User
import pygame
import pygame_gui

class MainMenu:

   def __init__(self):
       self.allUsers = []
       self.allTickets = []
       self.filteredTickets = []
       self.currentUser = None
       self.selectedTicket = None
       self.isSellingTicket = False
       self.mode = "LOGIN"  #this variable will keep track of the current mode, and update the display accordingly.
       # starts off as "LOGIN", and can also hold values of "MAINMENU" or "ACCOUNT"
       self.errorMessage = None #when are error window is created, it will display this error message
       self.usersFile = open("users.txt", 'a+')  #opens users and tickets files
       self.ticketsFile = open("tickets.txt", "a+")

       self.readUsersFile()
       self.readTicketsFile()
       self.filteredTickets = self.allTickets

       self.create()

   def create(self):
       pygame.init()

       #GUI manager and text input fields
       manager = pygame_gui.UIManager((700,500))
       UI_REFRESH_RATE = pygame.time.Clock().tick(60)/5000  #sets the rate at which the GUI will refresh
       self.usernameInput = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((300, 160), (200, 35)), manager=manager, object_id = "#usernameInput")
       self.passwordInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, 235), (200, 35)), manager=manager, object_id="#passwordInput")
       self.creditCardInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 150), (200, 35)), manager=manager, object_id="#creditCardInput")
       self.loadMoneyInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 225), (200, 35)), manager=manager, object_id="#loadMoneyInput")
       self.sellTicketInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 200), (300, 35)), manager=manager, object_id="#sellTicketInput")

       self.creditCardInput.visible = False
       self.loadMoneyInput.visible = False
       self.sellTicketInput.visible = False

       size = (700, 500)
       screen = pygame.display.set_mode(size)

       running = True
       while running:
           self.updateDisplay(screen)

           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   running = False
               elif event.type == pygame.MOUSEBUTTONDOWN:
                   mx, my = pygame.mouse.get_pos()  #gets coordinates of click
                   self.buttonPressed(mx,my)  #calls function to check which button was pressed, and what needs to be done

               if self.mode == "LOGIN":
                   if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#usernameInput":  #check if enter is pressed when typing username/password, and if so tries to log in
                       self.login(self.usernameInput.get_text(),self.passwordInput.get_text())
                       self.usernameInput.clear()
                       self.passwordInput.clear()
                   elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#passwordInput":
                       self.login(self.usernameInput.get_text(), self.passwordInput.get_text())
                       self.usernameInput.clear()
                       self.passwordInput.clear()

               manager.process_events(event)

           manager.update(UI_REFRESH_RATE)
           manager.draw_ui(screen)  #updates gui components (text input field)

           pygame.display.flip()  #updates visuals

       pygame.quit()
       self.ticketsFile.close()
       self.usersFile.close()


   def updateDisplay(self, window):
       if self.mode == "LOGIN":
           self.drawLoginWindow(window)

       elif self.mode == "MAINMENU":
           self.drawMainMenu(window)

       elif self.mode == "ACCOUNT":
           self.drawAccountWindow(window)


   def drawMainMenu(self, window):    #main menu visuals go here
       self.usernameInput.visible = False
       self.passwordInput.visible = False
       self.creditCardInput.visible = False
       self.loadMoneyInput.visible = False

       pygame.draw.rect(window, (50,93,161), (0, 0, 700, 100))    #draws upper background
       pygame.draw.rect(window, (93,129,181), (0, 100, 700, 400))  #draws lower background

       pygame.draw.rect(window, (255, 255, 204), (100, 25, 75, 50), 250, 3)  #draws "buy ticket" button
       pygame.draw.rect(window, (255, 255, 204), (200, 25, 75, 50), 250, 3)  #draws "sell ticket" button

       pygame.draw.rect(window, (255, 255, 204), (425, 25, 75, 50), 250, 3)  # draws "filter by price" button
       pygame.draw.rect(window, (255, 255, 204), (525, 25, 75, 50), 250, 3)  # draws "filter by artist" button

       pygame.draw.rect(window, (223,180,87), (312.5, 25, 75, 50), 250, 3)  # draws "Account" button

       font = pygame.font.Font('freesansbold.ttf', 10)
       slightlyBiggerFont = pygame.font.Font('freesansbold.ttf', 11)

       buyTicketText = font.render("Buy Ticket", True,(100, 100, 100))  # all the following code is for the text
       sellTicketText = font.render("Sell Ticket", True, (100, 100, 100))
       filterByPriceText = font.render("Filter by Price", True, (100, 100, 100))
       filterByArtistText = font.render("Filter by Artist", True, (100, 100, 100))
       accountText = font.render("Account", True, (100, 100, 100))

       buyTicketTextRect = buyTicketText.get_rect()
       sellTicketTextRect = sellTicketText.get_rect()
       filterByPriceTextRect = filterByPriceText.get_rect()
       filterByArtistTextRect = filterByArtistText.get_rect()
       accountTextRect = accountText.get_rect()

       buyTicketTextRect.center = (137.5, 50)
       sellTicketTextRect.center = (237.5, 50)
       filterByPriceTextRect.center = (462.5, 50)
       filterByArtistTextRect.center = (562.5, 50)
       accountTextRect.center = (350, 50)

       window.blit(buyTicketText, buyTicketTextRect)
       window.blit(sellTicketText, sellTicketTextRect)
       window.blit(filterByPriceText, filterByPriceTextRect)
       window.blit(filterByArtistText, filterByArtistTextRect)
       window.blit(accountText, accountTextRect)


       if self.selectedTicket:   #if a ticket is selected, draws highlight around it. Note: must be done before drawing ticket rectangle to make it an outline
           y = (self.filteredTickets.index(self.selectedTicket) * 70) + 125
           pygame.draw.rect(window, (255,255,0), (95,y-5,510,45))

       mx, my = pygame.mouse.get_pos()

       x = 100
       y = 125
       for ticket in self.filteredTickets:   #draw box for each ticket
           pygame.draw.rect(window, (255,255,255), (x, y, 500, 35), 0, 3)

           if mx > 100 and mx < 600:
               if my > y and my < y + 35:
                   pygame.draw.rect(window, (175,175,175), (x, y, 500, 35), 0, 3)
           ticketText = slightlyBiggerFont.render(str(ticket), True, (100, 100, 100))
           ticketTextRect = ticketText.get_rect()
           ticketTextRect.center = (x + 250, y + 17)
           window.blit(ticketText, ticketTextRect)

           y += 70


       if self.errorMessage != None:
           self.drawError(window)

       if self.isSellingTicket:
           self.drawSellTicketWindow(window)


   def drawLoginWindow(self, window):   #login window visuals go here
       self.usernameInput.visible = True  # sets text fields to visible
       self.passwordInput.visible = True

       pygame.draw.rect(window, (125, 225, 100), (0, 0, 700, 500))   #draws background

       pygame.draw.rect(window, (150, 50, 200), (150, 350, 130, 65), 250, 3)   #draws "Login" button
       pygame.draw.rect(window, (150, 50, 200), (425, 350, 130, 65), 250, 3)  # draws "Create Account" button

       font = pygame.font.Font('freesansbold.ttf', 15)
       logoFont = pygame.font.SysFont('impact', 50)
       logoFont2 = pygame.font.SysFont('vladimirscript', 50, italic=False)

       loginText = font.render("Login", True, (255, 255, 255))  #all the following code in this function is for the text
       createAccountText = font.render("Create Account", True, (255, 255, 255))
       usernameText = font.render("Username", True,(100, 100, 100))
       passwordText = font.render("Password", True, (100, 100, 100))
       logoText = logoFont.render("TICKET", True, (102, 0, 102))
       logoText2 = logoFont2.render("Mistress", True, (102, 0, 102))

       loginTextRect = loginText.get_rect()
       createAccountTextRect = createAccountText.get_rect()
       usernameTextRect = usernameText.get_rect()
       passwordTextRect = passwordText.get_rect()
       logoTextRect = logoText.get_rect()
       logoText2Rect = logoText2.get_rect()

       loginTextRect.center = (215, 382.5)
       createAccountTextRect.center = (490, 382.5)
       usernameTextRect.center = (250, 175)
       passwordTextRect.center = (250, 255)
       logoTextRect.center = (280, 90)
       logoText2Rect.center = (420, 90)

       window.blit(loginText, loginTextRect)
       window.blit(createAccountText, createAccountTextRect)
       window.blit(usernameText, usernameTextRect)
       window.blit(passwordText, passwordTextRect)
       window.blit(logoText, logoTextRect)
       window.blit(logoText2, logoText2Rect)

       if self.errorMessage != None:
           self.usernameInput.visible = 0
           self.passwordInput.visible = 0
       else:
           self.usernameInput.visible = 1
           self.passwordInput.visible = 1

       if self.errorMessage != None:
           self.drawError(window)


   def drawAccountWindow(self, window):   #user account screen visuals

       self.usernameInput.visible = False # sets text fields to invisible
       self.passwordInput.visible = False
       self.creditCardInput.visible = True
       self.loadMoneyInput.visible = True

       pygame.draw.rect(window, (50, 93, 161), (0, 0, 700, 100))  # draws upper background
       pygame.draw.rect(window, (93,129,181), (0, 100, 700, 400))  #draws lower background

       pygame.draw.rect(window, (223,180,87), (300, 25, 100, 50), 250, 3)  #draws "main menu" button

       pygame.draw.rect(window, (255, 255, 204), (460, 152.5, 75, 30))  # draws "confirm credit card" button
       pygame.draw.rect(window, (255, 255, 204), (460, 227.5, 75, 30))  # draws "load money" button


       font = pygame.font.Font('freesansbold.ttf', 12)

       mainMenuText = font.render("Main Menu", True, (100,100,100))
       creditCardText = font.render("Credit Card:", True, (255, 255, 255))
       loadMoneyText = font.render("Load Money:", True, (255, 255, 255))
       myTicketsText = font.render("My Tickets:", True, (255, 255, 255))
       creditCardButtonText = font.render("Confirm", True, (100,100,100))
       loadMoneyButtonText = font.render("Load Money", True, (100,100,100))
       balanceText = font.render("Balance:", True, (255, 255, 255))
       amountText = font.render(str(self.currentUser.balance), True, (255, 255, 255))

       mainMenuTexttRect = mainMenuText.get_rect()
       creditCardTextRect = creditCardText.get_rect()
       loadMoneyTextRect = loadMoneyText.get_rect()
       myTicketsTextRect = myTicketsText.get_rect()
       creditCardButtonTextRect = creditCardButtonText.get_rect()
       loadMoneyButtonTextRect = loadMoneyButtonText.get_rect()
       balanceTextRect = balanceText.get_rect()
       amountTextRect = amountText.get_rect()

       mainMenuTexttRect.center = (350, 50)
       creditCardTextRect.center = (205, 165)
       loadMoneyTextRect.center = (205, 240)
       myTicketsTextRect.center = (205, 285)
       creditCardButtonTextRect.center = (497.5, 167.5)
       loadMoneyButtonTextRect.center = (497.5, 242.5)
       balanceTextRect.center = (325, 115)
       amountTextRect.center = (375, 115)

       window.blit(mainMenuText, mainMenuTexttRect)
       window.blit(creditCardText, creditCardTextRect)
       window.blit(loadMoneyText, loadMoneyTextRect)
       window.blit(myTicketsText, myTicketsTextRect)
       window.blit(creditCardButtonText, creditCardButtonTextRect)
       window.blit(loadMoneyButtonText, loadMoneyButtonTextRect)
       window.blit(balanceText, balanceTextRect)
       window.blit(amountText, amountTextRect)


       x = 100
       y = 300

       for ticket in self.currentUser.cart.items:  # draw box for each ticket
           pygame.draw.rect(window, (255,255,255), (x, y, 500, 35), 0, 3)

           ticketText = font.render(str(ticket), True, (100, 100, 100))
           ticketTextRect = ticketText.get_rect()
           ticketTextRect.center = (x + 250, y + 17)
           window.blit(ticketText, ticketTextRect)

           y += 60


       if self.errorMessage != None:
           self.drawError(window)



   def buttonPressed(self, x, y):
       if self.errorMessage == None:
           allGood = True
       else:
           allGood = False

       if self.mode == "LOGIN":
           if x > 150 and x < 280 and y > 350 and y < 415 and allGood:  #Login button was pressed
               self.login(self.usernameInput.get_text(),self.passwordInput.get_text())

           if x > 425 and x < 555 and y > 350 and y < 415 and allGood: #Create Account button pressed
               self.createAccount(self.usernameInput.get_text(),self.passwordInput.get_text())

           if (not allGood) and x > 275 and x < 425 and y > 280 and y < 330:
               self.errorMessage = None


       elif self.mode == "MAINMENU":
           if x > 100 and x < 175 and y > 25 and y < 75 and allGood and (not self.isSellingTicket): #Buy ticket button pressed
               self.buyTicket()
           if x > 200 and x < 275 and y > 25 and y < 75 and allGood and (not self.isSellingTicket): #Sell Ticket button pressed
               self.sellTicket()
           if x > 425 and x < 500 and y > 25 and y < 75 and allGood and (not self.isSellingTicket): #Filter by Price button pressed
               self.filterByPrice()
           if x > 525 and x < 600 and y > 25 and y < 75 and allGood and (not self.isSellingTicket): #Filter by Artist button pressed
               self.filterByArtist()
           if x > 312.5 and x < 387.5 and y > 25 and y < 75 and allGood and (not self.isSellingTicket): #Account button pressed
               self.selectedTicket = None
               self.mode = "ACCOUNT"

           if self.isSellingTicket and x > 275 and x < 425 and y > 280 and y < 330:   #if sellTicket's window confirm button is pressed
               self.sellTicketInput.visible = False
               self.isSellingTicket = False
               self.confirmTicketSale()

           if (not allGood) and x > 275 and x < 425 and y > 280 and y < 330:   #if error window's exit button is pressed
               self.errorMessage = None

           #check if a ticket is selected
           if allGood and (not self.isSellingTicket):
               ticketx = 100
               tickety = 125
               for i in range(len(self.filteredTickets)):
                   if x > ticketx and x < (ticketx + 500) and y > tickety and y < (tickety + 35):
                       if self.selectedTicket == None or self.selectedTicket != self.filteredTickets[i]:
                           self.selectedTicket = self.filteredTickets[i]   #sets the selected ticket to the chosen ticket
                       else:
                           self.selectedTicket = None #however, if a ticket is selected, unselects it
                   tickety += 70


       elif self.mode == "ACCOUNT":
           if x > 300 and x < 400 and y > 25 and y < 75 and allGood: #Account button pressed
               self.mode = "MAINMENU"

           if x > 460 and x < 535 and y > 152.5 and y < 182.5 and allGood: #confirm credit card pressed
               self.confirmCreditCard()

           if x > 460 and x < 535 and y > 227.5 and y < 257.5 and allGood: #load money pressed
               self.loadMoney()

           if (not allGood) and x > 275 and x < 425 and y > 280 and y < 330:
               self.errorMessage = None



   def login(self, username, password):  #called when the login button is pressed

       self.usernameInput.clear()
       self.passwordInput.clear()

       if username == "":
           self.errorMessage = "Enter a Username"
           return
       elif password == "":
           self.errorMessage = "Enter a Password"
           return

       for user in self.allUsers:
           if username == user.username and password == user.password:
               self.currentUser = user
               self.mode = "MAINMENU"
               return

       self.errorMessage = "Invalid Username/Password"
       return


   def createAccount(self, username, password):  #called when the create account button is pressed

       self.usernameInput.clear()
       self.passwordInput.clear()

       if username == "":
           self.errorMessage = "Enter a Username"
           return
       elif password == "":
           self.errorMessage = "Enter a Password"
           return
       else:
           for user in self.allUsers:
               if username == user.username:
                   self.errorMessage = "Username Taken"
                   return

       self.usersFile.write("\n" + username + " , " + password + " , " + username + "@gmail.com" + " , " + "xxxx xxxx xxxx xxxx")
       self.usersFile.close()
       self.usersFile = open("users.txt", 'a+')

       self.readUsersFile()

   def buyTicket(self):
       if self.selectedTicket == None:
           self.errorMessage = "Select a Ticket"
           return

       if self.currentUser.balance < self.selectedTicket.price:
           self.errorMessage = "Not Enough Funds"
           self.selectedTicket = None
           return

       self.currentUser.cart.addToCart(self.selectedTicket)
       self.currentUser.balance -= self.selectedTicket.price
       self.selectedTicket = None

   def sellTicket(self):
       self.isSellingTicket = True
       self.selectedTicket = None


   def confirmTicketSale(self):

       ticketString = self.sellTicketInput.get_text().split(',')

       if (len(ticketString) != 5) or (not ticketString[4].isnumeric()):
           self.errorMessage = "Invalid Ticket"
           self.sellTicketInput.clear()
           self.selectedTicket = None
           return

       artist = ticketString[0]
       date = ticketString[1]
       time = ticketString[2]
       location = ticketString[3]
       price = ticketString[4]

       ticket = Ticket.Ticket(self.currentUser.username, artist, date, time, location, int(price))

       self.allTickets.append(ticket)
       self.filteredTickets = self.allTickets

       self.updateTicketsFile()


   def filterByPrice(self):

       priceList = []
       newOrderList = []
       for ticket in self.allTickets:
           priceList.append((ticket.price, ticket.date, ticket.time))

       priceList.sort()
       for price in priceList:
           for ticket in self.allTickets:
               if price[0] == ticket.price and price[1] == ticket.date and price[2] == ticket.time:
                   newOrderList.append(ticket)
                   break

       self.filteredTickets = newOrderList


   def filterByArtist(self):

       artistList = []
       newOrderList = []
       for ticket in self.allTickets:
           artistList.append((ticket.artist, ticket.date, ticket.time))

       artistList.sort()
       for artist in artistList:
           for ticket in self.allTickets:
               if artist[0] == ticket.artist and artist[1] == ticket.date and artist[2] == ticket.time:
                   newOrderList.append(ticket)
                   break

       self.filteredTickets = newOrderList



   def confirmCreditCard(self):
       if (not self.creditCardInput.get_text().isnumeric()) or len(self.creditCardInput.get_text()) != 16:
           self.errorMessage = "Enter a Valid Card"
           self.creditCardInput.clear()
           return

       self.currentUser.cardInfo = self.creditCardInput.get_text()
       self.updateUsersFile()
       self.creditCardInput.clear()

   def loadMoney(self):
       if not self.loadMoneyInput.get_text().isnumeric():
           self.errorMessage = "Enter a Number"
           self.loadMoneyInput.clear()
           return

       if self.currentUser.cardInfo == "xxxx xxxx xxxx xxxx":
           self.errorMessage = "No Payment Method"
           self.loadMoneyInput.clear()
           return

       self.currentUser.balance += int(self.loadMoneyInput.get_text())
       self.loadMoneyInput.clear()


   def readUsersFile(self):  #reads users file for checking login, balance, and other important information
       self.allUsers.clear()
       self.usersFile.seek(0)
       for user in self.usersFile:
           userString = user.split(',')

           username = userString[0].strip()
           password = userString[1].strip()
           emailAddress = userString[2].strip()
           cardInfo = userString[3].strip()
           self.allUsers.append(User.User(username, password, emailAddress, cardInfo))


   def readTicketsFile(self):  #reads ticket file and files self.allTickets
       self.ticketsFile.seek(0)  # resets the file reading position to the start, before reading it
       for ticket in self.ticketsFile:
           ticketString = ticket.split(',')

           seller = ticketString[0].strip()
           artist = ticketString[1].strip()
           date = ticketString[2].strip()
           time = ticketString[3].strip()
           location = ticketString[4].strip()
           price = int(ticketString[5].strip())
           self.allTickets.append(Ticket.Ticket(seller, artist, date, time, location, price))


   def updateUsersFile(self):

       self.usersFile.truncate(0)
       for user in self.allUsers:
           if self.allUsers.index(user) == 0:
               self.usersFile.write(user.fileFormat())
           else:
               self.usersFile.write("\n" + user.fileFormat())

       self.usersFile.close()
       self.usersFile = open("users.txt", 'a+')

   def updateTicketsFile(self):

       self.ticketsFile.truncate(0)
       for ticket in self.allTickets:
           if self.allTickets.index(ticket) == 0:
               self.ticketsFile.write(ticket.fileFormat())
           else:
               self.ticketsFile.write("\n" + ticket.fileFormat())

       self.usersFile.close()
       self.usersFile = open("users.txt", 'a+')


   def drawSellTicketWindow(self, window):   #calls this when a user wants to sell a ticket
       self.creditCardInput.visible = False
       self.loadMoneyInput.visible = False
       self.sellTicketInput.visible = True

       pygame.draw.rect(window, (0, 204, 102), (100, 110, 500, 290))  # draws background

       pygame.draw.rect(window, (0, 0, 255), (275, 280, 150, 50))  # draws confirm button

       font = pygame.font.Font('freesansbold.ttf', 15)

       ticketInfoText = font.render("Ticket Info:", True, (255, 255, 255))
       confirmText = font.render("Confirm", True, (255, 255, 255))

       ticketInfoTextRect = ticketInfoText.get_rect()
       confirmTextRect = confirmText.get_rect()

       ticketInfoTextRect.center = (200, 215)
       confirmTextRect.center = (350, 305)

       window.blit(ticketInfoText, ticketInfoTextRect)
       window.blit(confirmText, confirmTextRect)


   def drawError(self, window):   #call this whenever an error occurs to create an error pop up with with self.errorMessage
       self.creditCardInput.visible = False
       self.loadMoneyInput.visible = False


       pygame.draw.rect(window, (255,0,0), (200,110,300,290))   #draws error window background

       pygame.draw.rect(window, (0, 0, 255), (275, 280, 150, 50))   #draws exit button

       font = pygame.font.Font('freesansbold.ttf', 20)

       errorText = font.render(self.errorMessage, True, (255, 255, 255))
       exitText = font.render("Exit", True, (255, 255, 255))

       errorTextRect = errorText.get_rect()
       exitTextRect = exitText.get_rect()

       errorTextRect.center = (350, 225)
       exitTextRect.center = (350, 305)

       window.blit(errorText, errorTextRect)
       window.blit(exitText, exitTextRect)




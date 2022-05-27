import pygame
from network import Network
import pickle
pygame.font.init()


width = 750
height = 750

window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Client")

class Button:

   def __init__(self,text,x,y,color):
       self.text = text
       self.x = x
       self.y = y
       self.color = color
       self.width = 150
       self.height = 100

   def draw_game(self,window):
       """
       This function draw the button
       :param window:
       :return:
       """
       pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.height))
       font = pygame.font.SysFont("arial.ttf",40)
       text = font.render(self.text,1,(255,255,255))
       window.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                       self.y + round(self.height / 2) - round(text.get_height() / 2)))


   def click_but(self,position):
       """
         This function check if the button is clicked
         :param position:
         :return:
         """
       x_1 = position[0]
       y_1 = position[1]
       if self.x <= x_1 <= self.x + self.width and self.y <= y_1 <= self.y + self.height:
           return True
       else:
           return False






configure_buttons = [Button("Rock",50,500,(255,0,0)),Button("Scissors",250,500,(0,255,0))
    ,Button("Paper",450,500,(0,0,255))]


def redraw_game_window(window,game,player_num):
    """
    This function redraw the game window
    :param window:
    :param game:
    :param player_num:
    :return:
    """
    window.fill((128,128,128))

    if not (game.connected()): # only one player connect to the game
        font = pygame.font.SysFont("arial.ttf",60)
        text = font.render("Waiting For Opponent .....",1,(255,0,0))
        window.blit(text, (width/2 - text.get_width()/2 ,height/2 - text.get_height()/2))

    else :
        # both players connected to game
        font = pygame.font.SysFont("arial.ttf", 50)
        text = font.render("Your Move", True, (255,255, 255))
        window.blit(text,(80,200))

        text = font.render("Opponent", True, (255, 0, 0))
        window.blit(text, (380, 200))

        move_p1 = game.get_player_movement(0)
        move_p2 = game.get_player_movement(1)

        if game.players_both_moves():
            text_p1 = font.render(move_p1, 1, (0, 0, 0))
            text_p2 = font.render(move_p2, 1, (0, 0, 0))
        else:
            if game.p1_move and player_num == 0:
                text_p1 = font.render(move_p1, 1, (0, 0, 0))
            elif game.p1_move :
                text_p1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text_p1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2_move and player_num == 1:
                text_p2 = font.render(move_p2, 1, (0, 0, 0))
            elif game.p2_move :
                text_p2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text_p2 = font.render("Waiting...", 1, (0, 0, 0))

        if player_num == 1:
            window.blit(text_p2, (100, 350))
            window.blit(text_p1, (400, 350))
        else:
            window.blit(text_p1, (100, 350))
            window.blit(text_p2, (400, 350))

        for buttons in configure_buttons:
            buttons.draw_game(window)

    pygame.display.update()



def main():
    run_game = True
    clock = pygame.time.Clock()
    n = Network() # make the connection to the game
    player_number = int(n.get_p()) # connect the player and get player number 0 or 1
    print("Your player Number is {}".format(player_number))
    while run_game :
        clock.tick(60)
        try :
            game = n.send_message("Get")
        except:
            run_game = False
            print("Server Dont Respond ! ")


        if game.players_both_moves():  # check which player won the game
            redraw_game_window(window,game,player_number)
            pygame.time.delay(500)
            try:
                game = n.send_message("Reset")
            except:
                run_game = False
                print("Server Dont Respond ! ")

            font = pygame.font.SysFont("arial.ttf", 90)
            if (game.winner_of_the_game() == 1 and player_number == 1) or (game.winner_of_the_game() == 0 and player_number == 0):
                text = font.render("You Won!", 1, (0, 0, 255))
            elif game.winner_of_the_game() == -1:
                text = font.render("It's a Draw!", 1, (0, 0, 0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(3000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                for buttons in configure_buttons :
                    if buttons.click_but(position) and game.connected() : # check for clicking buttons
                        if player_number == 0 : # check for current player
                            # if players already make a move , they c'ant make another move
                            if not game.p1_move :
                                n.send_message(buttons.text)
                        else :
                            if not game.p2_move:
                                n.send_message(buttons.text)

        redraw_game_window(window,game,player_number)





def menu_screen():
    """
    This function draw the menu screen
    :return:
    """
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        window.fill((128, 128, 128))
        font = pygame.font.SysFont("arial.ttf", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        window.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()

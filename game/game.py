"""
Slime Invaders

Artwork from https://kenney.nl

This example shows how to:

* Get sprites to move as a group
* Change texture of sprites as a group
* Only have the bottom sprite in the group fire lasers
* Create 'shields' like in space invaders

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.slime_invaders
"""
import random
import arcade
#import numpy
WIDTH = 800
HEIGHT = 600
SPRITE_SCALING = 0.5

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_enemy = 0.5
SPRITE_SCALING_LASER = 0.8


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "RFI Shooter"

BULLET_SPEED = 5
SCREEN_SPEED = 2

MAX_PLAYER_BULLETS = 50

arcade.Sprite.set_texture = 1
# Game state
GAME_OVER = 1
PLAY_GAME = 0

import arcade
import arcade.gui

class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Click to start", WIDTH / 2, HEIGHT / 2,
                          arcade.color.BLACK, font_size=50, anchor_x="center")
        #arcade.draw_text("Click to start", WIDTH / 2, HEIGHT / 2 - 75,
                         #arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        MyGame.setup(game_view)
        self.window.show_view(game_view)

class MyGame(arcade.View):
    """ Main application class. """

    def __init__(self):
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None

        #variables that will hold the RFI attributes
        self.rfi_time = []
        self.rfi_frequency = []
        self.rfi_intensity = []

        # Textures for the enemy
        self.enemy_textures = None

        # State of the game
        self.game_state = PLAY_GAME

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        #self.set_mouse_visible(False)

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

        arcade.set_background_color(arcade.color.BLACK)

        # arcade.configure_logging()

    def setup_level_one(self):

        # Create rows and columns of enemies
        x_count = 7
        x_start = 380
        x_spacing = 60
        y_count = 5
        y_start = 420
        y_spacing = 40
        for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
            for y in range(y_start, y_spacing * y_count + y_start, y_spacing):

                # Create the enemy instance
                # enemy image from kenney.nl
                enemy = arcade.SpriteSolidColor(5, 5, arcade.color.RED)

                # Position the enemy
                enemy.center_x = x
                enemy.center_y = y

                # Add the enemy to the lists
                self.enemy_list.append(enemy)

    def setup(self):
        """
        Set up the game and initialize the variables.
        Call this method if you implement a 'play again' feature.
        """

        self.game_state = PLAY_GAME

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()

        # Set up the player
        self.score = 0

        # Image from kenney.nl
        self.player_sprite = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png/", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.bottom_y = 0
        self.player_list.append(self.player_sprite)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        self.setup_level_one()

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.enemy_list.draw()
        self.player_bullet_list.draw()
        self.player_list.draw()

        # Render the text
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)

        # Draw game over if the game state is such
        if self.game_state == GAME_OVER:
            arcade.draw_text("GAME OVER", 250, 300, arcade.color.WHITE, 55)
            self.set_mouse_visible(True)
            
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        # Gunshot sound
        arcade.play_sound(self.gun_sound)
        # Create a bullet
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

        # The image points to the right, and we want it to point up. So
        # rotate it.
        bullet.angle = 90

        # Give the bullet a speed
        bullet.change_y = BULLET_SPEED

        # Position the bullet
        bullet.center_x = self.player_sprite.center_x
        bullet.bottom = self.player_sprite.top

        # Add the bullet to the appropriate lists
        self.player_bullet_list.append(bullet)


    def update_enemies(self):

        # Move the enemy vertically
#        for enemy in self.enemy_list:
#            enemy.center_x += self.enemy_change_x

        # Check every enemy to see if any hit the edge. If so, reverse the
        # direction and flag to move down.
        move_down = False
        # for enemy in self.enemy_list:
        #     if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
        #         self.enemy_change_x *= -1
        #         move_down = True
        #     if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
        #         self.enemy_change_x *= -1
        #         move_down = True

        # Did we hit the edge above, and need to move t he enemy down?
        # if move_down:
        #     # Yes
        #     for enemy in self.enemy_list:
        #         # Move enemy down
        #         enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT
        #         # Flip texture on enemy so it faces the other way
        #         if self.enemy_change_x > 0:
        #             enemy.texture = self.enemy_textures[0]
        #         else:
        #             enemy.texture = self.enemy_textures[1]

    def process_player_bullets(self):

        # Move the bullets
        self.player_bullet_list.update()

        # Loop through each bullet
        for bullet in self.player_bullet_list:
            # Check this bullet to see if it hit a enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every enemy we hit, add to the score and remove the enemy
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1

                # Hit Sound
                arcade.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_update(self, delta_time):
        """ Movement and game logic """

        if self.game_state == GAME_OVER:
            return

        self.update_enemies()
        self.process_player_bullets()

        if len(self.enemy_list) == 0:
            self.setup_level_one()

    #def read_data(self):
        #read data from an npz file
        #from numpy import load
        #data = load('myFile.npy')
        #lst = data.files

        #for item in lst:
            #self.rfi_time
            #self.rfi_frequency
            #self.rfi_intensity


# class QuitButton(arcade.gui.UIFlatButton):
#     def on_click(self, event: arcade.gui.UIOnClickEvent):
#         arcade.exit()

# class StartButton(arcade.gui.UIFlatButton):
#     def on_click(self, event: arcade.gui.UIOnClickEvent):
#         # window = MyGame()
#         # #window.read_data()
#         # window.setup()
#         # arcade.run()
#         arcade.exit()


# class MyWindow(arcade.Window):
#     def __init__(self):
#         super().__init__(800, 600, "UIFlatButton Example", resizable=True)

#         # --- Required for all code that uses UI element,
#         # a UIManager to handle the UI.
#         self.manager = arcade.gui.UIManager()
#         self.manager.enable()

#         # Set background color
#         arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

#         # Render button
#         default_style = {
#             "font_name": ("calibri", "arial"),
#             "font_size": 15,
#             "font_color": arcade.color.WHITE,
#             "border_width": 2,
#             "border_color": None,
#             "bg_color": (21, 19, 21),

#             # used if button is pressed
#             "bg_color_pressed": arcade.color.WHITE,
#             "border_color_pressed": arcade.color.WHITE,  # also used when hovered
#             "font_color_pressed": arcade.color.BLACK,
#         }

#         red_style = {
#             "font_name": ("calibri", "arial"),
#             "font_size": 15,
#             "font_color": arcade.color.WHITE,
#             "border_width": 2,
#             "border_color": None,
#             "bg_color": arcade.color.REDWOOD,

#             # used if button is pressed
#             "bg_color_pressed": arcade.color.WHITE,
#             "border_color_pressed": arcade.color.RED,  # also used when hovered
#             "font_color_pressed": arcade.color.RED,
#         }

#         # Create a vertical BoxGroup to align buttons
#         self.v_box = arcade.gui.UIBoxLayout(space_between=20)

#         # Create the buttons
#         start_button = StartButton(text="Start Game", width=200)
#         self.v_box.add(start_button.with_space_around(bottom=20))

#         quit_button = QuitButton(text="Quit", width=200)
#         self.v_box.add(quit_button)

#         # Create a widget to hold the v_box widget, that will center the buttons
#         self.manager.add(
#             arcade.gui.UIAnchorWidget(
#                 anchor_x="center_x",
#                 anchor_y="center_y",
#                 child=self.v_box)
#         )
#     # def on_click_start(self, event):
#     #     print("Start:", event)
        
#     def on_draw(self):
#         self.clear()
#         self.manager.draw()
    
# class MenuView(arcade.View):
    # def on_show_view(self):
    #     arcade.set_background_color(arcade.color.WHITE)

    # def on_draw(self):
    #     self.clear()
    #     arcade.draw_text("Menu Screen", WIDTH / 2, HEIGHT / 2,
    #                      arcade.color.BLACK, font_size=50, anchor_x="center")
    #     arcade.draw_text("Click to advance.", WIDTH / 2, HEIGHT / 2 - 75,
    #                      arcade.color.GRAY, font_size=20, anchor_x="center")

    # def on_mouse_press(self, _x, _y,_button, _modifiers):
    #     game = MyGame()
    #     self.window.show_view(game)


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Different Views Example")
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()



if __name__ == "__main__":
    main()
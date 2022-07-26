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
import arcade
import numpy as np

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_enemy = 0.5
SPRITE_SCALING_LASER = 0.8


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "RFI Shooter"

BULLET_SPEED = 5
SCREEN_SPEED = 2

MAX_PLAYER_BULLETS = 50

# Game state
GAME_OVER = 1
PLAY_GAME = 0

NFREQS = 40
PIXEL_SIZE = SCREEN_WIDTH // NFREQS

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.background_List = None
        #variables that will hold the RFI attributes
        #will determine where the RFI is located on the screen
        
        # State of the game
        self.game_state = PLAY_GAME

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

        arcade.set_background_color(arcade.color.BLACK)

        # arcade.configure_logging()

    def setup_level_one(self):

        # Create rows and columns of enemies

        #the zip function will match the channel list with its corresponding amplitude list
        #go through and zip each list again to match the channel with its corresponding amplitude
        for i, (channel_lst, amplitude_lst) in enumerate(zip(self.rfi_channels, self.rfi_amplitudes)):
            for channel, amplitude in zip(channel_lst, amplitude_lst):
                
                # Create the enemy instance

                enemy = arcade.SpriteSolidColor(PIXEL_SIZE, PIXEL_SIZE, (255, 0, 0))

                # Position the enemy
                enemy.center_x = channel * PIXEL_SIZE
                enemy.center_y = i * PIXEL_SIZE
                enemy.change_y = -SCREEN_SPEED

                # Add the enemy to the lists
                print("adding enemy!!")
                self.enemy_list.append(enemy)

        
        # Create the background of squares
        data_range = (self.clean_data.max() - self.clean_data.min())
        self.clean_data -= self.clean_data.min()
        self.clean_data = self.clean_data / (data_range / 255.0)
        self.clean_data = self.clean_data.astype(int)

        self.background_list = arcade.ShapeElementList()
        for it, t in enumerate(self.clean_data):
            for inu, amp in enumerate(t):
                # Create a somewhat red square at a particular location
                sprite = arcade.create_rectangle_filled(inu*PIXEL_SIZE, it*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE, (amp, amp, 0))
                self.background_list.append(sprite)

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
        self.read_data()

        self.setup_level_one()

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.background_list.draw()
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
        self.enemy_list.update()

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

    def update_background_squares(self):
        self.background_list.move(0, -SCREEN_SPEED)

    def on_update(self, delta_time):
        """ Movement and game logic """

        if self.game_state == GAME_OVER:
            return

        self.update_enemies()
        self.process_player_bullets()
        self.update_background_squares()

    def read_data(self):
        """read data from an npz file"""
        from numpy import load
        self.clean_data = np.random.rand(30, NFREQS)
        self.rfi_channels = []
        self.rfi_amplitudes = []

        for t in self.clean_data:
            n = np.random.poisson(3)
            self.rfi_channels.append(np.random.choice(self.clean_data.shape[1], n, replace=False))
            self.rfi_amplitudes.append(5*np.random.uniform(size=n))

        # data = load('myFile.npy')
        # lst = data.files

        # for item in lst:
        #     self.rfi_time
        #     self.rfi_frequency
        #     self.rfi_intensity

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
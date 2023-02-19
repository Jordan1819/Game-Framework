# Author: Jordan Waite
# Inspiration and research for this project obtained from https://api.arcade.academy ,
# https://w3schools.com , https://stackoverflow.com , and previous projects of mine.

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Jumpbot"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
STAR_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

class game(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Creating the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        #Create a scene object
        self.scene = None

        #This variable will hold the player's sprite
        self.player_sprite = None

        #Instantiating the physics engine
        self.physics_engine = None

        #Create a camera that can allow for traversing the screen more immersively
        self.camera = None

        #Create background attribute to store image in later
        self.background = None

        #Assign inbuilt sounds to attributes
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

    def setup(self):
        
        #Here we set up the camera
        self.camera = arcade.Camera(self.width, self.height)

        #Setting the color of the game window
        self.background = arcade.load_texture(":resources:images/cybercity_background/back-buildings.png")

        #Initialize the scene object here
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls, use_spatial_hash=True")

        #Initiate the players sprite
        image_source = ":resources:images/animated_characters/robot/robot_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 75
        self.player_sprite.center_y = 150
        self.scene.add_sprite("Player", self.player_sprite)

        #Create the ground, using a loop to create the floor of the game window
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/snowCenter.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Put some obstacles on the ground
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                ":resources:images/tiles/brickTextureWhite.png", TILE_SCALING
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        #This will add the stars
        for x in range(128, 1250, 256):
            star = arcade.Sprite(":resources:images/items/star.png", STAR_SCALING)
            star.center_x = x
            star.center_y = 96
            self.scene.add_sprite("Stars", star)

        #Implement arcade's built-in physics engine to identify the sprites that cannot be moved through
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"])

    def on_draw(self):
        #Clear the screen in case it's a level other than one
        self.clear()

        #Drawing the backgound image
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                    self.background)

        #Activate the earlier established camera attribute
        self.camera.use()

        # Draw the sprites onto the screen
        self.scene.draw()

    def on_key_press(self, key, modifiers):

        #Here is where we assign player controls to WASD and assign positive and negative x and y values to those key presses
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
            arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        
        #Here we assign a zero value to the directional value when the key is released
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
    
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        #This section of code ensures that the camera value does not travel past zero
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        
        #This allows the scene to allow for multiple key presses and the utilization of the game engine 
        self.physics_engine.update()

        #Here we set up collision with the stars
        star_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Stars"]
        )

        #Remove the stars we hit from the screen
        for star in star_list:
            star.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)

        #Update the camera values
        self.center_camera_to_player()
        


def main():
    window = game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
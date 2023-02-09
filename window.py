import arcade
class createWindow():
    def launch(self):
        arcade.open_window(1000, 600, "Jumper")

        #This keeps the window open
        arcade.run()

#Instantiate the class
#because we are only using
#one instance (I think)
w = createWindow()


if __name__ == "__main__":
    w.launch()

import sys
import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button

def run_game():
	"""Initialize pygame, settings, and screen object"""
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion 2: The awakening")
	
	#Make a ship
	ship = Ship(ai_settings, screen)
	#Make an Alien
	alien = Alien(ai_settings, screen)
	#Make a group to store the bullets
	bullets = Group()
	#Make a group to store the aliens
	aliens = Group()
	#Create the alien fleet
	gf.create_fleet(ai_settings, screen, ship, aliens)
	#Create an instance to store the game statistics
	stats = GameStats(ai_settings)
	#Make a play button
	play_button = Button(ai_settings, screen, "Play")
	#Starting the loop for the game
	while True:
		
		gf.check_events(ai_settings, screen, ship, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
			gf.update_aliens(ai_settings,stats, screen, ship, aliens, bullets)
		gf.update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button)
run_game()	

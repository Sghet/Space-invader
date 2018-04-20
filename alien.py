import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	""" A class to represent a single alien in the fleet"""
	
	def __init__(self, ai_settings, screen):
		"""Initialize the alien and its current position"""
		super(Alien,self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#Load the alien image
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		#Start each new alien in the top left corner
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		#Store the alien exact position
		self.x = float(self.rect.x)
		
	def blitme(self):
		"""Draw the alien a its current position"""
		self.screen.blit(self.image, self.rect)
	
	def update(self):
		"""Move the alien right"""
		self.x += (self.ai_settings.alien_speed_factor *
			self.ai_settings.fleet_direction)
		self.rect.x = self.x
		
	def check_edges(self):
		"""Return true if aliens it hits the edge"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
				
		

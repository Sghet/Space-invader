import pygame

class Ship():
	
	def __init__(self, ai_settings, screen):
		"""Initialize ship and its current position"""
		self.screen = screen
		self.ai_settings = ai_settings
		
		#Load the ship image and gets its rect.
		self.image = pygame.image.load('images\ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#Start each new ship at the bottom center
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		#Store a decimal value for the ship center's
		self.center = float(self.rect.centerx)
		
		#Movement Flag.
		self.moving_right = False
		self.moving_left = False
	
	def update(self):
		"""Update the ship position based on the flag"""
		#Update the ship center value, not the rect.
		
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
			
		#Update rect object from self.center
		self.rect.centerx = self.center
			
	def blitme(self):
		"""Draw the ship in its current position"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""Center the ship on screen"""
		self.center = self.screen_rect.centerx

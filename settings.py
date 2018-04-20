class Settings():
	""" A class to store the settings of Alien Invasion"""
	
	def __init__(self):
		""" Initialize game screen"""
		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)
		
		#Ship settings
		self.ship_speed_factor = 1.8
		self.ship_limit = 3
		
		#Alien settings
		self.alien_speed_factor = 1.8
		self.fleet_drop_speed = 20
		#flet_direction of 1 represent right, -1 left
		self.fleet_direction = 1
		#Bullet settings	
		self.bullet_speed_factor = 3
		self.bullet_width = 5
		self.bullet_height = 15
		self.bullet_color = 60, 60 , 60
		self.bullets_allowed = 5
		
		

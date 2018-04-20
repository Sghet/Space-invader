import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from ship import Ship

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	""" Respond to keypresses"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		ship.moving_left = True
	if event.key == pygame.K_q:
		sys.exit()
	
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
		
def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet it the limit has not been reach"""
	#Create a new bullet and add it to the bullet groups
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens that fit in the screen"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of aliens that fit in the screen"""
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):	
	"""Create an alien and place it in the row"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a full fleet of aliens"""
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_row =  get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	#Create the fleet of aliens.
	for row_number in range(number_row):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
		
def check_keyup_events(event, ship):
	"""Respond to key releases""" 
	if event.key == pygame.K_RIGHT:	
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False	
				
def check_events(ai_settings, screen, ship, bullets):
	"""Respond to mouse and keyboard input"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()			
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
			
def update_screen(ai_settings, screen, ship, stats, bullets, aliens, play_button):
	"""Update the images in the screen"""
		
	#Redraw the screen during each pass through the loop.
	screen.fill(ai_settings.bg_color)		
	#Redraw all the bullets behind the ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	aliens.draw(screen)
	ship.blitme()
	#Draw the play button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()		
	#Make the most recent drawn screen visible.
	pygame.display.flip()
		

def update_bullets(ai_settings, screen, ship, aliens, bullets):
	"""Update position of bullets and get rid of old bullets"""
	bullets.update()
	#Get rids of the bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets)
	
def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets):
	"""Respond to any bullet-alien collision"""
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if len(aliens) == 0:
		#Destroy existing bullets and refill the fleet
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
	
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	"""Check if the aliens is in the edge and update the position of the aliens"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	#Look for alien-Bullet collision
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
	
def check_fleet_edges(ai_settings, aliens):
	"""Respond if the aliens reach the edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	"""Drop the fleet and change directions"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	"""Respond to a ship being hit"""
	if stats.ship_left > 0:
		#Decrement the ships remaining
		stats.ship_left -= 1
		#Empty the list of bullets and aliens
		aliens.empty()
		bullets.empty()
		#Create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		#Pause
		sleep(0.5)
	else:
		stats.game_active = False
	
	
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	"""Check if any alien hit the bottom"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#Treat this the same as if the ship was hit
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break
			

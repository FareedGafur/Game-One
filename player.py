import pygame, sys
from pygame.math import Vector2 as vector
from os import walk
from entity import Entity


class Player(Entity):

	def __init__(self, pos, groups, path, collision_sprites, create_bullet):

		super().__init__(pos, groups, path, collision_sprites)

		self.create_bullet = create_bullet
		self.bullet_shot = False
		self.sound = pygame.mixer.Sound('../sound/bullet.wav') # Bullet sound
		self.health = 1000


	def get_status(self):

		# idle

		if self.direction.x == 0 and self.direction.y == 0: #Plays idle animation if player is not moving

			self.status = self.status.split('_')[0] + '_idle'

		# Attacking

		if self.attacking:

			self.status = self.status.split('_')[0] + '_attack' #Plays attack animation if attacking


	def input(self):

		keys = pygame.key.get_pressed()
		
		if not self.attacking: #Only move when not shooting

			# Vertical Movement

			if keys[pygame.K_UP]:
				self.status = 'up'
				self.direction.y = -1

			elif keys[pygame.K_DOWN]:
				self.status = 'down'
				self.direction.y = 1

			else:
				self.direction.y = 0


			# Horizontal Movement

			if keys[pygame.K_RIGHT]:
				self.status = 'right'
				self.direction.x = 1

			elif keys[pygame.K_LEFT]:
				self.status = 'left'
				self.direction.x = -1

			else:
				self.direction.x = 0

			if keys[pygame.K_SPACE]:
				self.attacking = True # Sets staccking to true if space is pressed
				self.direction = vector() # Get the direction
				self.frame_index = 0 # Set frame index to 0 for animations (start from frame 0)
				self.bullet_shot = False 

				match self.status.split('_')[0]: #Animation will vary depending on what way the player  is facing (Status comes into play here)
					case 'right' : self.bullet_direction = vector(1,0)
					case 'left' : self.bullet_direction = vector(-1,0)
					case 'up' : self.bullet_direction = vector(0,-1)
					case 'down' : self.bullet_direction = vector(0,1)


	def animate(self, dt):

		current_animation = self.animations[self.status]

		self.frame_index += 7 * dt

		if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot: #once frame 2 is displayed, creates the bullet as part of the attack animation
			
			bullet_start_pos = self.rect.center + self.bullet_direction * 80
			self.sound.play()
			self.create_bullet(bullet_start_pos, self.bullet_direction)
			self.bullet_shot = True


		if self.frame_index >= len(current_animation): # Ensures the frame index doesnt exceed the amount of frames 

			self.frame_index = 0

			if self.attacking:

				self.attacking = False

		self.image = current_animation[int(self.frame_index)] #Updates the frame
		self.mask = pygame.mask.from_surface(self.image) #Updates the mask

	def check_death(self): #Checks to see if the player has died; if so, close the game

		if self.health <= 0:
			pygame.quit()
			sys.exit()

	def update(self, dt):
		self.check_death()
		self.get_status()
		self.input()
		self.move(dt)
		self.animate(dt)
		self.blink()
		self.vulnerability_timer()

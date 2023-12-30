import pygame
from entity import Entity
from pygame.math import Vector2 as vector

class Monster:

	def get_player_distance_direction(self):

		# Gets enemy and player position
		enemy_pos = vector(self.rect.center)
		player_pos = vector(self.player.rect.center)

		# Gets the distance between enemy and player
		distance = (player_pos - enemy_pos).magnitude()

		#Constanly updates the distance from player
		if distance != 0:
			direction = (player_pos - enemy_pos).normalize()

		else:
			direction = vector()

		return (distance, direction)

	def face_player(self):

		distance, direction = self.get_player_distance_direction()

		if distance < self.notice_radius: #If player enters the monster's notice range, it will face the layer

			if -0.5 < direction.y < 0.5:

				if direction.x < 0: # player to the left
					self.status = 'left_idle'

				elif direction.x > 0: # player to the right
					self.status = 'right_idle'
			else:
				if direction.y < 0: # player to the top
					self.status = 'up_idle'

				elif direction.y > 0: # player to the bottom
					self.status = 'down_idle'

	def walk_to_player(self):

		distance, direction = self.get_player_distance_direction()

		if self.attack_radius < distance < self.walk_radius: # While the ditance is between the attack radius and the walk radius, the monster will move towards the player
			self.direction = direction
			self.status = self.status.split('_')[0]
		else:
			self.direction = vector()



class Coffin(Entity, Monster):

	def __init__(self, pos, groups, path, collision_sprite, player):
		
		super().__init__(pos, groups, path, collision_sprite)
		
		# overwrite
		self.speed = 140

		# player interaction
		self.player = player
		self.notice_radius = 550
		self.walk_radius = 400
		self.attack_radius = 50

	
	def attack(self):

		distance = self.get_player_distance_direction()[0]

		if distance < self.attack_radius and not self.attacking: #If monster is within attack range and self.attacking is flase, initiate attack

			self.attacking = True
			self.frame_index = 0

		if self.attacking:

			self.status = self.status.split('_')[0] + '_attack' # Switch to attack frame


	def animate(self, dt):

		current_animation = self.animations[self.status]


		if int(self.frame_index) == 4 and self.attacking: #On the fourth frame, if the player is withing the coffin's attack radius, it will be damaged
			
			if self.get_player_distance_direction()[0] < self.attack_radius:

				self.player.damage()



		self.frame_index += 7 * dt


		if self.frame_index >= len(current_animation): # Ensures the frame index doesnt exceed the amount of frames 

			self.frame_index = 0

			if self.attacking:

				self.attacking = False

		self.image = current_animation[int(self.frame_index)]
		self.mask = pygame.mask.from_surface(self.image)


	def update(self, dt):
		self.face_player()
		self.walk_to_player()
		self.attack()

		self.move(dt)
		self.animate(dt)
		self.blink()

		self.check_death()
		self.vulnerability_timer()



class Cactus(Entity, Monster):

	def __init__(self, pos, groups, path, collision_sprites, player, create_bullet):
		super().__init__(pos, groups, path, collision_sprites)
		
		# overwrite
		self.speed = 90

		# player interaction
		self.player = player
		self.notice_radius = 600
		self.walk_radius = 500
		self.attack_radius = 350

		# bullets
		self.create_bullet = create_bullet
		self.bullet_shot = False
		self.sound = pygame.mixer.Sound('../sound/bullet.wav')

	def attack(self):

		distance = self.get_player_distance_direction()[0]

		if distance < self.attack_radius and not self.attacking: #If monster is within attack range and self.attacking is flase, initiate attack

			self.attacking = True
			self.frame_index = 0
			self.bullet_shot = False

		if self.attacking:

			self.status = self.status.split('_')[0] + '_attack' # Switch to attack frame

	def animate(self, dt):

		current_animation = self.animations[self.status]


		if int(self.frame_index) == 6 and self.attacking and not self.bullet_shot: #While on the 6th frame of the attack animation, create bullet which moves towards player

			direction = self.get_player_distance_direction()[1]
			pos = self.rect.center + direction * 150 #Controls bullets movement/ speed
			self.create_bullet(pos, direction) # Creates the bullet
			self.sound.play()
			self.bullet_shot = True
		
		
		self.frame_index += 7 * dt

		if self.frame_index >= len(current_animation): # Ensures the frame index doesnt exceed the amount of frames 

			self.frame_index = 0

			if self.attacking:

				self.attacking = False

		self.image = current_animation[int(self.frame_index)] # Updates image and mask of the cactus monster
		self.mask = pygame.mask.from_surface(self.image)

	def update(self, dt):
		self.face_player()
		self.walk_to_player()
		self.attack()

		self.move(dt)
		self.animate(dt)
		self.blink()

		self.check_death()
		self.vulnerability_timer()

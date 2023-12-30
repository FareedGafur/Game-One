import pygame, sys
from settings import *
from player import Player 
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet
from monster import Coffin, Cactus

class AllSprites(pygame.sprite.Group):

	def __init__(self):
		super().__init__()
		self.offset = vector()
		self.display_surface = pygame.display.get_surface()
		self.bg = pygame.image.load('C:/Users/faree/Downloads/Python Projects/Western Shooter/p1_setup/graphics/other/bg.png').convert()

	def customize_draw(self, player):

		# change the offset vector

		self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/2

		# blit the surfaces

		self.display_surface.blit(self.bg, -self.offset)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			
			offset_rect = sprite.image.get_rect(center = sprite.rect.center) # gets the offset position for each sprite
			offset_rect.center -= self.offset
			self.display_surface.blit(sprite.image, offset_rect) #blits the offsetted image to the screen, making it look like a camera view for the game




class Game:

	def __init__(self):

		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Western shooter')
		self.clock = pygame.time.Clock()
		self.bullet_surf = pygame.image.load('C:/Users/faree/Downloads/Python Projects/Western Shooter/p1_setup/graphics/other/particle.png').convert_alpha()

		# groups

		self.all_sprites = AllSprites()
		self.obstacles = pygame.sprite.Group() 
		self.bullets = pygame.sprite.Group()
		self.monsters = pygame.sprite.Group()

		# Setup	

		self.setup()

		# Music

		self.music = pygame.mixer.Sound('../sound/music.mp3')
		self.music.set_volume(0.5)
		self.music.play(loops = -1)




	def CreateBullet(self, pos, direction):

		Bullet(pos, direction, self.bullet_surf,  [self.all_sprites, self.bullets]) # Calls bullet class from sprite.py

 
	def bullet_collision(self):

		# bullet obstacle collision
		for obstacle in self.obstacles.sprites():
			pygame.sprite.spritecollide(obstacle, self.bullets, True, pygame.sprite.collide_mask) # Bullet sprites are killed if it makes contact with obstacles

		#bullet monster collision
		for bullet in self.bullets.sprites():
			sprites = pygame.sprite.spritecollide(bullet, self.monsters, False, pygame.sprite.collide_mask) #Checks to see if bullet collides with sprites
			if sprites:
				bullet.kill() # Kills bullet sprite if it collides with a sprite
				for sprite in sprites:
					sprite.damage() # Damages the sprite if it collides with the bullet

		# player bullet collision
		if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
			self.player.damage() # Damages the player if it collides with the bullet

	def setup(self):

		tmx_map = load_pygame('C:/Users/faree/Downloads/Python Projects/Western Shooter/Map.tmx') # Loads the map from Tiles
		
		# Tiles

		for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles(): # Adds in fences to the map

			Sprite((x*64,y*64), surf, [self.all_sprites, self.obstacles])

			
		# objects
		for obj in tmx_map.get_layer_by_name('Object'): # Adds the objects in the map (besides fence)

			Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])



		for obj in tmx_map.get_layer_by_name('Entities'): 

			if obj.name == 'Player': # Spawns in the player
				self.player = Player(
					pos = (obj.x,obj.y), 
					groups = self.all_sprites, 
					path = PATHS['player'], 
					collision_sprites = self.obstacles, 
					create_bullet = self.CreateBullet)

			if obj.name == 'Coffin': # Spawns the coffin entities
				Coffin((obj.x,obj.y), [self.all_sprites, self.monsters], PATHS['coffin'], self.obstacles, self.player)	

			if obj.name == 'Cactus':  # Spawns the cactus entities
				Cactus((obj.x,obj.y), [self.all_sprites, self.monsters], PATHS['cactus'], self.obstacles, self.player, self.CreateBullet)


	def run(self):

		while True:

			# event loop 

			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			# delta time
			dt = self.clock.tick() / 1000

			# update groups
			self.all_sprites.update(dt)
			self.bullet_collision()

			# draw groups
			self.display_surface.fill('black')
			self.all_sprites.customize_draw(self.player)


			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()
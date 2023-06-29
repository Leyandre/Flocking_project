import pygame
from pygame.locals import *
import random
import math

width = 1000
height = 500
framerate = 100
birds = 100

class vecteur:

    def __init__(self, a_x, b_y, c_limite = None):
        self.x = a_x
        self.y = b_y
        self.limite = c_limite
        self.ang = self.get_ang()
        self.norm = self.get_norm()
        self.list = [a_x, b_y]
        self.moy_x = a_x
        self.moy_y = b_y
        self.moy_ang = self.ang
        self.moy_n = 1

    def get_norm(self):
        norm = math.sqrt(((self.x) ** 2) + ((self.y) ** 2))
        return norm

    def get_ang(self):
        if ((self.x != 0) or (self.y != 0)):
            ang = get_sign(self.y) * math.acos(self.x / math.sqrt(((self.x) ** 2) + ((self.y) ** 2)))
        else:
            ang = 0
        return ang

    def maj_vect(self):
        self.ang = self.get_ang()
        self.norm = self.get_norm()
        self.list[0] = self.x
        self.list[1] = self.y
        self.moy()

    def modif_add_ang(self, a_norm, a_rad):
        self.x += (a_norm * math.cos(a_rad))
        self.y += (a_norm * math.sin(a_rad))
        self.maj_vect()

        self.ang = a_rad
        self.norm = a_norm

    def modif_ang(self, a_norm, a_rad):
        self.x = (a_norm * math.cos(a_rad))
        self.y = (a_norm * math.sin(a_rad))
        self.maj_vect()

        self.ang = a_rad
        self.norm = a_norm

    def get_vect_by_mult_list(self, c):
        self.x = 0
        self.y = 0

        for i in range(len(c)):
            self.x += c[i][0]
            self.y += c[i][1]

        self.maj_vect()

    def get_vect_by_list(self, c):
        self.x = c[0]
        self.y = c[1]
        self.maj_vect()

    def add_vect_by_list(self, c):
        self.x += c[0]
        self.y += c[1]
        self.maj_vect()

    def sub_vect_by_list(self, c):
        self.x -= c[0]
        self.y -= c[1]
        self.maj_vect()

    def mul_vect_by_list(self, c):
        self.x *= c[0]
        self.y *= c[1]
        self.maj_vect()

    def div_vect_by_list(self, c):
        self.x /= c[0]
        self.y /= c[1]
        self.maj_vect()

    def normalize(self):
        self.x = math.cos(self.ang)
        self.y = math.sin(self.ang)

    def limit(self):
        if self.limite != None:
            if abs(self.norm) > self.limite:
                self.x /= (self.norm / self.limite)
                self.y /= (self.norm / self.limite)

            self.maj_vect()

    def moy(self):
        self.moy_x = (((self.moy_x * self.moy_n) + self.x) / (self.moy_n + 1))
        self.moy_y = (((self.moy_y * self.moy_n) + self.y) / (self.moy_n + 1))
        self.moy_ang = (((self.moy_ang * self.moy_n) + self.ang) / (self.moy_n + 1))
        self.moy_n += 1

def dist(a, b):
    x = abs(a.x - b.x)
    y = abs(a.y - b.y)

    distance = math.sqrt(x ** 2 + y ** 2)

    return distance

def get_ang_line(a, b):
    x = abs(b.x - a.x)
    norme = dist(a, b)

    if (norme != 0):

        ang = math.acos(x / norme)
    else:
        ang = 0

    return ang

def check_out(a):
    # verifie si point en dehors de la fenetre
    if (a.x > width):
        a.x -= width
    if (a.x < 0):
        a.x += width
    if (a.y > height):
        a.y -= height
    if (a.y < 0):
        a.y += height

def get_sign(p):
    if (p != 0):
        signe = (p / abs(p))
    else:
        signe = 1
    return signe

def modulo(x, mod):
    boucle = True
    stack = abs(x)

    while boucle:
        if stack > (mod / 2):
            stack -= mod
        else:
            boucle = False

    return (get_sign(x) * stack)

def soust_ang(x, y, mod):

    if get_sign(y) != get_sign(x):
        if x < 0:
            while y > 0:
                y -= mod
        else:
            while x < 0:
                x += mod

    delta = x - y

    return delta

class oiseau():

    def __init__(self, idt, colour = (255, 0, 0)):
        self.maxvit = 3
        self.maxforce = 1
        self.coef_evit_wall = 1000
        self.coef_evit_bird = 100
        self.coef_cohe = 1

        self.vit_init = 2

        self.pos = vecteur(random.randint(10, (width - 10)), random.randint(10, (height -10)))
        self.vit = vecteur(random.uniform(-self.vit_init, self.vit_init), random.uniform(-self.vit_init, self.vit_init), self.maxvit)
        self.acc = vecteur(0, 0, self.maxforce)

        self.ident = idt
        self.couleur = colour
        self.vue_dist = 60
        self.vue_dist_obs = 10
        self.vue_dist_obs_wall = 20
        self.vue_ang = math.pi

        self.birds_in_sight = []
        self.obs_in_sight = []
        self.wall_in_sight = []

        self.pos_av = vecteur(0, 0)
        self.vit_av = vecteur(0, 0)

        self.acc_coh = vecteur(0, 0)
        self.acc_alig = vecteur(0, 0)
        self.acc_coll = vecteur(0, 0)
        self.acc_wall = vecteur(0, 0)
        self.acc_rand = vecteur(0, 0)

    def check_sight(self, swarm):
        # nettoie la liste avant de la remplir
        self.birds_in_sight.clear()
        self.obs_in_sight.clear()
        self.index_wall = 0

        #met dans liste birds_in_sight tous les oiseaux dans sa vue
        for i in range(birds):
            #on fait attention a ce qu'il ne se prenne pas en compte
            if i != self.ident:
                if self.ident == 0:
                    swarm[i].couleur = (255, 0, 0)
                if (dist(self.pos, swarm[i].pos) <= self.vue_dist):

                    vect_vision = vecteur((swarm[i].pos.x - self.pos.x), (swarm[i].pos.y - self.pos.y))
                    delta_ang = abs(vect_vision.ang - self.vit.ang)

                    if(delta_ang <= (self.vue_ang / 2)):
                        self.birds_in_sight.append(swarm[i])

                        if self.ident == 0:
                            swarm[i].couleur = (0, 255, 255)

                        if (dist(self.pos, swarm[i].pos) <= self.vue_dist_obs):
                            self.obs_in_sight.append(swarm[i].pos)

                            if self.ident == 0:
                                swarm[i].couleur = (0, 255, 0)

    def check_wall(self):
        self.wall_in_sight.clear()
        if (height - self.pos.y) < self.vue_dist_obs_wall:
            pos_mur_haut = vecteur(self.pos.x, height)
            self.wall_in_sight.append(pos_mur_haut)

        if self.pos.y < self.vue_dist_obs_wall:
            pos_mur_bas = vecteur(self.pos.x, 0)
            self.wall_in_sight.append(pos_mur_bas)

        if (width - self.pos.x) < self.vue_dist_obs_wall:
            pos_mur_droite = vecteur(width, self.pos.y)
            self.wall_in_sight.append(pos_mur_droite)

        if self.pos.x < self.vue_dist_obs_wall:
            pos_mur_gauche = vecteur(0, self.pos.y)
            self.wall_in_sight.append(pos_mur_gauche)

    def vit_aver(self):
        #on reinitialise la vitesse moyenne
        self.vit_av.get_vect_by_list([0, 0])

        for i in range(len(self.birds_in_sight)):

            self.vit_av.add_vect_by_list(self.birds_in_sight[i].vit.list)

        n = len(self.birds_in_sight)
        self.vit_av.div_vect_by_list([n, n])

    def pos_aver(self, liste_vecteur):
        # on reinitialise la position moyenne
        self.pos_av.get_vect_by_list([0, 0])

        for i in range(len(liste_vecteur)):
            if liste_vecteur == self.birds_in_sight:
                self.pos_av.add_vect_by_list(self.birds_in_sight[i].pos.list)
            else:
                self.pos_av.add_vect_by_list(liste_vecteur[i].list)

        n = len(liste_vecteur)
        self.pos_av.div_vect_by_list([n, n])

    def alignement(self):

        if len(self.birds_in_sight) > 0:
            self.vit_aver()

            #donne a l'acceleration d'alignement le delta entre vit_av et la vitesse
            self.acc_alig.get_vect_by_list([(self.vit_av.x - self.vit.x), (self.vit_av.y - self.vit.y)])

    def cohesion(self):

        if len(self.birds_in_sight) > 0:
            #on prend la position moyenne des oiseaux autour
            self.pos_aver(self.birds_in_sight)

            target = vecteur((self.pos_av.x - self.pos.x), (self.pos_av.y - self.pos.y))

            self.acc_coh.get_vect_by_list([(target.x - self.vit.x), (target.y - self.vit.y)])
            self.acc.maj_vect()
            self.acc_coh.mul_vect_by_list([self.coef_cohe, self.coef_cohe])

    def evitement(self):
        self.pos_aver(self.obs_in_sight)

        collision = vecteur((self.pos.x - self.pos_av.x), (self.pos.y - self.pos_av.y))

        self.acc_coll.get_vect_by_list([0, 0])

        if(abs(collision.x) >= 1 or abs(collision.y) >= 1):
            if abs(collision.x) >= 1:
                self.acc_coll.x = (self.coef_evit_bird / collision.x)

            if abs(collision.y) >= 1:
                self.acc_coll.y = (self.coef_evit_bird / collision.y)

        #si l'obstacle est a moins de 1 de lui
        else:
            self.acc_coll.x = self.coef_evit_bird * get_sign(collision.x)
            self.acc_coll.y = self.coef_evit_bird * get_sign(collision.y)

        self.acc_coll.maj_vect()

    def check_danger(self, ang_collision):

        if((math.pi / 2) > abs(self.acc.ang - ang_collision)):
            print("danger !! ang_acc :  ", self.acc.ang)
            return True
        else:
            return False

    def evitement_wall(self):
        self.pos_aver(self.wall_in_sight)

        steer_norm = (self.vit.norm / dist(self.pos, self.pos_av))

        collision = vecteur((self.pos.x - self.pos_av.x), (self.pos.y - self.pos_av.y))
        collision_inv = vecteur(-collision.x, -collision.y)

        delta = soust_ang(self.vit.ang, collision_inv.ang, (2 * math.pi))
        delta = modulo(delta, (2 * math.pi))

        self.acc_wall.get_vect_by_list([0, 0])

        if(steer_norm <= self.vit.norm):
            steer_ang = get_sign(delta) * (math.pi * (1 / dist(self.pos, self.pos_av)))
            self.acc_wall.modif_add_ang((self.coef_evit_wall * steer_norm), (self.vit.ang + steer_ang))

        #si l'obstacle est a moins de 1 de lui
        else:
            steer_ang = (get_sign(delta) * math.pi)
            self.acc_wall.modif_ang((self.coef_evit_wall * self.vit.norm), (self.vit.ang + steer_ang))

        self.acc_wall.maj_vect()

    def reinit(self, swarm):
        self.check_sight(swarm)
        self.check_wall()
        self.acc.get_vect_by_list([0, 0])
        self.acc_wall.get_vect_by_list([0, 0])
        self.acc_coll.get_vect_by_list([0, 0])
        self.acc_coh.get_vect_by_list([0, 0])
        self.acc_alig.get_vect_by_list([0, 0])

    def reaction(self, swarm):

        self.reinit(swarm)

        #si aucun oiseau en vue pas de réaction de groupe mais evitement mur possible
        #print(self.ident," : ",len(self.birds_in_sight),", ",len(self.wall_in_sight)," ; ")
        if(len(self.birds_in_sight) != 0 or len(self.wall_in_sight) != 0):

            self.alignement()

            self.cohesion()

            if len(self.obs_in_sight) > 0:
                self.evitement()

            self.acc.get_vect_by_mult_list([self.acc_alig.list, self.acc_coh.list, self.acc_alig.list, self.acc_coll.list, self.acc_wall.list])
            self.acc.limit()

            if len(self.wall_in_sight) > 0:
                self.evitement_wall()
                self.acc.get_vect_by_list(self.acc_wall.list)

        else:
            self.acc.modif_ang(1, random.normalvariate(self.vit.ang, 1))


        self.move()

    def move(self):

        self.vit.add_vect_by_list(self.acc.list)
        self.vit.limit()

        self.pos.add_vect_by_list(self.vit.list)

        check_out(self.pos)

def initialisation(liste_birds):
    for w in range(birds):
        liste_birds.append(oiseau(w))
        if w == 0:
            liste_birds[w].couleur = (0, 0, 255)

def manage_birds(fenetre, boids):

    for t in range(birds):
        boids[t].reaction(boids)
        draw_birds(fenetre, boids[t])

def draw_birds(fenetre, bird):
    taille = 2
    point = vecteur(((bird.vit.x * taille) + bird.pos.x), ((bird.vit.y * taille) + bird.pos.y))
    pygame.draw.line(fenetre, bird.couleur, [bird.pos.x, bird.pos.y], [point.x, point.y], 2)

    pygame.draw.circle(fenetre, bird.couleur, bird.pos.list, 2)

def flocking():
    pygame.init()

    fenetre = pygame.display.set_mode((width, height))

    horloge_framerate = pygame.time.Clock()

    fenetre.fill(0x000000)

    refresh = True
    init = True
    boids = []

    while refresh:
        fenetre.fill(0x000000)

        if (init == True):
            initialisation(boids)
            init = False

        manage_birds(fenetre, boids)

        for event in pygame.event.get():
            if event.type == QUIT:
                refresh = False

        pygame.display.flip()

        horloge_framerate.tick(framerate)

flocking()

import math
import pygame
pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Planet System')

FONT = pygame.font.SysFont('comicsans', 16)

class Planet: 
    def __init__(self, r_x, r_y, r, m, name, color, sun_status=False):
        self.name = name
        
        self.r_x = r_x
        self.r_y = r_y 

        self.r = r 
        self.m = m
        self.color = color 

        self.orbit = list()
        self.sun_status = sun_status 
        self.distance_sun = 0

        self.xv = 0
        self.yv = 0

        self.SCALE = 50 / 1.496e11


    distance = lambda  self, f_pl_dist, s_pl_dist: f_pl_dist - s_pl_dist

    sq_r = lambda self, dist_x, dist_y: math.sqrt(dist_x ** 2 + dist_y ** 2)

    def f_axes(self, sec_planet, G):
        dist_x = self.distance(sec_planet.r_x, self.r_x)
        dist_y = self.distance(sec_planet.r_y, self.r_y)

        distance_planets = self.sq_r(dist_x, dist_y)

        if sec_planet.sun_status == True:
            self.distance_sun = distance_planets

        f = G * self.m * sec_planet.m / distance_planets ** 2 
       
        theta = math.atan2(dist_y, dist_x)
            

        f_x = math.cos(theta) * f
        f_y = math.sin(theta) * f 

        return f_x, f_y
    
    def draw(self, win):
        x = self.r_x * self.SCALE + WIDTH / 2
        y = self.r_y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2: 
            updated_points = []
            
            for point in self.orbit: 
                x, y = point
                x =  x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.r)

        if not self.sun_status:
            distance_text = FONT.render('{}'.format(self.name), 1, (255, 255, 255))
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

class PlanetSys: 
    def __init__(self):
        self.planets = list()
        self.status = False
        self.G = 6.6743e-11
        # 149.6e6 * 1000
        self.AU = 1.496e11
        self.days = 365
        self.day_time =  24 * 60 * 60

        self.planets.append(Planet(0, 0, 13, 1.9891e30, 'Sun', (255, 255, 0), True))
        
        self.planets.append(Planet(.39 * self.AU, 0, 2, 0.33e24, 'Mercury', (255, 255, 0), False))
        self.planets[1].yv = -47400
        
        self.planets.append(Planet(.72 * self.AU, 0, 3, 4.87e24, 'Venus', (255, 255, 0), False))
        self.planets[2].yv = -35000
        
        self.planets.append(Planet(1 * self.AU, 0, 5, 5.97e24, 'Earth', (255, 255, 0), False))
        self.planets[3].yv = -29800
        
        self.planets.append(Planet(1.52 * self.AU, 0, 4, 0.642e24, 'Mars', (255, 255, 0), False))
        self.planets[4].yv = -24100
        
        self.planets.append(Planet(5.2 * self.AU, 0, 9, 1898e24, 'Jupiter', (255, 255, 0), False))
        self.planets[5].yv = -13100
        
        self.planets.append(Planet(9.54 * self.AU, 0, 8, 568e24, 'Saturn', (255, 255, 0), False))
        self.planets[6].yv = -9700
  
        self.planets.append(Planet(19.2 * self.AU, 0, 7, 86.8e24, 'Uranus', (255, 255, 0), False))
        self.planets[7].yv = -6800
 
        self.planets.append(Planet(30.06 * self.AU, 0, 6, 102e24, 'Neptune', (255, 255, 0), False))
        self.planets[8].yv = -5400


        self.planets.append(Planet(-5.2 * self.AU, 0, 4, 1898e24, 'L3', (255, 255, 0), False))
        self.planets[9].yv = 13100
        

        m1 = 1.9891e30
        m2 = 1e25
        R = 5.2 * self.AU
        r1 = m2*R/(m1+m2)
        r2 = m1*R/(m1+m2)

        v1 = math.sqrt(self.G*m2*r1/R**2)
        v2 = math.sqrt(self.G*m1*r1/R**2)
        w = v2 / r2
        theta = 60*math.pi/180


        print(w)

        self.planets.append(Planet(R * math.cos(theta), -R * math.sin(theta), 4, 1e25, 'L4', (255, 255, 0), False))
        self.planets[10].yv = -13100#-w

        self.planets.append(Planet(R * math.cos(theta), R * math.sin(theta), 4, 1e25, 'L5', (255, 255, 0), False))
        self.planets[11].yv = -13100
# 
        # self.planets.append(Planet(1.48104e11, 0, 9, 1898e24, 'L1', (255, 255, 0), False))
        # self.planets[6].yv = -12100
# 
        # self.planets.append(Planet(1.510924e11, 0, 9, 1898e24, 'L2', (255, 255, 0), False))
        # self.planets[7].yv = -14100
# 
        # self.planets.append(Planet(-5.2 * self.AU, 0, 9, 1898e24, 'L3', (255, 255, 0), False))
        # self.planets[8].yv = 13100
        # distance_to_sun = 5.2 * self.AU * (1.9891e30 * 0.001) / ((1.9891e30 * 0.001) + 1.9891e30)
        # self.planets.append(Planet(distance_to_sun, distance_to_sun, 9, 1898e24, 'L4', (255, 255, 0), False))
        # self.planets[9].yv = -2 * math.pi / (5.2 * self.AU)
# 
        # self.planets.append(Planet(distance_to_sun, -distance_to_sun, 9, 1898e24, 'L5', (255, 255, 0), False))
        # self.planets[10].yv = -2 * math.pi / (5.2 * self.AU)
        # 


    def update_positions(self, pl):
        total_fx = 0
        total_fy = 0

        for iter_pl in self.planets: 
            if pl == iter_pl:
                continue

            fx, fy = pl.f_axes(iter_pl, self.G)
            if pl.name == 'L4' or pl.name == 'L5':
                pass
            else:
                total_fx += fx
                total_fy += fy


        pl.xv += total_fx / pl.m * self.day_time
        pl.yv += total_fy / pl.m * self.day_time
        
        pl.r_x += pl.xv * self.day_time
        pl.r_y += pl.yv * self.day_time
        pl.orbit.append((pl.r_x, pl.r_y))

    def modeling(self):
        self.status = True  
        clock = pygame.time.Clock()

        while self.status: 
            clock.tick(10000)
            WIN.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.status = False

            for iter_pl in self.planets: 
                self.update_positions(iter_pl)
                iter_pl.draw(WIN)
        
            pygame.display.update()

        pygame.quit()




syst = PlanetSys()

syst.modeling()
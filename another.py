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
        self.lagrange_points = list()
        self.status = False
        self.G = 6.6743e-11
        # 149.6e6 * 1000
        self.AU = 1.496e11
        self.days = 365
        self.day_time =  24 * 60 * 60

        self.planets.append(Planet(0, 0, 13, 1.9891e30, 'Sun', (255, 255, 0), True))
        
        self.planets.append(Planet(.39 * self.AU, 0, 2, 0.33e24, 'Mercury', (0, 204, 204), False))
        self.planets[1].yv = -47400
        
        self.planets.append(Planet(.72 * self.AU, 0, 3, 4.87e24, 'Venus', (102, 102, 255), False))
        self.planets[2].yv = -35000
        
        self.planets.append(Planet(1 * self.AU, 0, 5, 5.97e24, 'Earth', (51, 153, 255), False))
        self.planets[3].yv = -29800
        
        self.planets.append(Planet(1.52 * self.AU, 0, 4, 0.642e24, 'Mars', (153, 76, 0), False))
        self.planets[4].yv = -24100
        
        self.planets.append(Planet(5.2 * self.AU, 0, 9, 1898e24, 'Jupiter', (102, 102, 0), False))
        self.planets[5].yv = -13100
        
        self.planets.append(Planet(9.54 * self.AU, 0, 8, 568e24, 'Saturn', (0, 76, 153), False))
        self.planets[6].yv = -9700
  
        self.planets.append(Planet(19.2 * self.AU, 0, 7, 86.8e24, 'Uranus', (102, 255, 178), False))
        self.planets[7].yv = -6800
 
        self.planets.append(Planet(30.06 * self.AU, 0, 6, 102e24, 'Neptune', (51, 153, 255), False))
        self.planets[8].yv = -5400


        self.planets.append(Planet(-5.2 * self.AU, 0, 4, 1898e24, 'L3', (102, 102, 0), False))
        self.planets[9].yv = 13100
        
        self.planets.append(Planet((5.2 - 0.363) * self.AU,  0, 4, 1e25, 'L1', (255, 255, 0), False))
        self.planets[10].yv = -13000   
        mass_sun = 1.9891e30
        mass_jupiter = 1898e24
        R = 5.2
        T = R**1.  
        rs = R * mass_jupiter / (mass_jupiter + mass_sun)
        rp = R * mass_sun / (mass_jupiter + mass_sun)
        w = 40000# (2 * math.pi / T) * 60 * 60 * 365 / 100 
        lx = rp-R/2
        ly= math.sqrt(3)*R / 2 
        self.planets.append(Planet(lx * self.AU, -ly * self.AU, 4, 1e25, 'L4', (102, 102, 0), False))
        self.planets[11].yv = -13100  
        self.planets.append(Planet(5.2 * self.AU / 2, 5.2 * self.AU * math.sqrt(3) / 2, 4, 1e25, 'L5', (102, 102, 0), False))
        self.planets[12].yv = -13100

        
        
        # self.lagrange_points.append(Planet(-5.2 * self.AU, 0, 4, 1898e24, 'L3', (255, 255, 0), False))
        # self.lagrange_points[0].yv = 13100
# 
        # self.lagrange_points.append(Planet(lx * self.AU, -ly * self.AU, 4, 1e25, 'L4', (255, 255, 0), False))
        # self.lagrange_points[1].yv = -13100
# 
        # self.lagrange_points.append(Planet(lx * self.AU, ly * self.AU, 4, 1e25, 'L5', (255, 255, 0), False))
        # self.lagrange_points[2].yv = 13000
        # for iter in self.lagrange_points:
            # print(iter.yv)
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
            if pl == iter_pl or iter_pl.name == 'L4' or iter_pl.name == 'L5':
                continue

            fx, fy = pl.f_axes(iter_pl, self.G)

            total_fx += fx
            total_fy += fy

        pl.xv += total_fx / pl.m * self.day_time
        pl.yv += total_fy / pl.m * self.day_time
                
        pl.r_x += pl.xv * self.day_time
        pl.r_y += pl.yv * self.day_time

        if pl.name == 'Jupiter':
            for iter_lagrange in self.planets:
                if iter_lagrange.name == 'L4': 
                    iter_lagrange.xv = pl.xv
                    iter_lagrange.yv = pl.yv
                    iter_lagrange.r_x = -(math.pi * 1 / 2 - pl.r_y)
                    iter_lagrange.r_y = math.pi * 1 / 2  - pl.r_x
                

                if iter_lagrange.name == 'L5': 
                    iter_lagrange.xv = pl.xv
                    iter_lagrange.yv = pl.yv
                    iter_lagrange.r_x = -pl.r_y + math.pi * 1 / 2
                    iter_lagrange.r_y = pl.r_x - math.pi * 1 / 2 
            
                # work L1
                # elif iter_lagrange.name == 'L5': 
                    # iter_lagrange.xv = pl.xv
                    # iter_lagrange.yv = pl.yv
                    # iter_lagrange.r_x = (math.sqrt(3) / 2) * pl.r_x
                    # iter_lagrange.r_y = (math.sqrt(3) / 2) * pl.r_y
                
                iter_lagrange.orbit.append((iter_lagrange.r_x, iter_lagrange.r_y))

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
                if iter_pl.name == 'L4' or iter_pl.name == 'L5':
                    pass
                else:
                    self.update_positions(iter_pl)
                
                iter_pl.draw(WIN)
                #if iter_pl.name == 'Jupiter':
                #    for iter_lagrange in self.lagrange_points:
                #        iter_lagrange.draw(WIN)
                
                
                
            pygame.display.update()

        pygame.quit()




syst = PlanetSys()

syst.modeling()
import pygame,  sys,  os,  Image
from pygame.locals import *


class OriCon():
    SCREENRECT = Rect(0,0,800,600)
    imagen_activa = 0
    redibujar = False
    imagen_pil = None
    contador = 0

    def mostrarSiguiente(self):
        if self.imagen_activa + 1 >= len(self.lista_imagenes):
            self.imagen_activa = 0
        else:
            self.imagen_activa+=1
            
        self.visor.mostrar("entrada/%s"%self.lista_imagenes[self.imagen_activa])
        self.imagen_pil = None


    def mostrarAnterior(self):
        if self.imagen_activa - 1 <= 0:
            self.imagen_activa = len(self.lista_imagenes) - 1
        else:
            self.imagen_activa -= 1
        
        self.visor.mostrar("entrada/%s"%self.lista_imagenes[self.imagen_activa])
        self.imagen_pil = None
    
    def exportarImagen(self):
        #calcular la imagen para exportar por pil
        #si no esta, carga la imagen con pil
        if not self.imagen_pil:
            self.imagen_pil = Image.open("entrada/%s"%self.lista_imagenes[self.imagen_activa])
        print self.imagen_pil
        print self.visor.escala
        print self.selector.posicion()[0]
        x_real = self.selector.posicion()[0] - self.visor.offset_x
        print x_real
        ancho_real = self.selector.tamano()[0] / self.visor.escala
        alto_real = self.selector.tamano()[1] / self.visor.escala
        offset_x_real = x_real / self.visor.escala
        offset_y_real = self.selector.posicion()[1] / self.visor.escala
        print self.selector.tamano()[0]
        print ancho_real
        print self.selector.tamano()[1]
        print alto_real
        print offset_x_real
        print offset_y_real
        caja = (int(offset_x_real),  int(offset_y_real),  int(ancho_real + offset_x_real),  int(alto_real + offset_y_real))
        print caja
        recorte = self.imagen_pil.crop(caja)
#        recorte = self.imagen_pil.crop((10, 10, 15, 15))
        recorte = recorte.resize((600, 800))
        recorte = recorte.convert("L")
        self.contador += 1
        recorte.save("salida/ori%s.jpg"%str(self.contador).zfill(3),  "JPEG")
    
    def __init__(self):
    #    creo la lista de imagenes
        self.lista_imagenes = os.listdir("entrada")
        self.lista_imagenes.sort()
            
        pygame.init()
        #ventana = pygame.display.set_mode(SCREENRECT.size,FULLSCREEN)
        #primero creo la ventana.
        self.ventana = pygame.display.set_mode(self.SCREENRECT.size)
        pygame.display.set_caption("OriCon")
        
#        fondo = pygame.Surface(self.SCREENRECT.size)
#        fondo =  fondo.convert()
#        fondo.fill((255, 0, 0))
#        self.ventana.blit(fondo, self.SCREENRECT)
        
        self.visor = Visor()
        self.visor.mostrar("entrada/%s"%self.lista_imagenes[self.imagen_activa])
        
        self.selector = Selector()
#        prueba = Prueba()
#        sprites = pygame.sprite.RenderPlain((selector))
        sprites = pygame.sprite.RenderUpdates((self.visor,  self.selector))
#        self.ventana.blit(r,(0, 0))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()     
                if event.type == pygame.KEYDOWN:
                    if event.key is pygame.K_SPACE:
                        self.mostrarSiguiente()
                    elif event.key == pygame.K_LEFT:
                        self.selector.achicar()
                    elif event.key == pygame.K_RIGHT:
                        self.selector.agrandar()
                    elif event.key is pygame.K_BACKSPACE:
                        self.mostrarAnterior()
                    elif event.key is pygame.K_RETURN:
                        self.exportarImagen()
            
            sprites.update()
            sprites.draw(self.ventana)
            
#            if self.redibujar:
            pygame.display.flip()



class Visor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ventana = pygame.display.get_surface()
        self.image = pygame.Surface(ventana.get_rect().size)
        self.rect = ventana.get_rect()
    
    def mostrar(self,  ruta_imagen):
        #trato de cargar la imagen
        try:
            imagen = pygame.image.load(ruta_imagen)
        except:
            imagen = None
            
        # escala y proceso
        if not imagen: 
            return
            
        imagen_rect = imagen.get_rect()
        ventana_rect = self.image.get_rect()
        escala = None
        
        factor_escala_x = float(ventana_rect[2]) / float(imagen_rect[2])
        print factor_escala_x 
        factor_escala_y = float(ventana_rect[3]) / float(imagen_rect[3])
        print factor_escala_y
        if factor_escala_x > 1 or factor_escala_y > 1:
            escala = min(factor_escala_x,  factor_escala_y)
        elif factor_escala_x < 1 or factor_escala_y <1:
            escala = min(factor_escala_x,  factor_escala_y)
            
        if escala:
            imagen = pygame.transform.scale(imagen,  (imagen_rect[2] * escala,  imagen_rect[3] * escala))
            imagen_rect = imagen.get_rect()
            
        print imagen
        
        #mostrarla
        if imagen:
            imagen.convert()
#                self.ventana.fill((255, 0, 0))
            offset_x = (ventana_rect[2] - imagen_rect[2]) / 2
            offset_y = (ventana_rect[3] - imagen_rect[3]) / 2
            self.image.blit(imagen, (offset_x, offset_y))
            self.escala = escala
            self.offset_x = offset_x
        
#        self.redibujar = True
        
class Selector(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(0, 0, 60, 80)
        self.image = pygame.Surface(self.rect.size, SRCALPHA)
        self.image.fill((255, 0, 0, 75))
        
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        
    def agrandar(self):
        self.rect.inflate_ip(6, 8)
        self.image = pygame.transform.scale(self.image,  self.rect.size)
    
    def achicar(self):
        self.rect.inflate_ip(-6, -8)
        self.image = pygame.transform.scale(self.image,  self.rect.size)
        
    def posicion(self):
        return self.rect.topleft
        
    def tamano(self):
        return self.rect.size
        
if __name__ == "__main__":
    OriCon()

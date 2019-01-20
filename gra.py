#gra szalona wiewiórka
from livewires import games, color
import random
#moduł games z pakietu livewires zapewnia wiele możliwości

#inicjalizujemy ekran graficzny (screen jest obiektem modułu ganmes)
games.init(screen_width = 900, screen_height = 500, fps = 50)

wall_image=games.load_image("las1.jpg", transparent= False)
games.screen.background = wall_image

#stworzenie klasy obiektu kopsz
class Kosz(games.Sprite):
    
    image = games.load_image("kosz.bmp")

#inicjalizacja obiektu
    "nadanie duszkowi obrazu, uzaleznienie sterowanie od myszki (tylko w osi poziomej)"
    def __init__(self):
        super(Kosz, self).__init__(image = Kosz.image,
                                  x = games.mouse.x,

                                  bottom = games.screen.height)
#tekst z punktacja
        self.punkty = games.Text(value = 0,
                                size = 40,
                                color = color.yellow,
                                top = 20,
                                 right = games.screen.width - 30)
        
        games.screen.add(self.punkty)
                                
        
    def update(self):
        "funkcja powiazuje ruch obiektu w osi x z ruchem myszy (w osi x)"
        self.x = games.mouse.x

        #gdy mysz wyjedzie poza lewą krawędź okna, ustaw kosz przy lewej krawędzi
        if self.left < 0:
            self.left = 0

        #analogicznie dla prawej krawędzi
        if self.right > games.screen.width:
            self.right = games.screen.width

        self.czy_zlapany()

#sprawdzenie czy zostanie złapany orzech
        "funkcja sprawdzajaca czy duszki na siebie wpadly, jesli tak odwoluje do kolejnej funkcji oraz zwieksza il zdobytych punktow o 10"
    def czy_zlapany(self):
        for orzech in self.overlapping_sprites:
            self.punkty.value += 10
            self.punkty.right = games.screen.width - 30
            orzech.zlapany()
        

#tworzenie klasy orzecha
class Orzech(games.Sprite):
    
    image = games.load_image("orzech.bmp")
    speed = 2 

#inicjalizacja klasy
    def __init__(self, x, y = 140):
        "funkcja nadaje obiektowi obraz, predkosc, polozenie"
    
        super(Orzech, self).__init__(image = Orzech.image,
                                    x = x, y = y,
                                    dy = Orzech.speed)
        
    def update(self):
        "funkcja sprawdza czy obiekt dotknął brzegu ekranu, jesli tak usuwa go i wywołuje funkcje koniec"
        if self.bottom > games.screen.height:
            self.koniec()
            self.destroy()

#usunięcie orzecha gdy zostanie złapany
        "funkcja usuwa duszka po złapaniu i zwiększa prędkoścnastepnego o 0,1"
    def zlapany(self):
        self.destroy()
        Orzech.speed = Orzech.speed + 0.1
    
        if Orzech.speed > 7:
            Orzech.speed = Orzech.speed - 0.1
 
#komunikat i koniec gry
    def koniec(self):
        "funkcja wyswietla napis koncowy, po którym usuwane sa duszki i okno się czyści"
        
        napis_koncowy = games.Message(value = "Koniec",
                                    size = 80,
                                    color = color.yellow,
                                    x = games.screen.width/2,
                                    y = games.screen.height/3,
                                    lifetime = 500,
                                    after_death = games.screen.clear)
        
        games.screen.add(napis_koncowy)


class Wiew(games.Sprite):
    "utworzenie klasy wiewiórki"
    
    image = games.load_image("squirl.bmp")
    speed = 4
    

#inicjalizacja klasy
    "nadanieobrazu, predkosci, polozenia"
    def __init__(self, y = 55, odds_change = 200):
        super(Wiew, self).__init__(image = Wiew.image,
                                   x = games.screen.width / 2,
                                   y = games.screen.height /3,
                                   dx = Wiew.speed)
        
        self.odds_change = odds_change
        self.leci = 0

    def update(self):
        "funkcja ktora zmienia zwrot wektora predkosci gdy wyjedzie on poza granice okna"
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
           self.dx = -self.dx
                
        self.zrzuc()


    def zrzuc(self):
        "funkcja wyswietla nowy obiekt na ekranie po okreslonym czasie"
        if self.leci > 0:
            self.leci -= 1
        else:
            nowy_orzech = Orzech(x = self.x)
            games.screen.add(nowy_orzech)
   
            self.leci = int(nowy_orzech.height*5/Orzech.speed)  

           

#wyświetlające się komunikaty
            "funkcja dodaje do ekranu napisy poczatkowe, znajduja sie one w nowej petli przez co by program dalej si ewykonal trzeba zamknąc okno"
def Message():
    message = games.Message( value = "Naciśnij 'X' aby rozpocząć",
                      size = 40,
                      color = color.white,
                      x = games.screen.width/2,
                      y = games.screen.height/2,
                      lifetime = 200,
                      after_death = None )
    
    hello = games.Message( value = "Witaj w grze Szalona Wiewiórka",
                       size = 50,
                       color = color.white,
                       x = games.screen.width/2,
                       y = games.screen.height/3,
                       lifetime = 200,
                       after_death= None)


    
    games.screen.add(hello)
    
    games.screen.add(message)

    games.screen.mainloop()

    
    
def main():
    "funckja głowna, dodaje obikty do ekranu, wywołuje wczesniejsze funkcje, wyswietla komunikat w kolejnej petli"
    

    wiewiorka = Wiew()
    games.screen.add(wiewiorka)


    #wyświetlamy obiekt na ekranie
    koszyk = Kosz()
    
    games.screen.add(koszyk)

    games.mouse.is_visible = False

    
    games.screen.mainloop()
  
Message()
main()


import pygame
from random import randint
import time
import sys

#waktu
clock=pygame.time.Clock()

pygame.init()

#ukuran window
width = 690
height = 695

#definisi icon, caption, mode
#icon = pygame.image.load("(ex gambar1.jpg)")
window = pygame.display.set_mode((width, height),pygame.RESIZABLE)
#pygame.display.set_caption("(ex Halo)")
#pygame.display.set_icon((ex icon))
pygame.display.update()

#definisi warna
hitam = (0,0,0)
biru = (0,0,255)
kuning = (255,255,0)

#Gambar papan dan dadu
papan = pygame.image.load("papan_permainan.png")

#Dadu
dadu1 = pygame.image.load("dadu1.png")
dadu2 = pygame.image.load("dadu2.png")
dadu3 = pygame.image.load("dadu3.png")
dadu4 = pygame.image.load("dadu4.png")
dadu5 = pygame.image.load("dadu5.png")
dadu6 = pygame.image.load("dadu6.png")

#Gambar player 1, 2, 3, 4
player1 = pygame.image.load("player1.png")
player2 = pygame.image.load("player2.png")
player3 = pygame.image.load("player3.png")
player4 = pygame.image.load("player4.png")

#Background utama
background = pygame.image.load("backgroundutama.png")

#Status mouse(?)
mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed()

#Style Judul Permainan
def message_display(text, x, y, fs):
    largeText = pygame.font.SysFont('Calibri', 17)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x,y)
    window.blit(TextSurf,TextRect)

#Definisi text_objects
def text_objects(text,font):
    textSurface = font.render(text, True, hitam)
    return textSurface, textSurface.get_rect()

#Style message ststus
def message_status(text, x, y, fs, c):
    largeText=pygame.font.SysFont('Calibri', 17)
    TextSurf, TextRect = text_objects1(text, largeText)
    TextRect.center = (x,y)
    window.blit(TextSurf, TextRect)

#Definisi text_objects1
def text_objects1(text, font):
    textSurface = font.render(text, True, hitam)
    return textSurface, textSurface.get_rect()

#Peta kotak kecil di papan
def posisi_gambar(posisi):
    peta = [
    [1,405],[242,405],[287,405],[332,405],[377,405],[422,405],[467,405],[512,405],[557,405],[602,405],[647,405],
    [647,360],[602,360],[557,360],[512,360],[467,360],[422,360],[377,360],[332,360],[287,360],[242,360],
    [242,315],[287,315],[332,315],[377,315],[422,315],[467,315],[512,315],[557,315],[602,315],[647,315],
    [647,270],[602,270],[557,270],[512,270],[467,270],[422,270],[377,270],[332,270],[287,270],[242,270],
    [242,225],[287,225],[332,225],[377,225],[422,225],[467,225],[512,225],[557,225],[602,225],[647,225],
    [647,180],[602,180],[557,180],[512,180],[467,180],[422,180],[377,180],[332,180],[287,180],[242,180],
    [242,135],[287,135],[332,135],[377,135],[422,135],[467,135],[512,135],[557,135],[602,135],[647,135],
    [647,90],[602,90],[557,90],[512,90],[467,90],[422,90],[377,90],[332,90],[287,90],[242,90],
    [242,45],[287,45],[332,45],[377,45],[422,45],[467,45],[512,45],[557,45],[602,45],[647,45],
    [647,0],[602,0],[557,0],[512,0],[467,0],[422,0],[377,0],[332,0],[287,0],[242,0]
    ]

    #Posisi player tertentu
    posisi_sekarang = peta[posisi]
    x = posisi_sekarang[0]
    y = posisi_sekarang[1]
    
    return x,y

#Alur rope/tali(untuk naik ke atas)
def tali(x):
    if x == 5: return 39
    elif x == 34: return 69
    elif x == 59: return 78
    elif x == 73: return 96
    else: return x

#Alur jurang
def jurang(x):
    if x == 57: return 49
    elif x == 83: return 66
    elif x == 42: return 36
    elif x == 32: return 13
    else: return x

#Memunculkan dadu sesuai angka
def dice(a):
    if a == 1:
        a = dadu1
    elif a == 2:
        a = dadu2
    elif a == 3:
        a = dadu3
    elif a == 4:
        a = dadu4
    elif a == 5:
        a = dadu5
    elif a == 6:
        a = dadu6

    time = pygame.time.get_ticks()
    while pygame.time.get_ticks()-time<1000:
        window.blit(a,(120, 300))
        pygame.display.update()

def button_mengocokdadu(text, xmouse, ymouse, x, y, w, h, i, a, fs):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w>xmouse>x and y+h>ymouse>y:
        pygame.draw.rect(window, a, [x-2.5, y-2.5, w+5, h+5])
        if pygame.mouse.get_pressed()==(1,0,0):
            return True
    
    else: 
        pygame.draw.rect(window, i, [x, y, w, h])
    message_display(text,(x+w+x)/2, (y+h+y)/2,fs)

def turn(posisi, status_tali, status_jurang):
    #Mengacak angka dadu
    a = randint(1,6)

    #Memunculkan gambar dadu
    gambar_dadu = dice(a)
    #Menyimpan dimana posisi player
    posisi+=a

    #Jika belum mencapai puncak/finisih (100)
    if posisi<=100:
        #tali(posisi) dapat menghasilkan posisi setelah menemukan tali atau posisi sekarang
        tali2 = tali(posisi)
        #Jika tali2 tidak sama dengan posisi player
        if tali2 != posisi:
            status_tali=True
            time=pygame.time.get_ticks()
            #posisi sekarang berada di status ladder terakhir
            posisi=tali2

        jurang2 = jurang(posisi)

        if jurang2 != posisi:
            status_jurang = True
            posisi = jurang2
    else:
        #Kasus ketika mendekati finish jumlah dadu dijumlahkan dengan posisi sekarang tidak sama dengan 100 
        #kembali ke posisi awal
        posisi-=a

        time=pygame.time.get_ticks()
        while pygame.time.get_ticks()-time<1500:
            message_status("Tidak bisa mencapai Finish!", 50, 70, 35, hitam)
            pygame.display.update()
    return posisi , status_tali, status_jurang

#Definisi untuk keluar permainan
def Quit():
    pygame.quit()
    quit()

#Mulai bermain
def play(jumlah_pemain):
    time= 0

    #Memunculkan background dan papan
    window.blit(background, (0,0))
    #window.blit(papan, (240, 0))

    #Posisi awal player
    x_posisiawal = 175
    y_posisiawal = 410

    #Posisi awal player 1
    window.blit(player1, (x_posisiawal, y_posisiawal))
    
    if jumlah_pemain==2: 
        window.blit(player2, (115, 410))

    elif jumlah_pemain==3:
        window.blit(player2, (115, 410))
        window.blit(player3, (55, 410))

    elif jumlah_pemain==4:
        window.blit(player2, (115, 410))
        window.blit(player3, (55, 410))
        window.blit(player4, (35, 410))
    else:
        window.blit(player1, (x_posisiawal, y_posisiawal))

    #Awal bermain   
    p1="Player 1"
    posisi_p1=0

    if 5>jumlah_pemain>1:
        p2="Player 2"
        posisi_p2=0
    if 5>jumlah_pemain>2:
        p3="Player 3"
        posisi_p3=0
    if 5>jumlah_pemain>3:
        p4="Player 4"
        posisi_p4=0

    turn_ke=1

    x_player1 = 175
    x_player2 = 115
    x_player3 = 55
    x_player4 = 15
    y_player1 = 410
    y_player2 = 410
    y_player3 = 410
    y_player4 = 410

    mulai_bermain = True
    while mulai_bermain:
        status_tali = False
        status_jurang = False
        
        
        time=3000

        #Menampilkan background
        window.blit(background, (0,0))
        window.blit(papan, (240,0))

        #Mouse
        mouse=pygame.mouse.get_pos()

        #Untuk keluar
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                Quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    Quit()

        #Jika player hanya dua
        if 5>jumlah_pemain>1:   
                
            if button_mengocokdadu("Player 1", mouse[0], mouse[1], 100, 550, 200, 50, kuning, biru, 30):
                if turn_ke==1:
                    posisi_p1, status_tali, status_jurang = turn(posisi_p1,status_tali,status_jurang)
                    
                    
                    x_player1, y_player1 = posisi_gambar(posisi_p1)
                    
                    turn_ke+=1
                    
                    #Jika posisi sudah 100
                    if posisi_p1==100:
                        time=pygame.time.get_ticks()
                        while pygame.time.get_ticks()-time<2000:
                            message_status("Player 1 Menang", 120,60,35,hitam)
                            pygame.display.update()
                        break

            window.blit(player1, (x_player1, y_player1))

            if button_mengocokdadu("Player 2", mouse[0],mouse[1],400,550,200,50,kuning,biru,30):
                if turn_ke==2:
                    posisi_p2,status_tali,status_jurang=turn(posisi_p2,status_tali,status_jurang)
                    
                    x_player2, y_player2 = posisi_gambar(posisi_p2)
                    turn_ke+=1
                    if jumlah_pemain<3:
                        turn_ke=1

                    if posisi_p2==100:
                        time=pygame.time.get_ticks()
                        while pygame.time.get_ticks()-time<2000:
                            message_status("Player 2 Menang", 120,60,35,hitam)
                            pygame.display.update()
                        break

            window.blit(player2, (x_player2, y_player2))
        
        #Jika player hanya 3
        if 5>jumlah_pemain>2:
            if button_mengocokdadu("Player 3",mouse[0],mouse[1],100,610,200,50,kuning,biru,30):
                if turn_ke==3:
                    posisi_p3,status_tali,status_jurang = turn(posisi_p3, status_tali,status_jurang)
                    
                    x_player3, y_player3 = posisi_gambar(posisi_p3)
                    turn_ke+=1
                    if jumlah_pemain<4:
                        turn_ke=1

                    if posisi_p3==100:
                        time=pygame.time.get_ticks()
                        while pygame.time.get_ticks()-time<2000:
                            message_status("Player 3 Menang",120,60,35,hitam)
                            pygame.display.update()
                        break

            window.blit(player3, (x_player3, y_player3))

        #Jika pemain hanya empat
        if 5>jumlah_pemain>3:
            if button_mengocokdadu("Player 4", mouse[0],mouse[1],400,610,200,50,kuning,biru,30):
                if turn_ke==4:
                    posisi_p4,status_tali,status_jurang = turn(posisi_p4,status_tali,status_jurang)
                    
                    x_player4, y_player4 = posisi_gambar(posisi_p4)
                    turn_ke+=1
                    if jumlah_pemain<5:
                        turn_ke=1

                    if posisi_p4==100:
                        time=pygame.time.get_ticks()
                        while pygame.time.get_ticks()-time<2000:
                            message_status("Player 4 Menang", 120,60,35,hitam)
                            pygame.display.update()
                        break

            window.blit(player4, (x_player4, y_player4))

        if status_tali:
            time=pygame.time.get_ticks()
            while pygame.time.get_ticks()-time<2000:
                message_status("Selamat anda berada", 129,60,35,hitam)
                message_status("di daerah Tali !", 120, 90, 35, hitam)
                message_status("Anda akan naik",120,120,40,hitam)
                pygame.display.update()

        if status_jurang:
            time=pygame.time.get_ticks()
            while pygame.time.get_ticks()-time<2000:
                message_status("Sayang sekali, anda", 120,60,35,hitam)
                message_status("berada di jurang!", 120, 90, 35, hitam)
                message_status("Anda akan turun", 120,120,40, hitam)
                pygame.display.update()

        clock.tick(7)
        pygame.display.update()

total_pemain = sys.argv[1]
total_pemain = int(total_pemain)
play(total_pemain)

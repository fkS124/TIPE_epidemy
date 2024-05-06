import matplotlib.pyplot as plt
import numpy as np 
import time
import cv2 as cv

h, w = 0, 0

# ------------- Traitement d'image -----------------

def diminution_resolution2(img, coeff):
    """
    Diminue la résolution d'une image
    """
    img = img.copy()
    new_img = []
    w, h = img.shape[0:2]

    for x in range(0, w, coeff):
        new_line = []
        for y in range(0, h, coeff):
            new_line.append(img[x, y, :])
        new_img.append(new_line)
        
    return np.array(new_img)

# ------------------ Détection de blanc

def detect_white_line(img):
    # Détection grossière de points blancs
    img = img.copy()
    w, h = img.shape[0:2]
    red = [0.6, 0.4, 0.4]
    first_red = w//2
    greenPoints = []
    for y in range(h):
        for x in range(first_red, w):
            if h // 3 < y < 2 * h // 3:
                continue
            if (
                img[x, y, 0] > red[0] and
                img[x, y, 1] > red[1] and
                img[x, y, 2] > red[2] 
                ):
                img[x, y, :] = [0, 1, 0]
                greenPoints.append((y, x))

    return img, greenPoints


def clearGreenPoints(img, greenPoints, n=1):
    # Fonction de nettoyage de défauts de detect_white_line 
    # (INUTILISÉ)
    newGreenPoints = []
    for x, y in greenPoints:
        found = False
        for i in range(-n, n+1):
            for j in range(-n, n+1):
                try:
                    if tuple(img[y + i, x + j, :]) == (0, 1, 0) and (i, j) != (0, 0):
                        found = True
                except IndexError:
                    pass
        if found:
            newGreenPoints.append((x, y))
    
    for x, y in greenPoints:
        if (x, y) in newGreenPoints:
            img[y, x, :] = [1, 1, 1]
    print(len(greenPoints), len(newGreenPoints))
    return newGreenPoints


# ------------- Densité --------------

def graduate_density(img, greenPoints, r=4):
    # Affiche la densité de chaque points
    densities = [[density(img, x, y, r), (x, y)] for x, y in greenPoints]
    i = 0
    maxd = max(densities, key=lambda x: x[0])[0]
    for x, y in greenPoints:
        d = densities[i]
        img[y, x, :] = [0, d[0]/maxd, 0]
        i += 1
    return img, sorted(densities, key=lambda x: x[0], reverse=True)


def density(img, x, y, radius):
    # Calcule la densité d'un point
    count = 0
    n_green = 0
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            try:
                if tuple(img[y + i, x + j, :]) == (0, 1, 0) and (i, j) != (0, 0):
                    n_green += 1
                count += 1
            except IndexError:
                pass
    return n_green/count


# ------------- Modélisation --------------------

def modelisation(densities, N_dense = 20):
    # Regressions linéaires sur N_dense points pour modéliser les lignes
    rightX, rightY = [], []
    leftX, leftY = [], []
    
    i = 0
    # 20 points les plus denses de chaque côté
    while len(rightX) < N_dense or len(leftX) < N_dense:
        i += 1
        x, y = densities[i][1]
        if x > w // 2 and len(rightX) < N_dense:
            rightX.append(x)
            rightY.append(y)
        elif len(leftX) < N_dense:
            leftX.append(x)
            leftY.append(y)

    print(len(leftX), len(rightX))
    rightA, rightB = np.polyfit(rightX, rightY, deg=1)
    leftA, leftB = np.polyfit(leftX, leftY, deg=1)
    
    return (rightA, rightB, leftA, leftB)


def read_video(filename):
    cap = cv.VideoCapture(filename)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            continue
        # Our operations on the frame come here
        global h, w
        h, w = frame.shape[0:2]
        frame, greenPoints = detect_white_line(frame)
        frame, densities = graduate_density(frame, greenPoints, r=1)
        for density in densities:
            if not np.isfinite(density[0]):
                print("!!!!")
        rA, rB, lA, lB = modelisation(densities)

        cv.line(frame, (0, h), (w//2, lA*w//2+lB), (0, 255, 0), 5)
        cv.line(frame, (w, h), (w//2, rA*w//2+rB), (0, 255, 0), 5)

        # Display the resulting frame
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()



if __name__ == "__main__":
    # ----------- Test -----------
    read_video("resources/video_piste.mp4")

    # ---------- Image -----------
    # Récupération image et diminution résolution (on considèrera que
    # la caméra transmet les images déjà à la bonne résolution)
    img = plt.imread("resources/IMG_piste.png")
    img = diminution_resolution2(img, 15)
    h, w = img.shape[0:2]

    # -------- Début des calculs qui seront effectués en temps réel
    debut = time.time()

    img, greenPoints = detect_white_line(img)
    img, densities = graduate_density(img, greenPoints, r=1)
    rA, rB, lA, lB = modelisation(densities)

    fin = time.time()
    print(fin-debut)

    # ----------- Affichage des résultats (temps de calcul non pris en compte)
    tl = np.linspace(0, w//2, 10)
    tr = np.linspace(w//2, w, 10)

    plt.plot(tr, rA*tr+rB, color="red")
    plt.plot(tl, lA*tl+lB, color="blue")
    plt.imshow(img)
    plt.show()
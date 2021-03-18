import cv2
import numpy as np
import matplotlib.pyplot as plt

#[[User specified parameters]]

# ------- color condition ----------
R_low = 0
R_high = 100
G_low = 0
G_high = 100
B_low = 100
B_high = 300
# -----------------------------------

# ------- scale condition -----------
Area_th_min = 1200
Area_th_max = 10000
# -----------------------------------


# Step 1 ---------------------------
image_dir = './assets/'
filename = "IMG_2747.png"
input_img = image_dir + filename
img = cv2.imread(input_img)
img_c_origin = cv2.imread(input_img)
height = img.shape[0]
width = img.shape[1]
img_c = cv2.resize(img , (int(width*0.5), int(height*0.5)))
for i in range(2):
    img_c = cv2.GaussianBlur(img_c,(5,5),0)

B, G, R = cv2.split(img_c)

img_g_th = np.where((G < G_high) & (G > G_low), 1, 0)
img_b_th = np.where((B < B_high) & (B > B_low), 1, 0)
img_r_th = np.where((R < R_high) & (R > R_low), 1, 0)

img_th = img_r_th * img_g_th * img_b_th * 255
img_th = np.uint8(img_th)

# Step 2 ---------------------------
contours = cv2.findContours(img_th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

# Step 3 ---------------------------
Active_contours = []

for cont in contours:
    if cv2.contourArea(cont) > Area_th_min and cv2.contourArea(cont) < Area_th_max:
        Active_contours.append(cont)

# Step 4 ---------------------------
cont_img = cv2.drawContours(img_c_origin, Active_contours, -1, (255,0,0), 3)

cont_img = cv2.cvtColor(cont_img, cv2.COLOR_BGR2RGB)
img_c_origin = cv2.cvtColor(img_c_origin, cv2.COLOR_BGR2RGB)

# ------------- show images ------------- 
plt.gray()

plt.subplot(1,2,1)
plt.imshow(img_th, vmin=0, vmax=255, interpolation = 'none')
cv2.imwrite('./output/blue_output.png', img_th)
plt.title('Threshold')

plt.subplot(1,2,2)
plt.imshow(cont_img, interpolation = 'none')
plt.title('Contour')

plt.show()
# ----------------------------------------
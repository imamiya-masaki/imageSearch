# coding: UTF-8
image_dir = './assets/'
image_file = 'graph.png'

output_dir = "./output/"
output_file = "graph_output2.png"
def drawEllipseWithBox(img_ary, box, color, enbNumber=True, lineThickness=1):
    for i, img in enumerate(img_ary):
        cv2.ellipse(img, box, color, lineThickness, cv2.LINE_AA)

        # 中心位置をマーク
        cx = int(box[0][0])
        cy = int(box[0][1])
        cv2.drawMarker(img, (cx,cy), color, markerType=cv2.MARKER_CROSS, markerSize=20, thickness=5)

        # 外角矩形描画
        vtx = np.int0(cv2.boxPoints(box))
        for j in range(0, 4):
            cv2.line(img, (vtx[j,0],vtx[j,1]), (vtx[(j+1)%4, 0],vtx[(j+1)%4, 1]), color, lineThickness, lineType=cv2.LINE_AA)
        if i == 0 :
            if enbNumber:
                cv2.putText(img, str(i+1), (cx+3,cy+3), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 1,cv2.LINE_AA)
        else:
            cv2.putText(img, str(i+1), (cx+3,cy+3), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 1,cv2.LINE_AA)

import cv2
import numpy as np

ksize = 3 #中央値フィルタ
neiborhood = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8)
fileName = image_dir + image_file
img = cv2.imread(fileName,1)

#print (img)
#cv2.imshow('image',img)
#cv2.waitKey(0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imwrite(fileName,gray)

img = cv2.imread(fileName,0)
threshold = 64 #閾値

ret, img_thresh = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY)
img_thresh = cv2.bitwise_not(img_thresh)

#ノイズ除去
img_thresh = cv2.erode(img_thresh,neiborhood,iterations=4) #縮小サイズ指定
img_thresh = cv2.dilate(img_thresh,neiborhood,iterations=8) #拡大サイズ指定
img_thresh = cv2.medianBlur(img_thresh,ksize) #中央値フィルタ

#細線化
# skeleton1 = cv2.ximgproc.thinning(img_thresh,thinningType = cv2.ximgproc.THINNING_ZHANGSUEN)
# skeleton2 = cv2.ximgproc.thinning(img_thresh,thinningType = cv2.ximgproc.THINNING_GUOHALL)

resimg = img_thresh // 2 + 128
result_nor = [resimg, resimg.copy()]
result_ams = [resimg, resimg.copy()]
result_dir = [resimg, resimg.copy()]

contours, _ =  cv2.findContours(img_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for i, cnt in enumerate(contours):
    alen = cv2.arcLength(cnt,True)

    # 楕円フィッティング
    ebox = cv2.fitEllipse(cnt)
    drawEllipseWithBox(result_nor, ebox, (255,0,0), True)

    # 楕円フィッティングAMS
    eboxAMS = cv2.fitEllipseAMS(cnt)
    drawEllipseWithBox(result_ams, eboxAMS, (0,0,255), False)
    print(eboxAMS)

    # 楕円フィッティングDirect
    eboxDirect = cv2.fitEllipseDirect(cnt)
    drawEllipseWithBox(result_dir, eboxDirect, (0,128,0), False)
    print(eboxDirect)

# 画像表示
cv2.imshow('Result',resimg)
cv2.imshow('Result fitEllipse',result_nor[1])
cv2.imshow('Result fitEllipseAMS',result_ams[1])
cv2.imshow('Result fitEllipseDirect',result_dir[1])
cv2.waitKey()
#cv2.imwrite(output_dir + output_file, img_thresh)
# cv2.imwrite("skeleton1.png",skeleton1)
# cv2.imwrite("skeleton2.png",skeleton2)
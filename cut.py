import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

"""
通过四个坐标点在任意位置切割图片，主要用于将大图片分割成多个小图片
img_path：需要切割图片的路径
"""


def cut_image():
    img = Image.open(img_path)
    w, h = img.size
    ###############################     这里需要定义角度   ########################################
    # 坐标点可以根据自己的需要进行调整，这里是个数   （X左上起始,Y左上起始, 宽,高）
    cut = [(0, 0, 120, h), (120, 0, 240, h), (240, 0, 360, h), (360, 0, w, h)]
    for i, n in enumerate(cut, 1):
        temp = img.crop(n)
        # 分别保存多个小图片，路径可以根据自己的需要设计
        temp.save(img_path.replace(".jpg", str(i - 1) + '.jpg'))
    return True


"""
扇形切割：按份数平均分割
"""


def cut_in_sectorial():
    img_color = cv2.imread(img_path, 1)
    height = img_color.shape[0]
    width = img_color.shape[1]
    Cx = int(width / 2)
    Cy = int(height / 2)
    radius = int(np.sqrt(Cx ** 2 + Cy ** 2))
    num = int(input("How many pieces? "))  # 均匀分成num份
    angle = 360 / num  # 每一份的角度
    for i in range(num):
        mask = np.zeros(img_color.shape[:2], np.uint8)
        cv2.ellipse(mask, (Cx, Cy), (radius, radius), 0, angle * i, angle * (i + 1), (255, 255, 255),
                    -1)  # 在模板图上画椭圆填充，填充的白色点位亮度提取区域

        masked_image = cv2.bitwise_and(img_color.copy(), cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR))

        cv2.imwrite(img_path.split('.')[0] + '_' + str(i + 1) + '.' + img_path.split('.')[1], masked_image)

        fig = plt.figure(figsize=(12, 5))
        ax1 = fig.add_subplot(1, 2, 1)
        plt.title('img_ellipse_color')
        plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))

        ax2 = fig.add_subplot(1, 2, 2)
        plt.title('mask')
        plt.imshow(mask, 'gray')

        
"""
扇形切割：用户自定义角度
"""


def cut_in_sectorial_self(angle_num):
    img_color = cv2.imread(img_path, 1)
    height = img_color.shape[0]
    width = img_color.shape[1]
    Cx = int(width / 2)
    Cy = int(height / 2)
    radius = int(np.sqrt(Cx ** 2 + Cy ** 2))


    for i in range(len(angle_num) - 1):
        img_ellipse_color = cv2.ellipse(img_color.copy(), (Cx, Cy), (radius, radius), 0, angle_num[i],
                                        angle_num[i + 1],
                                        (0, 255, 0), 3)  # 在彩图上画椭圆

        mask = np.zeros(img_color.shape[:2], np.uint8)
        cv2.ellipse(mask, (Cx, Cy), (radius, radius), 0, angle_num[i], angle_num[i + 1], (255, 255, 255),
                    -1)  # 在模板图上画椭圆填充，填充的白色点位亮度提取区域

        masked_image = cv2.bitwise_and(img_color.copy(), cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR))

        cv2.imwrite(img_path.split('.')[0] + '_' + str(i + 1) + '.' + img_path.split('.')[1], masked_image)


        fig = plt.figure(figsize=(12, 5))
        ax1 = fig.add_subplot(1, 2, 1)
        plt.title('img_ellipse_color')
        plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))

        ax2 = fig.add_subplot(1, 2, 2)
        plt.title('mask')
        plt.imshow(mask, 'gray')


"""
通过获取输入，进行水平和竖直的均匀切割
img_path：需要切割图片的路径
"""


def cut_average():
    img = Image.open(img_path)
    size = img.size
    cuts_h = int(input("Cuts in height: "))
    cuts_w = int(input("Cuts in weight: "))
    print(size, cuts_h, cuts_w)

    # 切割后的小图的宽度和高度
    if (cuts_h * cuts_w) < 1:
        # 准备将图片切割成小图片
        cuts_h += 1
        cuts_w += 1
        print("0 cut means no change")

    weight = int(size[0] // cuts_w)
    height = int(size[1] // cuts_h)

    for j in range((cuts_h + 1)):
        for i in range((cuts_w + 1)):
            box = (weight * i, height * j, weight * (i + 1), height * (j + 1))
            region = img.crop(box)
            region.save('output_{}{}.png'.format(j, i))


"""
通过坐标xy的最大最小值对图片进行整体切割
path1：需要切割图片的路径
path2：切割后保存图片的位置
x_min：切割矩形左边x值对应原图的x坐标
x_max：切割矩形右边x值对应原图的x坐标
y_min：切割矩形上边y值对应原图的y坐标
y_max：切割矩形下边y值对应原图的y坐标
"""


def cut_img_by_xy(x_min, x_max, y_min, y_max):
    img = Image.open(img_path)
    crop = img.crop((x_min, y_min, x_max, y_max))
    crop.save("result.jpg")


if '__main__' == __name__:
    img_path = input("Input a path： ")
    choice = int(input("Method: "))
    # 转换通道
    img = Image.open(img_path)
    img = img.convert("RGB")
    img.save(img_path)

    # 坐标切割
    if choice == 1:
        cut_image()
    # 扇形份数切割
    elif choice == 2:
        cut_in_sectorial()
    # 扇形自由切割
    elif choice == 3:
        cut_in_sectorial_self((0, 50, 80, 100, 156, 240, 320, 360))
    # 平均切割
    elif choice == 4:
        cut_average()
    # 整体切割
    elif choice == 5:
        cut_img_by_xy(120, 240, 60, 180)
    else:
        print("Please type method 1 or 2 or 3 or 4 or 5")


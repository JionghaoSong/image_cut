from PIL import Image
#输出到源文件夹

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
通过四个坐标点在任意位置切割图片，主要用于将大图片分割成多个小图片
img_path：需要切割图片的路径
"""


def cut_image(path):
    img = Image.open(path)
    w, h = img.size
    # 坐标点可以根据自己的需要进行调整，这里是个数   （X左上起始,Y左上起始, 宽,高）
    cut = [(0, 0, 120, h), (120, 0, 240, h), (240, 0, 360, h), (360, 0, w, h)]
    for i, n in enumerate(cut, 1):
        temp = img.crop(n)
        # 分别保存多个小图片，路径可以根据自己的需要设计
        temp.save(path.replace(".jpg", str(i - 1) + '.jpg'))
    return True


"""
通过坐标xy的最大最小值对图片进行整体切割
path1：需要切割图片的路径
path2：切割后保存图片的位置
x_min：切割矩形左边x值对应原图的x坐标
x_max：切割矩形右边x值对应原图的x坐标
y_min：切割矩形上边y值对应原图的y坐标
y_max：切割矩形下边y值对应原图的y坐标
"""


def cut_img_by_xy(path1, x_min, x_max, y_min, y_max, path2):
    img = Image.open(path1)
    crop = img.crop((x_min, y_min, x_max, y_max))
    crop.save(path2)


if __name__ == '__main__':
    img_path = input("Input a path： ")
    choice = int(input("Method: "))
    # 转换通道
    img = Image.open(img_path)
    img = img.convert("RGB")
    img.save(img_path)

    if choice == 1:
        # 平均切割
        cut_average()
    elif choice == 2:
        # 坐标切割
        cut_image(img_path)
    elif choice == 3:
        # 整体切割
        cut_img_by_xy(img_path, 120, 240, 60, 180, "2.jpg")
    else:
        print("Please type method 1 or 2 or 3")

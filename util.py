from PIL import Image, ImageDraw, ImageFont
import json

class Camera:
    def __init__(self, size):
        self.images = []
        self.camera_order = []
        self.associations = []
        self.window_size = size
        self.circle_radius = size[1] // 60
        self.text_size = size[1] // 70
        self.rows = 0
        self.cols = 0
        self.plain = Image.new(mode="RGB", size = self.window_size)
        self.background = self.plain.copy()
        self.added = []
        with open("camera.config") as file:
            self.camera_order = json.load(file)["camera_order"]
        self.rows = len(self.camera_order)
        for r in self.camera_order:
            if len(self.camera_order) > self.cols:
                self.cols = len(self.camera_order)
        self.image_size = size[0] // self.cols, size[1] // self.rows
        self.ratios = []
        for r in range(self.rows):
            rr = []
            for c in range(self.cols):
                rr.append((0, 0))
            self.ratios.append(rr)

        with open("associations.config") as file:
            self.associations = json.load(file)

    def draw_all(self):
        self.background = self.plain.copy()
        for c, ca in enumerate(self.associations):
            for a in ca:
                self.draw(c, a)

    def load_image(self, c, image_file):
        self.get_base(c)
        im = Image.open(image_file)
        self.images.append(im)
        ratio = (im.size[0] / self.image_size[0], im.size[1] / self.image_size[1])
        self.set_ratio(c, ratio)
        resized = im.resize(self.image_size, Image.ANTIALIAS)
        bx, by = self.get_base(c)
        self.plain.paste(resized, (bx, by))

    def circle(img, xy, r, color):
        image_draw = ImageDraw.Draw(img)
        ax, ay = xy
        square = (ax-r, ay-r, ax+r, ay+r)
        image_draw.ellipse(square, fill=color, outline=color)
        return image_draw

    def draw(self, c, a):
        if a["trust"]:
            color = "blue"
        else:
            color = "red"
        ax, ay = self.get_xy(c, a)
        image_draw = Camera.circle(self.background,(ax,ay),self.circle_radius, color)
        arial = ImageFont.truetype("arial.ttf", self.text_size)
        text = str(a["cell_coordinates"]["x"]) + "," + str(a["cell_coordinates"]["y"])
        w, h = arial.getsize(text)
        image_draw.text((ax - w // 2, ay - h // 2), text, (255, 255, 255), font=arial)

    def set_ratio (self, c, ratio):
        row, col = self.get_rc(c)
        self.ratios[row][col] = ratio

    def get_ratio(self,c):
        row, col = self.get_rc(c)
        return self.ratios[row][col]

    def get_rc(self, c):
        for row in range(2):
            for col in range(2):
                if c == self.camera_order[row][col]:
                    return row, col

    def get_base(self, c):
        row, col = self.get_rc(c)
        base = col * self.window_size[1] // self.cols, row * self.window_size[0] // self.cols
        return base

    def get_xy(self, c, a):
        x_base, y_base = self.get_base(c)
        wr, hr = self.get_ratio(c)
        return int(x_base + a["centroid"]["x"]/wr), int(y_base + a["centroid"]["y"]/hr)

    def get_cxy(self, pixel_xy):
        pixel_x, pixel_y = pixel_xy
        width, height = self.image_size
        col = int(pixel_x // width)
        row = int(pixel_y // height)
        c = self.camera_order[row][col]
        w_ratio, h_ratio = self.get_ratio(c)
        base_x, base_y = self.get_base(c)
        centroid_x = (pixel_x - base_x) * w_ratio
        centroid_y = (pixel_y - base_y) * h_ratio
        return c, centroid_x, centroid_y

    def association(self, centroid_xy, coordinates_xy, trust):
        centroid_x, centroid_y = centroid_xy
        coordinates_x, coordinates_y = coordinates_xy
        return {"centroid": {"x": centroid_x, "y": centroid_y}, "cell_coordinates": {"x": coordinates_x, "y": coordinates_y}, "trust": trust}

    def add_association(self, c, a):
        while self.exists(c, a["cell_coordinates"]):
            self.remove(c, a["cell_coordinates"])
        self.associations[c].append(a)
        self.added.append((c, a["cell_coordinates"]))

    def find(self, c, cc):
        for i, a in enumerate(self.associations[c]):
            if a["cell_coordinates"] == cc:
                return i
        return -1

    def remove(self, c, cc):
        i = self.find(c,cc)
        if i!=-1:
            self.associations[c] = self.associations[c][0:i]+self.associations[c][i+1:]

    def remove_last(self):
        if (len(self.added) == 0):
            return
        self.remove(self.added[-1])
        self.added = self.added[:-1]

    def exists(self, c, cc):
        return self.find(c,cc) != -1

    def save (self):
        with open("associations.config", "w") as file:
            json.dump(self.associations, file)

camera = Camera((800, 800))
camera.load_image(0, "camera_0.png")
camera.load_image(1, "camera_1.png")
camera.load_image(2, "camera_2.png")
camera.load_image(3, "camera_3.png")
camera.draw_all()
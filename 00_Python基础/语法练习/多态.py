class Animal:
    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        print("汪汪汪")


class Cat(Animal):
    def speak(self):
        print("喵喵喵")


def make_noise(animal: Animal):
    animal.speak()


# 演示多态，使用2个子类对象来调用函数
dog = Dog()
cat = Cat()

make_noise(dog)
make_noise(cat)


# 演示抽象类

class AC:
    def cool_wind(self):
        pass

    def hot_wind(self):
        pass

    def swing_l_r(self):
        pass


class Midea_AC(AC):
    def cool_wind(self):
        print("美的制冷")

    def hot_wind(self):
        print("美的制热")

    def swing_l_r(self):
        print("美的摆风")


class Geli_AC(AC):
    def cool_wind(self):
        print("格力制冷")

    def hot_wind(self):
        print("格力制热")

    def swing_l_r(self):
        print("格力摆风")


def make_cool(ac: AC):
    ac.cool_wind()


meide = Midea_AC()
geli = Geli_AC()

make_cool(meide)
make_cool(geli)

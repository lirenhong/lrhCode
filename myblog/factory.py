# coding:utf-8
from abc import ABCMeta, abstractmethod

# class Animal(object):
#     __metaclass__ = ABCMeta

#     @abstractmethod
#     def do_say(self):
#         pass

# class Dog(Animal):
#     def do_say(self):
#         print "Bhow Bhow!"

# class Cat(Animal):
#     def do_say(self):
#         print "Meow Meow!"

# class ForestFactory(object):
#     def make_sound(self, object_type):
#         return object_type().do_say()

# if __name__ == "__main__":
#     ff = ForestFactory()
#     ff.make_sound(Dog)

class Section(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def describe(self):
        pass

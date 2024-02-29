import os
import json


class Person:
    def __init__(self, firstname, lastname, age, gender, profile_pic_path, photo_folder_path):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.profile_pic_path = profile_pic_path
        self.photo_folder_path = photo_folder_path

    def verify(self):
        # Verify that the profile picture exists
        if not os.path.isfile(self.profile_pic_path):
            raise ValueError(f"Invalid profile picture path: {self.profile_pic_path}")

        # Verify that the photo folder exists and is a directory
        if not os.path.isdir(self.photo_folder_path):
            raise ValueError(f"Invalid photo folder path: {self.photo_folder_path}")

    def __str__(self):
        return (
            f"{self.firstname} {self.lastname} (age: {self.age}, gender: {self.gender},"
            f" profile picture: {self.profile_pic_path}, photo folder: {self.photo_folder_path})"
        )

    def display_info(self):
        print(self)
    def current_amount_of_photos(self):
        # check if the directory exists
        if os.path.isdir(self.photo_folder_path):
            return len(os.listdir(self.photo_folder_path))


if __name__ == "__main__":
    p = Person(
        firstname="John",
        lastname="Doe",
        age=30,
        gender="male",
        profile_pic_path="path/to/profile.jpg",
        photo_folder_path="path/to/photo/folder",
    )
    print(p)


def dict_to_person(d: dict) -> Person:
    return Person(
        firstname=d["firstname"],
        lastname=d["lastname"],
        age=d["age"],
        gender=d["gender"],
        profile_pic_path=d["profile_pic_path"],
        photo_folder_path=d["photo_folder_path"],
    )




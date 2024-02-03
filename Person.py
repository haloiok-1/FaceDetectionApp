import os


class Person:
    def __init__(self, name, lastname, age, gender, profile_pic_path, photo_folder_path):
        self.name = name
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.profile_pic_path = profile_pic_path
        self.photo_folder_path = photo_folder_path

        # Verify that the profile picture exists
        if not os.path.isfile(self.profile_pic_path):
            raise ValueError(f"Invalid profile picture path: {self.profile_pic_path}")

        # Verify that the photo folder exists and is a directory
        if not os.path.isdir(self.photo_folder_path):
            raise ValueError(f"Invalid photo folder path: {self.photo_folder_path}")

    def __str__(self):
        return (
            f"{self.name} {self.lastname} (age: {self.age}, gender: {self.gender},"
            f" profile picture: {self.profile_pic_path}, photo folder: {self.photo_folder_path})"
        )

    def display_info(self):
        print(self)


# Example usage
p = Person(
    name="John",
    lastname="Doe",
    age=30,
    gender="male",
    profile_pic_path="path/to/profile.jpg",
    photo_folder_path="path/to/photo/folder",
)
p.display_info()

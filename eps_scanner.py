from os import listdir
from os.path import isfile, join

# music_folder_path = "\\\\192.168.1.2\\Music\\Eps"
music_folder_path = "/music"


def scan():
    total_count = 0
    only_folders = [f for f in listdir(music_folder_path) if not isfile(join(music_folder_path, f))]
    for folder in only_folders:
        if not '__' in folder:
            sub_folder = [fi for fi in listdir(music_folder_path + '/' + folder) if
                          not isfile(join(music_folder_path + '/' + folder, fi))]
            print(folder + ', ' + str(len(sub_folder)))
            total_count = total_count + len(sub_folder)
    print('labels: ' + str(len(only_folders)))
    print('eps: ' + str(total_count))

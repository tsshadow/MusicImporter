import sys
from time import sleep

from processing.extractor import Extractor
from processing.mover import Mover
from processing.renamer import Renamer
from data.settings import Settings
# from data.database import Database
# from postprocessing.scanner import Scanner
from postprocessing.tagger import Tagger

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Run command with \'main.py docker\' or \'main.py windows\'')
    else:
        settings = Settings()
        settings.initialize(sys.argv[1])

        extractor = Extractor()
        renamer = Renamer()
        mover = Mover()
        tagger = Tagger()
        # database = Database()
        # scanner = scanner.Scanner(database)

        counter = 75
        while True:
            extractor.extract()
            renamer.rename()
            mover.move()
            tagger.tag()

            if counter > 72:
                counter = 0
                # scanner.scan()
            counter = counter + 1
            print('sleeping for 300s')
            sleep(300)

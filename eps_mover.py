import os

# musicFolderPathTODO = "\\\\192.168.1.2\\Music\\Eps\\__TODO"
musicFolderPathTODO = "\\volume1\\Music\\Eps\\__TODO"
musicFolderPath = "\\\\192.168.1.2\\Music\\Eps"
musicFolderPath = "\\volume1\\Music\\Eps"
from os import listdir
from os.path import isfile, join

labels = {
    '247HC': '247 Hardcore',
    'A2REC': 'A2 Records',
    'ABUSEDDIGI': 'Abused_Recordingz',
    'ACR': 'Acid Reign',
    'ACT': 'Activa',
    'ACTDIGI': 'Activa',
    'ACTDRK': 'Activa Dark',
    'ACTSH': 'Activa Shine',
    '_': 'Actuation',
    'AT': 'Adrenaline_Tracks',
    'AFT3R': 'Afterlife Recordings (2) (AFT3R)',
    'AFTER': 'Afterlife Recordings (AFTER)',
    'AR': 'Aggressive Records',
    'ANY': 'Anarchy',
    'AM': 'Annihilate Music',
    'ASR': 'Antisocial Records',
    'APEX': 'APEX Records',
    'ARN': 'Arena_Label',
    'ARMADA': 'Armada Music',
    'AOC': 'Art of creation',
    '_': 'ARTificial',
    'ASTROPROJEKT': 'AstroFonik',
    'APHET': 'Audiophetamine',
    'ARM': 'Aurora Mortem records',
    'AVIO': 'AVIO',
    'AVIOCD': 'AVIO',
    'B2S': 'B2S',
    'BABY': 'Babys Back',
    '_': 'Bad Bitches',
    'BBR': 'Barbaric Records',
    'BF': 'Barong Family',
    'BD_': 'Bass-D Music',
    'BSC': 'Basscon Records',
    'BYMD': 'Be Yourself Music',
    'BYMCD': 'Be Yourself Music',
    'BKJN': 'Beter Kom Je Niet BKJN',
    'BIT': 'Bit Italy',
    'BMR': 'Black Mirror Society',
    '': 'Black Reaper Records',
    'BBD': 'Blackbox Digital',
    'BLU': 'Blutonium Records',
    'BOMB': 'Bomb records',
    'BAB': 'Bombs And Bullets',
    'BT': 'Border Town',
    'BBR': 'Bounce Back Records',
    '_': 'Brachiale Musikk',
    '_': 'Brandstichters',
    'BYT': 'Break The Rules',
    'BHM': 'Brennan Heart Music',
    'BMUT': 'Bring Me Up Tempo',
    'BTR': 'Bring the riot',
    'BSR': 'Broken Strain Records',
    'BRU': 'Brutale',
    'CM': 'Caput Mundi Records',
    'CRT': 'Cartel00 Records',
    'CAUSE': 'Cause Records',
    'CBK-': 'Cawfee Break',
    'CBK': 'Cawfee Break',
    'CUL': 'Chaotic Universe',
    'CFR': 'Chosen_Few_Recordz',
    'CLDG': 'Cloud 9 Dance',
    'CLDM': 'Cloud 9 Dance',
    '_': 'Cloud 9 Music',
    '_': 'CNNCTD',
    '_': 'CrunkD Records',
    '_': 'Crypton Music',
    'CR.': 'Cyndium Records',
    'CR': 'Cyndium Records',
    '_': 'D-Fence Records',
    '_': 'D8K2OU~7',
    '_': 'Danamite',
    '_': 'Dance Pollution',
    '_': 'Dance Tunes BV',
    'DARKUL': 'Darkside unleashed',
    '_': 'Deathchant',
    '_': 'Deathmatch Music',
    '_': 'Delict Records',
    '_': 'Delirium Music',
    'DQX': 'Dequinox Music',
    '_': 'Derailed Trax black',
    '_': 'Derailed Trax grey',
    'DT': 'Derailed Traxx',
    'DVNT': 'DeviantMusic',
    '_': 'DF records',
    '_': 'Digital Abuse Records',
    '_': 'Digital Age',
    '_': 'Digital Plague',
    '_': 'Dimitri K Records',
    '_': 'Dirty Rave',
    'DWX': 'Dirty workz',
    'DSBR': 'Disobey Records',
    '_': 'DistroKid',
    '_': 'DJs United Orange Records',
    '_': 'DJs United Red Records',
    '_': 'DJs United Zanzatraxx',
    'DOG': 'Dogfight Records',
    '_': 'Dort Music',
    '_': 'Drillkore Records',
    'DROKZ': 'Drokz',
    'DTS': 'DTS',
    'DMW': 'Dutch Master Works',
    'DWARF': 'Dwarf Records',
    '_': 'Eastside Underground',
    'ELFX': 'Electric Fox',
    '_': 'Element',
    '_': 'Elitepauper Publishers',
    '_': 'Ellivium Music',
    '_': 'EMFA Music',
    '_': 'Empire Hardcore Music',
    'EOL': 'End of line',
    '_': 'Enzyme K7',
    'ENZYME': 'Enzyme Records',
    '_': 'Enzyme VIP',
    '_': 'Enzyme X',
    '_': 'Epic Local',
    '_': 'Essential Platinum',
    '_': 'Eternity',
    '_': 'Euphoric Frenchcore',
    '_': 'Euphoric Madness',
    '_': 'Evolve AU',
    '_': 'Exit Records',
    'EXT': 'Exitus Hardcore',
    '_': 'Exode Records',
    '_': 'Face Your Fear',
    '_': 'Fe Records',
    '_': 'Fear FM',
    'FLM': 'Fear Less Music',
    '_': 'Filthy Face Records',
    'FISHRICE': 'Fish and Rice Recordings',
    '??': 'Foolish',
    'FWXXDIGI': 'Footworxx',
    '_': 'Freestyle',
    '_': 'Frenchcore Decadence',
    'FWWSVP': 'Frenchcore SVP',
    'FWWSGL': 'Frenchcore Worldwide',
    '_': 'FrenchKickz Records',
    '_': 'FRFC Records',
    '_': 'FROSTBYTE',
    '_': 'Fucking Bastard Records',
    'FUSION': 'Fusion records',
    'SICKRAGE': 'Future Sickness Recordings',
    'FVCK': 'FVCK GENRES',
    'GBD': 'Gearbox Digital',
    'GBE': 'Gearbox Euphoria',
    'GHD': 'Gearbox Hard Dance',
    'GBO': 'Gearbox Overdrive',
    'GBR': 'Gearbox Revolutions',
    '_': 'GEE thAng Music',
    '_': 'Genosha One Seven Five',
    '_': 'Genosha Records',
    'GPF': 'GPF Recordz',
    'GREAZY': 'GPF Recordz',
    '_': 'Guillotine Recordings',
    '_': 'Handkcuf Records',
    'H2O': 'H2oh Recordings',
    '_': 'Hard Music Records Gold',
    '_': 'Hard Music Records Raw',
    '_': 'Hard With Style',
    '_': 'Hardcore Blasters',
    '_': 'Hardcore Blasters Jump',
    '_': 'Hardcore Canada Records',
    'HF': 'Hardcore France',
    '_': 'Hardcore Malice',
    '_': 'Hardcore Mayhem',
    '_': 'Hardcore Riot',
    '_': 'HARDCORE TANOC',
    'HC': 'Hardstyle Creation',
    'HSF': 'Hardstyle France',
    '_': 'Hardtek.JP',
    '_': 'HARRIS & FORD',
    '_': 'HCMF',
    '_': 'Head Fuck Negative',
    '_': 'Head Fuck Records',
    '_': 'Head Fuck Records Digital',
    'H4H': 'Heart for Hard',
    'HELLS': 'Hells Recordings',
    'HERESY': 'HERESY',
    'DISCIPLES': 'Heresy Disciples',
    'HBR': 'Hexablast Records',
    'HKV': 'Hong Kong Violence',
    '_': 'I Am Frenchcore',
    'IAH': 'I AM HARDSTYLE',
    'IAHA': 'I AM HARDSTYLE - Amplify',
    '_': 'I Love Beats',
    '_': 'Identity Records',
    'IGD': 'Ignition Digital',
    '_': 'IGor Records',
    '_': 'Important Corestyle',
    '_': 'Important Hardcore',
    '_': 'Important Hardcore Limited',
    '_': 'Independent',
    '_': 'Indus3 Records',
    'ISRD': 'Industrial Strength',
    '_': 'Infected Records',
    'INFEX': 'InfeXious Raw',
    '_': 'Inner Rage Productions',
    'ISX': 'Insaniax',
    '_': 'Intents Records',
    '_': 'Invaders & Science',
    '_': 'Invaders Records',
    '_': 'Invaissor Records',
    'IR': 'Irrational Impulses',
    '_': 'Italian Hardstyle',
    '_': 'Jabroer',
    '_': 'JDX Music',
    'K1R': 'K1 Recordz',
    'KKR': 'KarmaKontra Records',
    'KKRC': 'KarmaKontra Records',
    'KKV': 'KarmaKontra Records',
    'KKE': 'KarmaKontra Records',
    'KRE': 'KarmaKontra Records',
    '_': 'Karnage Records',
    'KIU': 'Keep it up',
    '_': 'Keeping The Rave Alive',
    '_': 'KETA RECORDS',
    '_': 'KNOR Records',
    '_': 'Kontor Records',
    '_': 'Kurrupt Recordings Hard',
    '_': 'LASER [BNL]',
    '_': 'Le Bask Records',
    '_': 'Lethal Theory',
    '_': 'LEVEL',
    'LCM': 'Lose Control Music',
    '_': 'LOVE 4 HARD',
    '_': 'Love Hz',
    '_': 'LoverLoud',
    '_': 'Lowroller Inc',
    'LT': 'Luca Testa',
    'LT_': 'Luca Testa',
    '_': 'Madback Records',
    '_': 'Major Smoke Records',
    '_': 'Mandala',
    '_': 'Manneken Pis',
    '_': 'Mark With a K',
    '_': 'Masif',
    'MD': 'Massive Dynamic',
    'MOHDIGI': 'Masters Of Hardcore',
    '_': 'MAXXIMIZE',
    ''
    'MMT': 'Meccano Music',
    'MRV': 'Megarave Records',
    '_': 'Midify',
    'MIM': 'Minus Is More',
    'MINUS': 'Minus Is More',
    '_': 'Monolith',
    '_': 'Monstercat',
    '_': 'Monsters Of Terrorcore Records',
    '_': 'More Music And Media',
    '_': 'Motormouth Records',
    '_': 'Mr. Ivex Auditory',
    '_': 'Mvtate',
    'MTIU': 'My tempo is uptempo',
    '_': 'My Way',
    'MYM': 'My Way Music',
    '_': 'Negative Audio',
    '_': 'Nekrolog1k Recordings',
    'NEO': 'Neophyte records',
    'NMR': 'Neox Music Records',
    'NMR_': 'Neox Music Records',
    '_': 'New Dawn Records',
    'NWO': 'New World Order Records',
    '_': 'Nexchapter',
    '_': 'Next Chapter',
    '_': 'NG Recordings',
    '_': 'Nightbreed Nocturnal',
    'NBQ': 'Nightbreed Records',
    '_': 'NightCode Recordings',
    '_': 'No Es Ruido',
    '_': 'Noisecontrol Records',
    '_': 'Noisekick Records',
    '_': 'Noize Junky',
    '_': 'Northern Outpost',
    '_': 'Nothing 4 All',
    '_': 'NOTYPE',
    '_': 'NRGY Music',
    '_': 'Nutty Traxx',
    '_': 'OBLIVION',
    '_': 'Oblivion Music',
    '_': 'Oblivion Underground Recordings',
    'OFFRAGE': 'Offensive Rage',
    '_': 'Offensive Records',
    '_': 'Omny Lab',
    '_': 'One More Rep',
    'ONESEVENTY': 'One Seventy',
    '_': 'Origins',
    '_': 'Othercide',
    'PR': 'Partyraiser Records',
    'PCR': 'Peacock Records',
    '_': 'Peacocks Exclusives',
    '_': 'PIJN',
    '_': 'Pink Beats',
    '_': 'PL4N3T X',
    '_': 'Pow records',
    '_': 'Power Hour Records',
    '_': 'Prague Nightmare Records',
    '_': 'Project Chaos Records',
    '_': 'Project Red',
    '_': 'Promo Test',
    '_': 'Prospect',
    '_': 'Prototypes Records',
    '_': 'Psychik Genocide',
    'PM': 'Pure Massive Records',
    'PLM': 'Pussy Lounge Music',
    'Q': 'QDance',
    'QDIG': 'QDance',
    'NEXT': 'Qdance presents NEXT',
    'QORE': 'QORE',
    '_': 'Qult Records',
    'R909-': 'Randy909',
    'RAPT': 'Rapture Records',
    '_': 'Rave Alert',
    '_': 'Rave Culture',
    '_': 'Rave Generation',
    '_': 'Rave Instinct',
    '_': 'REBiRTH Events Records',
    'REBL': 'Rebl Records',
    '_': 'Relentless Digital',
    '_': 'Relianze',
    '_': 'Remz Roster',
    'REVR': 'Revealed Recordings',
    '_': 'Revloxist',
    '_': 'ROQ n Rolla',
    '_': 'Rotterdam Records',
    'ROUGHR': 'Rough Recruits',
    'ROUGH': 'Roughstate',
    '_': 'RSLVD Records',
    '_': 'RSU Records',
    'RV': 'Rude Vibes',
    '_': 'Ruffex',
    '_': 'Ruffneck Anomalies',
    '_': 'Ruffneck Records',
    '_': 'S-Trax',
    'SSR': 'Savage Squad Recordings',
    'SSROZ': 'Savage Squad Recordings OZ',
    'SCAN': 'Scantraxx',
    'BLACK': 'Scantraxx Black',
    'SCARB': 'Scantraxx Carbon',
    '_': 'Scantraxx Evolutionz',
    '_': 'Scantraxx Global',
    'ITAL': 'Scantraxx Italy',
    'PRSPX': 'Scantraxx Prospexx',
    '_': 'Scantraxx Reloaded',
    'SSL': 'Scantraxx Silver',
    'SEADIGI': 'Sealand Recordings',
    '_': 'Sefa Music',
    '_': 'Seismic Raw',
    '_': 'Seismic Records',
    '_': 'Shadow Mask',
    '_': 'Sharp As A Knife Records',
    '_': 'ShutUpAndRave',
    'SR': 'SickCore Records',
    '_': 'Sinphony',
    '_': 'Skink',
    '?': 'Smash',
    'SMASH': 'Smash Records',
    'SSO': 'Smashed Society',
    'SPM': 'Snakepit Music',
    '_': 'Snowbass Records',
    '_': 'Sound of Hardcore',
    '_': 'Speedcore Italia',
    'SPEQTRUM': 'Speqtrum Music',
    '_': 'Spike Protein',
    '_': 'Spinning records',
    '_': 'Spirit of Hardstyle',
    '_': 'Spline Music',
    'SPOON': 'Spoontech Records',
    'SOA': 'State Of Anarchy',
    '_': 'Static Gravity Records',
    '_': 'Subground',
    '_': 'Super Solid',
    '_': 'Supernova Records',
    '_': 'Superplastik',
    '_': 'Supreme Intelligence',
    '_': 'Symphony of Core',
    '_': 'System outage',
    '_': 'T!LLT',
    '_': 'TC Labs',
    '_': 'TC Records',
    '_': 'Terror Machine Records',
    '_': 'Terrordrang',
    '_': 'Terrordrang Records',
    '_': 'Terrorheads',
    'TEX_': 'Texcore',
    'TEX': 'Texcore',
    '_': 'The boss records',
    '_': 'The Funky Cat',
    '_': 'The Magic Show',
    '_': 'The Third Movement',
    '_': 'Therabyte',
    'TCREC': 'Theracords',
    'TCC': 'Theracords Classics',
    'TCLABS': 'Theracords Labs',
    'TCLABSPRO': 'Theracords Labs',
    'TIF': 'This Is Frenchcore Recordings',
    'TIH?': 'This is hardcore',
    'TIH': 'This Is Hardstyle',
    'TIT': 'This is Terror',
    'TIUR': 'This is uptempo records',
    '_': 'Thorax Productions',
    'TDM': 'Thunderdome Music',
    '?': 'Thunderdome Records',
    '_': 'Titanic',
    'TOFF': 'TOFF Music',
    '_': 'ToXicCore Rec',
    'TRAX': 'Traxtorm',
    '_': 'Triple G Records',
    'TSR': 'Triple Six Records',
    '_': 'Triplex Records',
    '_': 'Triton',
    '_': 'Twisted sound records',
    'UCSTR': 'U Cant Stop The Rave',
    '_': 'Unbreakable Records',
    '_': 'Underground Gangsta Records',
    'UIPR': 'Underground Industry Records',
    '_': 'Underground Tekno',
    'UNFR': 'Unfold Music',
    '_': 'Unite Records',
    '_': 'Unleashed Records',
    '_': 'Unlocked Records',
    'UPR': 'Upcoming Records',
    '_': 'Uptempo Hardcore Records',
    '_': 'Uptempo is the tempo records',
    '_': 'Vyolet',
    '_': 'War Force Records',
    '_': 'Warner Music Denmark',
    'WER': 'WE R',
    'WER': 'WE R RAW',
    'WERT': 'WE R Tomorrow',
    '_': 'WLFPCK',
    '_': 'Wolf Clan',
    'WOLV': 'Wolvpack Recordings',
    '_': 'Worldwidedomination Records',
    '_': 'Wuze Records',
    '_': 'X-Bone',
    '_': 'X-Qlusive Holland Records',
    '_': 'X-Rate Records',
    '_': 'X-RAW',
    'XTR': 'X-Tinction Recordz',
    '_': 'X7M',
    '_': 'XBREED Records',
    '_': 'Xploded Music Limited',
    'XPN': 'XPN Music',
    'XAV': 'Xtreme Audio Violence',
    '_': 'Xtreme Records',
    '_': 'XTRMN8 RECORDS',
    '_': 'Yosuf',
    '_': 'Young Guns Records',
    '_': 'Zanza Files',
    '_': 'Zanzalabs',
    '_': 'Zero Day Records',
    '_': 'Zoo Digital',
    '_': 'Zoo Records',
}


def get_cat_id(folder):
    catid = folder.split(' ')
    return catid[0]


def get_label_by_cat_id():
    print('a')


import string


# cleaned = yourstring.rstrip(string.digits)
def move():
    onlyfolders = [f for f in listdir(musicFolderPathTODO) if not isfile(join(musicFolderPathTODO, f))]
    for folder in onlyfolders:
        catid = get_cat_id(folder);

        if(len(catid)):
            last_char = catid[-1]

            # Remove E, D, R, or B postfix
            if(last_char == 'B' or last_char == 'D' or last_char == 'E'  or last_char == 'R' ):
                if(catid[-2].isdigit()):
                     catid = catid[:-1]

            # Strip last numbers after PRO
            catid_prefix = catid.rstrip(string.digits);

            #remove pro if used
            if 'PRO' in catid_prefix:
                catid_prefix = catid_prefix[:-3]

            #Remove last numbers before PRO
            catid_prefix = catid_prefix.rstrip(string.digits);
        try:
            label = labels[catid_prefix]
            src = musicFolderPathTODO+'\\'+folder
            dst = musicFolderPath+'\\'+ label+'\\'+ folder
            print('src: '+ src)
            print('dst: '+ dst)
            os.rename(src, dst)
        except:
            print('Could not find label for \''+folder+ '\'')

import json
from pathlib import Path
import requests
from time import time


class CardExpJson:
    def __init__(self, ld):
        self.ld = ld
        self.imgurls = []
        self.multiverse_ids = []
        self.uids = []
        self.names = []

        self.cards = None
        self.jsonexps = None

    def load_json(self):

        unzipped = Path('AllSets.json')
        zipped = Path('AllSets.json.zip')
        if not (unzipped.is_file()):
            if zipped.is_file():
                print('[Info] Descomprimiendo el archivo zip que contiene el archivo json...')
                import zipfile
                zip_ref = zipfile.ZipFile('AllSets.json.zip', 'r')
                zip_ref.extractall()
                zip_ref.close()
            else:
                self.ld.show_dialog('Descargando AllSets.json desde la web oficial...')
                self.ld.set_range(1, 100)
                print('[Info] Descargando AllSets.json...')
                response = requests.get(
                    'https://mtgjson.com/json/AllSets.json', stream=True, headers={'Accept-Encoding': None})
                with open('AllSets.json', 'wb') as f:
                    count = 1
                    total = response.headers.get('content-length')
                    if total is None:
                        f.write(response.content)
                    else:
                        total = int(total)
                        block_size = max(total / 1000, 1024 * 1024)
                        for data in response.iter_content(chunk_size=block_size):
                            percent = int(count * block_size * 100 / total)
                            self.ld.set_value(percent)
                            f.write(data)
                            count += 1
                self.ld.close()
        self.ld.set_range(0, 0)
        self.ld.show_dialog('Cargando AllSets.json...')
        self.read_json()
        self.ld.set_range(0, 1)
        self.ld.close()

    def read_json(self):

        t0 = time()
        try:
            self.jsonexps = json.loads(open('AllSets.json', encoding="utf8").read())
        except MemoryError:
            raise Exception('[Error] Please ensure you are running 64 bit Python')
        t1 = time()
        print('[Info] Archivo AllSets.json cargado en {:.1f} segundos...'.format(t1 - t0))

    def get_exp_name(self, code):
        for i in (list(self.jsonexps.keys())):
            _name = self.jsonexps[i]['name']
            if i == code:
                return _name
    
    def get_exps(self):
        # return alphabetized list of all expansions, removing expansions for which no card images exist
        retexps = []
        exps_dict = {}
        for exp in (list(self.jsonexps.keys())):
            cards = self.jsonexps[exp]['cards']
            name = self.jsonexps[exp]['name']
            empties = False
            exists = False
            multiverse_ids = []
            for card in cards:
                try:
                    multiverse_ids.append(card['multiverseId'])
                    exists = True
                except:
                    multiverse_ids.append(None)
                    empties = True
            if empties and (not exists):
                pass
            elif empties and exists:
                pass
            else:
                retexps.append(exp)
                if name == 'Revised Edition':
                    name = 'Revised'
                elif name == 'Unlimited Edition':
                    name = 'Unlimited'
                elif name == 'Limited Edition Beta':
                    name = 'Beta'
                elif name == 'Limited Edition Alpha':
                    name = 'Alpha'
                exps_dict[exp] = name
        retexps = sorted(retexps)
        return retexps, exps_dict
    
    def load_imgs(self, expcode):
            try:
                self.cards = self.jsonexps[expcode]['cards']
            except:
                raise NameError('[Error] No set found with that setcode')

            self.names = []
            for card in self.cards:
                self.names.append(card['name'])

            self.uids = []
            for card in self.cards:
                self.uids.append(card['uuid'])

            self.multiverse_ids = []

            empties = False
            exists = False
            for card in self.cards:
                try:
                    self.multiverse_ids.append(card['multiverseId'])
                    exists = True
                except:
                    self.multiverse_ids.append(None)
                    empties = True
            if empties and (not exists):
                print('[Error] Imagenes no accesibles')
            elif empties and exists:
                print('[Peligro] Algunas imagenes no accesibles')
            else:
                print('[Info] Todas las imagenes accesibles')

            # self.imgurls = list of all URLs to gatherer card images
            for m_id in self.multiverse_ids:
                if m_id is None:
                    self.imgurls.append(None)
                else:
                    self.imgurls.append(
                        'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + str(m_id) + '&type=card')

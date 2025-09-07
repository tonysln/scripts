from PIL import ExifTags, Image
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import sys


def dms_to_dd(latd, lond, lat_sign='N', lon_sign='E'):
    lat = float(latd[0]) + float(latd[1])/60 + float(latd[2])/3600
    lon = float(lond[0]) + float(lond[1])/60 + float(lond[2])/3600

    if lat_sign == 'S':
        lat = -lat
    if lon_sign == 'W':
        lon = -lon

    return lat,lon


inn = sys.argv[1] + ('' if sys.argv[1].endswith('/') else '/')
out = sys.argv[2]
f = open(out, 'a')
c = 0
# C_LIM = 500
data = []

print(f'Writing to {out}')

with open(out, 'a') as f:
    for year in tqdm(range(2000, 2026)):
        d = inn + str(year)

        for file in listdir(d):
            fp = join(d, file)
            if isfile(fp) and any([fp.endswith(ext) for ext in ['.jpg', '.jpeg', '.png']]):
                im = Image.open(fp)
                exif = im.getexif()
                if exif:
                    gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
                    if gps_ifd and len(gps_ifd) >= 4:
                        try:
                            lat_dms = gps_ifd[2]
                            lon_dms = gps_ifd[4]
                            lat_sign = gps_ifd[1]
                            lon_sign = gps_ifd[3]

                            lat,lon = dms_to_dd(lat_dms, lon_dms, lat_sign, lon_sign)

                            # fn = file.split('.')[0]
                            f.write(f'{lon},{lat}\n')
                            c += 1
                        except:
                            print('[!]', gps_ifd[1])

            # if c >= C_LIM:
            #     print('\n'.join(data))
            #     c = 0

print(f'Wrote {c} entries.')
print('Done.')

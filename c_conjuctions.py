from skyfield import almanac
from skyfield.api import load, wgs84
import argparse, sys


def start(lat, lon, o1, o2, f):
    eph = load("de440s.bsp") 
    data = {
        'moon': eph['moon'],
        'jupiter': eph['jupiter barycenter'],
        'mars': eph['mars barycenter'],
        'saturn': eph['saturn barycenter'],
        'neptune': eph['neptune barycenter'],
        'uranus': eph['uranus barycenter'],
        'mercury': eph['mercury'],
        'venus': eph['venus'],
        'earth': eph['earth']
    }

    earth = data['earth']
    town = wgs84.latlon(lat, lon) 
    observer = earth + town

    ts = load.timescale()
    t = ts.now()

    max = 100 * 365 #100 years +-

    planet1 = data.get(o1.lower())
    planet2 = data.get(o2.lower())

    if 'earth' in list(map(str.lower, [o1, o2])):
        print('The Earth is our planet!')
        input('Press enter to exit... ')
        exit()

    if not planet1 or not planet2:
        print('Invalid names of planets!')
        input('Press enter to exit... ')
        exit()

    print("TIME IN UTC!!!")
    print('Looking for conjuctions for 100 years...')

    file_data = ""
    for i in range(1, max+1):
        nt = t+i
        e = observer.at(nt)

        p = e.observe(planet1).apparent()
        p1 = e.observe(planet2).apparent()
        separation = p.separation_from(p1).degrees
        if 0.5 < separation < 1:
            print('Less 1 degree separation!')
        elif separation <= 0.5:
            print("Less 30' separation!")
        else:
            continue  
        inf = nt.utc_iso(' ') + ' ' + '{:.2f}′'.format(separation * 60)
        print(inf)
        file_data += inf+"\n"
    
    if file_data == "":
        print("Conjuctions have not been founded")
    if f and file_data != "":
        with open(f, 'w+', encoding='utf-8') as file:
            file.write(file_data.strip())

    input('Press enter to exit... ')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('You need to enter at least two planets')
        exit()

    parser = argparse.ArgumentParser()

    parser.add_argument('-lat', default=0.0, type=float, help="Latitude")
    parser.add_argument('-lon', default=0.0, type=float, help='Longitude')
    parser.add_argument('--file', '-f', default=None, type=str, help='Filename')
    parser.add_argument('planet1', type=str, help='First planet')
    parser.add_argument('planet2', type=str, help='Second planet')

    args = parser.parse_args()

    start(args.lat, args.lon, args.planet1, args.planet2, args.file)
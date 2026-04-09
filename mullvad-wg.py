#!/usr/bin/env python3

import os
import subprocess
import glob
import curses

COUNTRIES = {
  'al': 'Albania',
  'ar': 'Argentina',
  'at': 'Austria',
  'au': 'Australia',
  'be': 'Belgium',
  'bg': 'Bulgaria',
  'br': 'Brazil',
  'ca': 'Canada',
  'ch': 'Switzerland',
  'cl': 'Chile',
  'co': 'Colombia',
  'cy': 'Cyprus',
  'cz': 'Czech Republic',
  'de': 'Germany',
  'dk': 'Denmark',
  'ee': 'Estonia',
  'es': 'Spain',
  'fi': 'Finland',
  'fr': 'France',
  'gb': 'UK',
  'gr': 'Greece',
  'hk': 'Hong Kong',
  'hr': 'Croatia',
  'hu': 'Hungary',
  'id': 'Indonesia',
  'ie': 'Ireland',
  'il': 'Israel',
  'it': 'Italy',
  'jp': 'Japan',
  'mx': 'Mexico',
  'my': 'Malaysia',
  'ng': 'Nigeria',
  'nl': 'Netherlands',
  'no': 'Norway',
  'nz': 'New Zealand',
  'pe': 'Peru',
  'ph': 'Philippines',
  'pl': 'Poland',
  'pt': 'Portugal',
  'ro': 'Romania',
  'rs': 'Serbia',
  'se': 'Sweden',
  'sg': 'Singapore',
  'si': 'Slovenia',
  'sk': 'Slovakia',
  'th': 'Thailand',
  'tr': 'Turkey',
  'ua': 'Ukraine',
  'us': 'USA',
  'za': 'South Africa',
}

CITIES = {
  'adl': 'Adelaide',
  'akl': 'Auckland',
  'ams': 'Amsterdam',
  'ath': 'Athens',
  'atl': 'Atlanta, GA',
  'bcn': 'Barcelona',
  'beg': 'Belgrade',
  'ber': 'Berlin',
  'bkk': 'Bangkok',
  'bne': 'Brisbane',
  'bod': 'Bordeaux',
  'bog': 'Bogota',
  'bos': 'Boston, MA',
  'bru': 'Brussels',
  'bts': 'Bratislava',
  'bud': 'Budapest',
  'bue': 'Buenos Aires',
  'buh': 'Bucharest',
  'chi': 'Chicago, IL',
  'cph': 'Copenhagen',
  'dal': 'Dallas, TX',
  'den': 'Denver, CO',
  'det': 'Detroit, MI',
  'dub': 'Dublin',
  'dus': 'Dusseldorf',
  'for': 'Fortaleza',
  'fra': 'Frankfurt',
  'glw': 'Glasgow',
  'got': 'Gothenburg',
  'hel': 'Helsinki',
  'hkg': 'Hong Kong',
  'hou': 'Houston, TX',
  'iev': 'Kyiv',
  'ist': 'Istanbul',
  'jnb': 'Johannesburg',
  'jpu': 'Jakarta',
  'kul': 'Kuala Lumpur',
  'lax': 'Los Angeles, CA',
  'lim': 'Lima',
  'lis': 'Lisbon',
  'lju': 'Ljubljana',
  'lon': 'London',
  'los': 'Lagos',
  'mad': 'Madrid',
  'mel': 'Melbourne',
  'mia': 'Miami, FL',
  'mil': 'Milan',
  'mkc': 'Kansas City, MO',
  'mma': 'Malmö',
  'mnc': 'Manchester',
  'mnl': 'Manila',
  'mrs': 'Marseille',
  'mtr': 'Montreal',
  'nic': 'Nicosia',
  'nyc': 'New York, NY',
  'osa': 'Osaka',
  'osl': 'Oslo',
  'par': 'Paris',
  'per': 'Perth',
  'phx': 'Phoenix, AZ',
  'pmo': 'Palermo',
  'prg': 'Prague',
  'qas': 'Ashburn, VA',
  'qro': 'Queretaro',
  'rag': 'Raleigh, NC',
  'sao': 'Sao Paulo',
  'scl': 'Santiago',
  'sea': 'Seattle, WA',
  'sin': 'Singapore',
  'sjc': 'San Jose, CA',
  'slc': 'Salt Lake City, UT',
  'sof': 'Sofia',
  'sto': 'Stockholm',
  'svg': 'Stavanger',
  'syd': 'Sydney',
  'tia': 'Tirana',
  'tll': 'Tallinn',
  'tlv': 'Tel Aviv',
  'tor': 'Toronto',
  'txc': 'McAllen, TX',
  'tyo': 'Tokyo',
  'uyk': 'Secaucus, NJ',
  'van': 'Vancouver',
  'vie': 'Vienna',
  'vlc': 'Valencia',
  'was': 'Washington DC',
  'waw': 'Warsaw',
  'yyc': 'Calgary',
  'zag': 'Zagreb',
  'zrh': 'Zurich',
}

ACTIVE_CONF = "/tmp/mullvad-wg-active.conf"


def check_mullvad_status(url="https://am.i.mullvad.net/connected"):
  try:
    result = subprocess.run(["curl", "-s", "--max-time", "5", url], capture_output=True, text=True)
    if result.returncode == 0: return result.stdout.strip()
  except Exception: pass
  return f"Could not reach {url}"

def stop_wireguard(interface):
  subprocess.run(["wg-quick", "down", interface])
  print("Wireguard stopped.")
  if os.path.exists(ACTIVE_CONF): os.remove(ACTIVE_CONF)

def start_wireguard(interface):
  subprocess.run(["wg-quick", "up", interface])
  with open(ACTIVE_CONF, "w") as f: f.write(interface)
  print(f"WireGuard started on {interface}.")
  print(check_mullvad_status())

def list_configs():
  configs = {}
  for path in glob.glob("/etc/wireguard/*.conf"):
    filename = os.path.basename(path).replace(".conf", "")
    parts = filename.split("-")
    if len(parts) >= 3 and parts[0] in COUNTRIES and parts[1] in CITIES:
      co = parts[0]
      ci = parts[1]
      if co not in configs: configs[co] = {}
      if ci not in configs[co]: configs[co][ci] = []
      configs[co][ci].append(filename)
  return configs


def select_config(configs):
  def _main(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.BUTTON4_PRESSED | curses.BUTTON5_PRESSED)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    expanded = set()
    current = 0
    top = 0
    country_codes = tuple(sorted(configs.keys()))

    def build_items():
      items = []
      for co in country_codes:
        items.append(('country', co))
        if co in expanded:
          for ci in sorted(configs[co].keys()):
            for cfg in sorted(configs[co][ci]):
              items.append(('config', co, ci, cfg))
      return items

    def find_next(items, start):
      for i in range(start + 1, len(items)):
        if items[i][0] == 'config': return i
      return start

    def find_prev(items, start):
      for i in range(start - 1, -1, -1):
        if items[i][0] == 'config': return i
      return start

    def clamp(val, lo, hi): return max(lo, min(val, hi))

    def toggle_country(co, items):
      if co in expanded: expanded.remove(co)
      else: expanded.add(co)
      new_items = build_items()
      # find the country header in the new list to keep cursor on it
      for i, item in enumerate(new_items):
        if item[0] == 'country' and item[1] == co:
          return new_items, i
      return new_items, 0

    items = build_items()
    result = None

    while True:
      height, width = stdscr.getmaxyx()
      visible_rows = height - 4
      stdscr.clear()

      header = "Mullvad WireGuard Config Selection ([] to toggle country, Enter/lclick to select, q to quit)"
      stdscr.addstr(0, 0, header[:width-1], curses.A_BOLD)
      stdscr.addstr(1, 0, "-" * (width - 1))

      current = clamp(current, 0, len(items) - 1)
      if current < top:
        top = current
      elif current >= top + visible_rows:
        top = current - visible_rows + 1
      top = clamp(top, 0, max(0, len(items) - visible_rows))

      row = 3
      for i in range(top, min(top + visible_rows, len(items))):
        vis_idx = i - top
        item = items[i]
        selected = i == current
        attr = curses.A_REVERSE if selected else curses.A_NORMAL

        if item[0] == 'country':
          co = item[1]
          marker = "[-]" if co in expanded else "[+]"
          country_name = COUNTRIES.get(co, co)
          line = f"  {marker} {country_name}"
        else:
          co, ci, cfg = item[1], item[2], item[3]
          city_name = CITIES.get(ci, ci)
          line = f"      {city_name} / {cfg}"

        try:
          stdscr.addstr(row + vis_idx, 0, line[:width-1], attr)
        except curses.error:
          pass

      stdscr.refresh()

      key = stdscr.getch()
      if key == -1:
        curses.napms(30)
        continue

      if key in (curses.KEY_DOWN, ord('j')):
        current = clamp(current + 1, 0, len(items) - 1)
      elif key in (curses.KEY_UP, ord('k')):
        current = clamp(current - 1, 0, len(items) - 1)
      elif key in (curses.KEY_ENTER, curses.KEY_RIGHT, ord(' '), ord('\n'), ord('\r')):
        item = items[current]
        if item[0] == 'country':
          items, current = toggle_country(item[1], items)
        else:
          result = item[3]
          break
      elif key == curses.KEY_MOUSE:
        try:
          _, mx, my, _, bstate = curses.getmouse()
        except curses.error:
          continue
        if bstate & curses.BUTTON4_PRESSED:
          current = clamp(current - 3, 0, len(items) - 1)
        elif bstate & curses.BUTTON5_PRESSED:
          current = clamp(current + 3, 0, len(items) - 1)
        elif bstate & curses.BUTTON1_CLICKED:
          idx = my - 3 + top
          if 0 <= idx < len(items):
            current = idx
            item = items[current]
            if item[0] == 'country':
              items, current = toggle_country(item[1], items)
            else:
              result = item[3]
              break
      elif key in (ord('['), ord(']')):
        item = items[current]
        if item[0] == 'country':
          co = item[1]
          if key == ord(']') and co not in expanded:
            items, current = toggle_country(co, items)
          elif key == ord('[') and co in expanded:
            items, current = toggle_country(co, items)
      elif key in (ord('q'), ord('Q'), 27):
        break

      curses.napms(30)

    stdscr.nodelay(False)
    return result
  return curses.wrapper(_main)

def confirm_disconnect(interface):
  status = check_mullvad_status()

  def _main(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    current = 0
    options = ["Disconnect", "Cancel"]

    while True:
      height, width = stdscr.getmaxyx()
      stdscr.clear()
      stdscr.addstr(0, 0, f"WireGuard is active: {interface}", curses.A_BOLD)
      stdscr.addstr(1, 0, "-" * (width - 1))
      stdscr.addstr(3, 0, status)
      stdscr.addstr(5, 0, "Disconnect?")

      for i, opt in enumerate(options):
        attr = curses.A_REVERSE if i == current else curses.A_NORMAL
        prefix = ">" if i == current else " "
        try:
          stdscr.addstr(7 + i, 2, f"{prefix} {opt}", attr)
        except curses.error:
          pass

      stdscr.refresh()

      key = stdscr.getch()
      if key == -1:
        curses.napms(30)
        continue

      if key in (curses.KEY_DOWN, ord('j')):
        current = min(current + 1, len(options) - 1)
      elif key in (curses.KEY_UP, ord('k')):
        current = max(current - 1, 0)
      elif key in (curses.KEY_ENTER, ord(' '), ord('\n'), ord('\r')):
        return current == 0
      elif key == curses.KEY_MOUSE:
        try:
          _, mx, my, _, bstate = curses.getmouse()
        except curses.error:
          continue
        if bstate & curses.BUTTON1_CLICKED:
          idx = my - 7
          if 0 <= idx < len(options):
            return idx == 0
      elif key in (ord('q'), ord('Q'), 27):
        return False

      curses.napms(30)
    return False
  return curses.wrapper(_main)


if __name__ == "__main__":
  if os.path.exists(ACTIVE_CONF):
    with open(ACTIVE_CONF) as f: 
      ifce = f.read().strip()
    if confirm_disconnect(ifce):
      stop_wireguard(ifce)
  else:
    configs = list_configs()
    if not configs:
      print("No Mullvad configs found in /etc/wireguard")
    else:
      selected = select_config(configs)
      if selected:
        start_wireguard(selected)

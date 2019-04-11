import json
import sys

conv = {}
cards = {}
decklist = {}
parse_failed = 0
sane_decklist = ""
out_decklist = None
empty_lines_replaced = 0
fixed_cards = {}

with open('CONV.json', 'r') as indata:
  conv = json.load(indata)

with open('Convergence Cycle Cards.json', 'r') as indata2:
  cards = json.load(indata2)

with open(sys.argv[1]) as decklist_raw:
  try:
    decklist = json.load(decklist_raw)
    out_decklist = decklist
  except:
    decklist = open(sys.argv[1]).read()
    parse_failed = 1

# The parse failed, we have empty CardID and empty rows with only a , plus possibly one totally empty row
if parse_failed:
  decklist = decklist.replace('"CardID": ,', '"CardID": 1,')
  decklist = decklist.replace('\t,', '\t1,')

# Replaced the broken stuff, all unknown cards have id 1 now

for line in decklist.splitlines():
  ll = len(line.strip())
  if ll > 0:
    sane_decklist += line
  else:
    empty_lines_replaced = empty_lines_replaced + 1
    sane_decklist += "999"

# Replaced all empty lines with 999, we might have one card listed as 999 in the deck now

# ditch the last three 9's
out_decklist = json.loads(sane_decklist[0:-3])

# The EOF was replaced by a 999 too, subtract one
empty_lines_replaced = empty_lines_replaced - 1


#### Done fixing


def grab_object_by_name(json_object, name):
  index = 0
  for crd in json_object:
    print(crd)
    if crd['name'] == name:
      return crd, index
    index = index + 1
  return None, -1

def grab_object_by_nickname(json_object, name):
  index = 0
  for crd in json_object:
    if crd['Nickname'] == name:
      return crd, index
    index = index + 1
  return None, -1

def grab_object_by_number(json_object, nbr):
  index = 0
  for crd in json_object:
    if str(crd['position']) == nbr:
      return crd, index
    index = index + 1
  return None, -1

def grab_object_by_description(json_object, nbr):
  index = 0
  for crd in json_object:
    if str(crd['Description']) == nbr:
      return crd, index
    index = index + 1
  return None, -1

def insert_card_id(arr, idd):
  idx = 0
  for val in arr:
    if val == 1:
      arr[idx] = idd
      break
    idx += 1

## Loop over cards

index = 0
for card in out_decklist['ObjectStates'][0]['ContainedObjects']:
  elite = 0
  idx = -1
  obj = None
  if(card['Name'] == "Card" and "CONV" in card['Description']):
    if "elite" in card['Description']:
      card['Description'] = card['Description'][6:]
      elite = 1
    obj, idx = grab_object_by_description(cards['ObjectStates'][0]['ContainedObjects'], str(card['Description']))
  if(obj):
    if elite:
      obj['Description'] = "elite " + obj['Description']
    out_decklist['ObjectStates'][0]['ContainedObjects'][index] = obj
  index = index + 1

# Characters and battlefields fixed

# Fix cards in deck

outer_idx = 0
for outer in out_decklist['ObjectStates'][0]['ContainedObjects']:
  if outer['Name'] == "Deck":
    deckIDs = outer['DeckIDs']
    if deckIDs[len(deckIDs) - 1] == 999:
      deckIDs[len(deckIDs) - 1] = 1
    for card in outer['ContainedObjects']:
      if "CONV" in card['Description']:
        obj, idx = grab_object_by_description(cards['ObjectStates'][0]['ContainedObjects'], str(card['Description']))
        out_decklist['ObjectStates'][0]['ContainedObjects'][outer_idx]['CustomDeck'][idx] = obj
        insert_card_id(deckIDs, obj['CardID'])
        out_decklist['ObjectStates'][0]['ContainedObjects'][outer_idx]['DeckIDs'] = deckIDs
    #print(str(deckIDs))
    out_decklist['ObjectStates'][0]['ContainedObjects'][outer_idx]['CustomDeck'] = {}
  else:
    outer_idx += 1

with open(sys.argv[1][0:-5]+'_fixed.json', 'w') as outfile:
  json.dump(out_decklist, outfile, sort_keys = True, indent = 4, ensure_ascii = False)












#with open('fixed.json', 'w') as outfile:
#  json.dump(out_decklist, outfile, sort_keys = True, indent = 4, ensure_ascii = False)


exit(0)
#print(json.dumps(conv, indent=2, sort_keys=True))

#print(grab_name(cards['ObjectStates'], "Asajj Ventress"))
for card in cards['ObjectStates'][0]['ContainedObjects']:
  setto = None
  obj = None
  index = -1
  obj, index = grab_object_by_name(conv, card['Nickname'])
  if obj:
    #print("Found CARD ", card['Nickname'])
    #print("Would set ttsid to ", card['CardID'])
    print(index)
    setto = card['CardID']
  else:
    #print("-------------- Failed to find card ",card['Nickname'])
    obj, index = grab_object_by_number(conv, card['Description'][5:])
    if obj:
      #print("Found CARD ", card['Description'])
      #print("Would set ttsid to ", card['CardID'])
      print(index)
      setto = card['CardID']
    else:
      print("-------------- Failed to find card ",card['Nickname'])
  if setto:
    print(setto, card['Nickname'])
    print(conv[index]['name'])
    conv[index]['ttscardid'] = setto



#print(cards['ObjectStates'][0]['ContainedObjects'][0]['Nickname'])

#print(grab_object(conv, "Asajj Ventress"))
print(json.dumps(conv, indent=2, sort_keys=True))


with open('CONV_OUT.json', 'w') as outfile:
    json.dump(conv, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

#print(len(conv))
#for item in conv:
#  print("a")

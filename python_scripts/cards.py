import json

conv = {}
cards = {}

with open('CONV.json', 'r') as indata:
  conv = json.load(indata)

with open('Convergence Cycle Cards.json', 'r') as indata2:
  cards = json.load(indata2)


def grab_object_by_name(json_object, name):
  index = 0
  for crd in json_object:
    if crd['name'] == name:
      return dict, index
    index = index + 1
  return None, -1

def grab_object_by_number(json_object, nbr):
  index = 0
  for crd in json_object:
    if str(crd['position']) == nbr:
      return dict, index
    index = index + 1
  return None, -1


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

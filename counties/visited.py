from collections import Counter

visited = [
    ('Mobile',      'AL'),
    ('Montgomery',  'AL'),
    ('Jefferson',   'AL'),
    ('St. Clair',   'AL'),
    ('Talladega',   'AL'),
    ('Calhoun',     'AL'),
    ('Cleburne',    'AL'),

    ('Ketchikan Gateway', 'AK'),
    ('Juneau',      'AK'),
    ('Skagway-Hoonah-Angoon', 'AK'),
    ('Anchorage',   'AK'),
    ('Matanuska-Susitna', 'AK'),
    ('Denali',      'AK'),
    ('Fairbanks North Star', 'AK'),

    ('Apache',      'AZ'),
    ('Navajo',      'AZ'),
    ('Coconino',    'AZ'),
    ('Cochise',     'AZ'),
    ('Pima',        'AZ'),
    ('Pinal',       'AZ'),
    ('Maricopa',    'AZ'),

    ('Sebastian',   'AR'),
    ('Union',       'AR'),
    ('Garland',     'AR'),
    ('Conway',      'AR'),

    ('San Francisco', 'CA'),
    ('San Mateo',   'CA'),
    ('Santa Cruz',  'CA'),
    ('Monterey',    'CA'),
    ('San Benito',  'CA'),
    ('Santa Clara', 'CA'),

    ('Montezuma',   'CO'),
    ('La Plata',    'CO'),
    ('San Juan',    'CO'),
    ('Archuleta',   'CO'),
    ('Mineral',     'CO'),
    ('Rio Grande',  'CO'),
    ('Alamosa',     'CO'),
    ('Costilla',    'CO'),
    ('Huerfano',    'CO'),
    ('Los Animas',  'CO'),
    ('Pueblo',      'CO'),
    ('Otero',       'CO'),
    ('Bent',        'CO'),
    ('Prowers',     'CO'),
    ('Kit Carson',  'CO'),
    ('Lincoln',     'CO'),
    ('Elbert',      'CO'),
    ('Arapahoe',    'CO'),
    ('Adams',       'CO'),
    ('Denver',      'CO'),
    ('Broomfield',  'CO'),
    ('Jefferson',   'CO'),
    ('Boulder',     'CO'),

    ('District of Columbia', 'DC'),

    ('Okaloosa',    'FL'),
    ('Walton',      'FL'),
    ('Bay',         'FL'),
    ('Leon',        'FL'),
    ('Hillsborough', 'FL'),
    ('Pinellas',    'FL'),
    ('Manatee',     'FL'),
    ('Sarasota',    'FL'),
    ('Charlotte',   'FL'),
    ('Lee',         'FL'),
    ('Collier',     'FL'),
    ('Polk',        'FL'),
    ('Osceola',     'FL'),
    ('Orange',      'FL'),
    ('Brevard',     'FL'),
    ('Broward',     'FL'),
    ('Miami-Dade',  'FL'),

    ('Haralson',    'GA'),
    ('Carroll',     'GA'),
    ('Douglas',     'GA'),
    ('Cobb',        'GA'),
    ('Fulton',      'GA'),
    ('Clayton',     'GA'),

    ('St. Clair',   'IL'),
    ('Clinton',     'IL'),
    ('Marion',      'IL'),
    ('Clay',        'IL'),
    ('Richland',    'IL'),
    ('Lawrence',    'IL'),
    ('Crawford',    'IL'),
    ('Clark',       'IL'),
    ('Edgar',       'IL'),
    ('Coles',       'IL'),
    ('Douglas',     'IL'),
    ('Champaign',   'IL'),
    ('Piatt',       'IL'),
    ('De Witt',     'IL'),
    ('McLean',      'IL'),
    ('Woodford',    'IL'),
    ('Tazewell',    'IL'),
    ('Peoria',      'IL'),
    ('Knox',        'IL'),
    ('Henry',       'IL'),
    ('Rock Island', 'IL'),
    ('Madison',     'IL'),
    ('Macoupin',    'IL'),
    ('Montgomery',  'IL'),
    ('Sangamon',    'IL'),
    ('Logan',       'IL'),
    ('Livingston',  'IL'),
    ('Grundy',      'IL'),
    ('Will',        'IL'),
    ('Kendall',     'IL'),
    ('Kane',        'IL'),
    ('DeKalb',      'IL'),
    ('DuPage',      'IL'),
    ('Cook',        'IL'),
    ('Kankakee',    'IL'),
    ('Ford',        'IL'),
    ('Lake',        'IL'),

    ('Knox',        'IN'),
    ('Gibson',      'IN'),
    ('Vanderburgh', 'IN'),
    ('Daviess',     'IN'),
    ('Martin',      'IN'),
    ('Orange',      'IN'),
    ('Warrick',     'IN'),
    ('Spencer',     'IN'),

    ('Fremont',       'IA'),
    ('Mills',         'IA'),
    ('Pottawattamie', 'IA'),
    ('Harrison',      'IA'),
    ('Monona',        'IA'),
    ('Woodbury',      'IA'),
    ('Scott',         'IA'),
    ('Cedar',         'IA'),
    ('Johnson',       'IA'),
    ('Iowa',          'IA'),
    ('Poweshiek',     'IA'),
    ('Jasper',        'IA'),
    ('Polk',          'IA'),
    ('Dallas',        'IA'),
    ('Madison',       'IA'),
    ('Adair',         'IA'),
    ('Cass',          'IA'),
    ('Decatur',       'IA'),
    ('Clarke',        'IA'),
    ('Warren',        'IA'),
    ('Story',         'IA'),
    ('Hamilton',      'IA'),
    ('Wright',        'IA'),
    ('Franklin',      'IA'),
    ('Cerro Gordo',   'IA'),
    ('Worth',         'IA'),

    ('Sedgwick',   'KS'),
    ('Sumner',     'KS'),
    ('Cowley',     'KS'),
    ('Butler',     'KS'),
    ('Harper',     'KS'),
    ('Kingman',    'KS'),
    ('Reno',       'KS'),
    ('Harvey',     'KS'),
    ('Marion',     'KS'),
    ('McPherson',  'KS'),
    ('Saline',     'KS'),
    ('Riley',      'KS'),
    ('Geary',      'KS'),
    ('Dickinson',  'KS'),
    ('Lincoln',    'KS'),
    ('Ellsworth',  'KS'),
    ('Russell',    'KS'),
    ('Ellis',      'KS'),
    ('Trego',      'KS'),
    ('Gove',       'KS'),
    ('Logan',      'KS'),
    ('Thomas',     'KS'),
    ('Sherman',    'KS'),
    ('Chase',      'KS'),
    ('Lyon',       'KS'),
    ('Coffey',     'KS'),
    ('Franklin',   'KS'),
    ('Douglas',    'KS'),
    ('Miami',      'KS'),
    ('Johnson',    'KS'),
    ('Wyandotte',  'KS'),
    ('Linn',       'KS'),
    ('Bourbon',    'KS'),
    ('Crawford',   'KS'),
    ('Allen',      'KS'),
    ('Woodson',    'KS'),
    ('Wabaunsee',  'KS'),
    ('Osage',      'KS'),
    ('Shawnee',    'KS'),
    ('Jackson',    'KS'),
    ('Nemaha',     'KS'),
    ('Greenwood',  'KS'),
    ('Pratt',      'KS'),
    ('Kiowa',      'KS'),
    ('Ford',       'KS'),
    ('Gray',       'KS'),
    ('Finney',     'KS'),
    ('Kearny',     'KS'),
    ('Hamilton',   'KS'),
    ('Meade',      'KS'),
    ('Seward',     'KS'),
    ('Ottawa',     'KS'),
    ('Cloud',      'KS'),
    ('Republic',   'KS'),
    ('Rush',       'KS'),
    ('Barton',     'KS'),
    ('Pawnee',     'KS'),
    ('Stafford',   'KS'),
    ('Edwards',    'KS'),
    ('Rice',       'KS'),
    ('Chautauqua', 'KS'),
    ('Wilson',     'KS'),
    ('Montgomery', 'KS'),
    ('Marshall',   'KS'),
    ('Labette',    'KS'),
    ('Cherokee',   'KS'),

    ('Boone',       'KY'),

    ('Caddo',       'LA'),
    ('De Soto',     'LA'),
    ('Natchitoches', 'LA'),
    ('Rapides',     'LA'),
    ('Avoylles',    'LA'),
    ('Evangeline',  'LA'),
    ('St. Landry',  'LA'),
    ('Lafayette',   'LA'),
    ('St. Martin',  'LA'),
    ('Iberville',   'LA'),
    ('West Baton Rouge', 'LA'),
    ('East Baton Rouge', 'LA'),
    ('Ascension',   'LA'),
    ('St. James',   'LA'),
    ('St. John the Baptist', 'LA'),
    ('St. Charles', 'LA'),
    ('Jefferson',   'LA'),
    ('Orleans',     'LA'),
    ('Tangipahoa',  'LA'),
    ('Madison',     'LA'),
    ('Richland',    'LA'),
    ('Ouachita',    'LA'),
    ('Lincoln',     'LA'),
    ('Bienville',   'LA'),
    ('Webster',     'LA'),
    ('Bossier',     'LA'),

    ('Penobscot',   'ME'),
    ('Somerset',    'ME'),
    ('Waldo',       'ME'),
    ('Kennebec',    'ME'),
    ('Androscoggin', 'ME'),
    ('Oxford',      'ME'),
    ('Hancock',     'ME'),

    ('Montgomery',  'MD'),
    ('Frederick',   'MD'),

    ('Iron',        'MI'),
    ('Ontagonon',   'MI'),
    ('Gogebic',     'MI'),
    ('Charlevoix',  'MI'),
    ('Oakland',     'MI'),
    ('Wayne',       'MI'),

    ('St. Louis',   'MN'),
    ('Carlton',     'MN'),
    ('Pine',        'MN'),
    ('Chisago',     'MN'),
    ('Washington',  'MN'),
    ('Anoka',       'MN'),
    ('Ramsey',      'MN'),
    ('Dakota',      'MN'),
    ('Scott',       'MN'),
    ('Rice',        'MN'),
    ('Steele',      'MN'),
    ('Freeborn',    'MN'),

    ('Pike',        'MS'),
    ('Lincoln',     'MS'),
    ('Copiah',      'MS'),
    ('Hinds',       'MS'),
    ('Madison',     'MS'),
    ('Rankin',      'MS'),
    ('Warren',      'MS'),

    ('Jackson',     'MO'),
    ('Clay',        'MO'),
    ('Platte',      'MO'),
    ('Clinton',     'MO'),
    ('DeKalb',      'MO'),
    ('Daviess',     'MO'),
    ('Harrison',    'MO'),
    ('Lafayette',   'MO'),
    ('Saline',      'MO'),
    ('Cooper',      'MO'),
    ('Boone',       'MO'),
    ('Callaway',    'MO'),
    ('Montgomery',  'MO'),
    ('Warren',      'MO'),
    ('St. Charles', 'MO'),
    ('Newton',      'MO'),
    ('Jasper',      'MO'),
    ('Lawrence',    'MO'),
    ('Greene',      'MO'),
    ('Webster',     'MO'),
    ('Laclede',     'MO'),
    ('Pulaski',     'MO'),
    ('Phelps',      'MO'),
    ('Crawford',    'MO'),
    ('Franklin',    'MO'),
    ('St. Louis',   'MO'),
    ('City of St. Louis', 'MO'),
    ('Pettis',      'MO'),
    ('Vernon',      'MO'),

    ('Thayer',      'NE'),
    ('Fillmore',    'NE'),
    ('York',        'NE'),
    ('Polk',        'NE'),
    ('Butler',      'NE'),
    ('Platte',      'NE'),
    ('Madison',     'NE'),
    ('Stanton',     'NE'),
    ('Wayne',       'NE'),
    ('Dixon',       'NE'),
    ('Dakota',      'NE'),
    ('Richardson',  'NE'),
    ('Nemaha',      'NE'),
    ('Otoe',        'NE'),
    ('Seward',      'NE'),
    ('Lancaster',   'NE'),
    ('Thurston',    'NE'),
    ('Burt',        'NE'),
    ('Dodge',       'NE'),
    ('Saunders',    'NE'),
    ('Gage',        'NE'),
    ('Cedar',       'NE'),
    ('Pierce',      'NE'),
    ('Antelope',    'NE'),   

    ('Coos',        'NH'),

    ('Quay',        'NM'),
    ('Guadalupe',   'NM'),
    ('Torrance',    'NM'),
    ('Santa Fe',    'NM'),
    ('Bernalillo',  'NM'),
    ('Cibola',      'NM'),
    ('McKinley',    'NM'),
    ('Dona Ana',    'NM'),
    ('Luna',        'NM'),
    ('Grant',       'NM'),
    ('Hidalgo',     'NM'),
    ('Chaves',      'NM'),
    ('Curry',       'NM'),

    ('Monroe',      'NY'),
    ('Genesee',     'NY'),
    ('Erie',        'NY'),
    ('Niagara',     'NY'),

    ('Montgomery',  'OH'),
    ('Greene',      'OH'),
    ('Franklin',    'OH'),

    ('Kay',         'OK'),
    ('Noble',       'OK'),
    ('Payne',       'OK'),
    ('Logan',       'OK'),
    ('Oklahoma',    'OK'),
    ('Cleveland',   'OK'),
    ('McClain',     'OK'),
    ('Garvin',      'OK'),
    ('Murray',      'OK'),
    ('Carter',      'OK'),
    ('Love',        'OK'),
    ('Grady',       'OK'),
    ('Caddo',       'OK'),
    ('Comanche',    'OK'),
    ('Cotton',      'OK'),
    ('Canadian',    'OK'),
    ('Custer',      'OK'),
    ('Washita',     'OK'),
    ('Beckham',     'OK'),
    ('Roger Mills', 'OK'),
    ('Harmon',      'OK'),
    ('Greer',       'OK'),
    ('Jackson',     'OK'),
    ('Blaine',      'OK'),
    ('Kingfisher',  'OK'),
    ('Major',       'OK'),
    ('Garfield',    'OK'),
    ('Grant',       'OK'),
    ('Texas',       'OK'),
    ('Lincoln',     'OK'),
    ('Creek',       'OK'),
    ('Tulsa',       'OK'),
    ('Rogers',      'OK'),
    ('Mayes',       'OK'),
    ('Craig',       'OK'),
    ('Ottawa',      'OK'),
    ('Pawnee',      'OK'),
    ('Osage',       'OK'),
    ('Pottawatomie', 'OK'),
    ('Seminole',    'OK'),
    ('Okfuskee',    'OK'),
    ('Okmulgee',    'OK'),
    ('Pontotoc',    'OK'),
    ('Coal',        'OK'),
    ('Atoka',       'OK'),
    ('Pushmataha',  'OK'),
    ('Choctaw',     'OK'),
    ('Washington',  'OK'),
    ('Jefferson',   'OK'),

    ('Multnomah',   'OR'),
    ('Washington',  'OR'),
    ('Yamhill',     'OR'),
    ('Columbia',    'OR'),
    ('Clatsop',     'OR'),

    ('Union',       'SD'),
    ('Lincoln',     'SD'),
    ('Minnehaha',   'SD'),

    ('Cooke',       'TX'),
    ('Denton',      'TX'),
    ('Collin',      'TX'),
    ('Dallas',      'TX'),
    ('Tarrant',     'TX'),
    ('Johnson',     'TX'),
    ('Hill',        'TX'),
    ('McLennan',    'TX'),
    ('Falls',       'TX'),
    ('Bell',        'TX'),
    ('Williamson',  'TX'),
    ('Travis',      'TX'),
    ('Hays',        'TX'),
    ('Comal',       'TX'),
    ('Guadalupe',   'TX'),
    ('Bexar',       'TX'),
    ('Ellis',       'TX'),
    ('Navarro',     'TX'),
    ('Freestone',   'TX'),
    ('Leon',        'TX'),
    ('Madison',     'TX'),
    ('Walker',      'TX'),
    ('Montgomery',  'TX'),
    ('Harris',      'TX'),
    ('Fort Bend',   'TX'),
    ('Waller',      'TX'),
    ('Grimes',      'TX'),
    ('Brazos',      'TX'),
    ('Parker',      'TX'),
    ('Palo Pinto',  'TX'),
    ('Erath',       'TX'),
    ('Eastland',    'TX'),
    ('Callahan',    'TX'),
    ('Taylor',      'TX'),
    ('Nolan',       'TX'),
    ('Mitchell',    'TX'),
    ('Howard',      'TX'),
    ('Martin',      'TX'),
    ('Midland',     'TX'),
    ('Ector',       'TX'),
    ('Crane',       'TX'),
    ('Ward',        'TX'),
    ('Reeves',      'TX'),
    ('Jeff Davis',  'TX'),
    ('Culberson',   'TX'),
    ('Hudspeth',    'TX'),
    ('El Paso',     'TX'),
    ('Sherman',     'TX'),
    ('Dallam',      'TX'),
    ('Hartley',     'TX'),
    ('Wheeler',     'TX'),
    ('Hemphill',    'TX'),
    ('Collingsworth', 'TX'),
    ('Childress',   'TX'),
    ('Wilbarger',   'TX'),
    ('Wichita',     'TX'),
    ('Archer',      'TX'),
    ('Montague',    'TX'),
    ('Wise',        'TX'),
    ('Lamar',       'TX'),
    ('Red River',   'TX'),
    ('Franklin',    'TX'),
    ('Titus',       'TX'),
    ('Morris',      'TX'),
    ('Cass',        'TX'),
    ('Marion',      'TX'),
    ('Harrison',    'TX'),
    ('Gregg',       'TX'),
    ('Smith',       'TX'),
    ('Wood',        'TX'),
    ('Rains',       'TX'),
    ('Hunt',        'TX'),

    ('San Juan',    'UT'),
    ('Grand',       'UT'),

    ('Loudoun',     'VA'),
    ('Fairfax',     'VA'),
    ('Arlington',   'VA'),

    ('Pacific',     'WA'),
    ('Wahkiakum',   'WA'),
    ('Cowlitz',     'WA'),
    ('Clark',       'WA'),
    ('Skamania',    'WA'),

    ('Kenosha',     'WI'),
    ('Racine',      'WI'),
    ('Milwaukee',   'WI'),
    ('Ozaukee',     'WI'),
    ('Sheboygan',   'WI'),
    ('Manitowoc',   'WI'),
    ('Brown',       'WI'),
    ('Oconto',      'WI'),
    ('Marinette',   'WI'),
    ('Florence',    'WI'),
    ('Iron',        'WI'),
    ('Ashland',     'WI'),
    ('Bayfield',    'WI'),
    ('Douglas',     'WI'),
    ('Winnebago',   'WI'),
    ('Green Lake',  'WI'),
    ('Fond du Lac', 'WI'),
    ('Columbia',    'WI'),
]

print "Number of counties:", len(visited)
by_state = {}
by_name = {}

for v in visited:
    try:
        by_state[v[1]] += 1
    except KeyError:
        by_state[v[1]] = 1

    try:
        by_name[v[0]].append(v[1])
    except KeyError:
        by_name[v[0]] = [ v[1] ]

print "Number of states:", len(by_state.keys())

for state, count in sorted(by_state.items(), key=lambda x: x[1], reverse=True):
    print "%s: %d" % (state, count)

for name, states in sorted(by_name.items(), key=lambda x: len(x[1]), reverse=True):
    if len(states) > 1:
        print "%s: %d (%s)" % (name, len(states), ", ".join(states))

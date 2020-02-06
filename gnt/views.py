from django.shortcuts import render


def home(request):
    return render(request, 'gnt/index.html')


def results(request):
    # TODO: Replace hard coded drinks with information passed into request
    drinks = [
        {
            'id': 'ankeoigab4a34q35htrgif847qyrahd',
            'picture': 'https://assets.bonappetit.com/photos/57acc14e53e63daf11a4d9b6/master/pass/whiskey-sour.jpg',
            'name': 'Whiskey Sour',
                    'ingredients': ['1 ½ oz oz Whiskey',
                                    '2 oz Sour Mix (Fresh preferred)',
                                    'Optional: 1/2 oz egg white (makes drink foamy)'
                                    ],
                    'method': ['glass: Highball',
                               'Shake Ingredients in a Mixing Glass or Cocktail Shaker w/ice',
                               'Strain into a large old fashioned glass with fresh ice',
                               'Garnish with cherry & orange'
                               ]

        },
        {
            'id': '394agdnavior;oa4eih',
            'picture': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS9h-WqGmZDxZTkvjEqRWyDG0ZIw5wC6RlQyFj_THX8fmYcQEgv',
            'name': 'Old Fashioned',
                    'ingredients': ['Packet of Sugar',
                                    '2 dashes of Bitters',
                                    'Splash of soda',
                                    'Cherry & orange',
                                    '2 oz Whiskey'
                                    ],
                    'method': [	'glass: Rocks glass',
                                'Muddle sugar, bitters, soda in glass',
                                'Add Whiskey',
                                'Fill glass with ice'
                                ]
        }
    ]
    context = {
        'drinks': drinks
    }
    return render(request, 'gnt/results.html', context)


def loading(request):
    return render(request, 'gnt/loading.html')

# seat-planner
# seat-planner
dummy htmls are in api/templates for reference

for pref:     
  GET method     
    'Name': a str name     
    ‘Window’: Prefer window or aisle         # Window = 1, Indifferent = 0, Aisle = -1     
    ‘Sleep’: Sleep, rest (need quiet)        # Sleep Very Much = 2 <-----> Sleep Very Less = -2     
    ‘Networking’: willing to networking       # Very Willing = 2 <-----> Very Unwilling = -2     
    ‘WindowShading’:           # Very Willing to Open = 2 <----> Very Unwilling to Open = -2     


        
        
The format of feedback parameters do not matter as we use generated feedback for the learning models for now.


result:
  result does not take any parameters, but it returns the following json:
  https://drive.google.com/open?id=1Vp4wbqSs2aSUnDDWGZaAOSZjCTVXpBTH
  [
        {
            'Name': name_to_highlight,
            'Preferences':{
                'Window':(some value),
                'Sleep':(some value),
                'Networking':(some value),
                'WindowShading':(some value),
            },
            'Color': {
                'R':(some value from 0 to 255),
                'G':(some value from 0 to 255),
                'B':(some value from 0 to 255),
            }
        },
        {
            'Name': highlight_neighbor,
            'Preferences':{
                'Window':(some value),
                'Sleep':(some value),
                'Networking':(some value),
                'WindowShading':(some value),
            },
            'Color': {
                'R':(some value from 0 to 255),
                'G':(some value from 0 to 255),
                'B':(some value from 0 to 255),
            }
        }
    ]

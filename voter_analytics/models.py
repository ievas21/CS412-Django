from django.db import models

# Ieva sagaitis, ievas@bu.edu

class Voter(models.Model):
    '''
    Store/represent the data from one voter in Newton, MA.
    Voter ID Number,Last Name,First Name,Residential Address - Street Number,Residential Address - Street Name,R
    esidential Address - Apartment Number,Residential Address - Zip Code,Date of Birth,Date of Registration,Party Affiliation,
    Precinct Number,v20state,v21town,v21primary,v22general,v23town,voter_score
    '''

    voter_id = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True, null=True) 
    zip_code = models.TextField() #
    dob = models.DateField()
    registration_date = models.DateField()
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'

def load_data():
    '''Load the data records from a CSV file, and create Django model instances.'''

     # delete all records
    Voter.objects.all().delete()

    filename = "C:\\Users\\ievas\\OneDrive\\Desktop\\CS412\\newton_voters.csv"
    f = open(filename)
    headers = f.readline().strip().split(',')

    for line in f:
        try:
            fields = line.strip().split(',')
            result = Voter(voter_id=fields[0],
                                last_name=fields[1],
                                first_name=fields[2],
                                street_number=fields[3],
                                street_name=fields[4],
                                apartment_number=fields[5] if fields[5] else None,

                                zip_code=fields[6],
                                dob=fields[7],
                                registration_date=fields[8],
                                party_affiliation=fields[9].strip(),
                                precinct_number=fields[10],

                                v20state=fields[11] == 'TRUE',
                                v21town=fields[12] == 'TRUE',
                                v21primary=fields[13] == 'TRUE',
                                v22general=fields[14] == 'TRUE',
                                v23town=fields[15] == 'TRUE',
                                voter_score=fields[16],
                                )
            result.save()
            print(f'Created result: {result}')
        except:
            print(f'Exception Occured: {fields}.')

    print("Done.")

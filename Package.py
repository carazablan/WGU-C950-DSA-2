class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline, weight):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = 'At HUB'
        self.loading_time = None
        self.delivery_time = None

    def __str__(self):
        # return str((self.ID))
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode,
                                                       self.deadline, self.weight, self.status, self.delivery_time)

    def __repr__(self):
        # return str((self.ID))
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode,
                                                       self.deadline, self.weight, self.status, self.delivery_time)

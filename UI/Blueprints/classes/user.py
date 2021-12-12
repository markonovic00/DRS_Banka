class User:
    id=-1
    first_name = ""
    last_name = ""
    address=""
    city=""
    country=""
    phone_number=""
    email=""
    password=""

    def __init__(self,id,first_name,last_name,address,city,country,phone_number,email,password):
        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.address=address
        self.city=city
        self.country=country
        self.phone_number=phone_number
        self.email=email
        self.password=password

    #def myfunc(self):                # Mogucnost definisanja dodatnih funckija radi ispisa
    #    return self.first_name

from user.constants import GeoChoise

# Random test user's data  👇
DEVELOPMENT_USER_PLAYER_LIST = [
    # Club Admin 👇
    {
        "user": {
            "email": "club_admin@mail.com",
            "password": "123njkQ6**N1q",
            "first_name": "Ivan",
            "second_name": "Pizdalov",
            "birth_date": "1994-05-26",
            "sex": 1,
            "geo": GeoChoise[0][0],
        },
        "player": {
            "playing_hand": 1,
            "blade": "mazda rx 6",
            "rubber_forehand": "lada niva",
            "rubber_backhand": "toyota land arbuzer",
            "rating": 10
        }
    },
    # 10 players 👇
    {
        "user": {
            "email": "user1@example.com",
            "password": "Password1**A1",
            "first_name": "Alex",
            "second_name": "Smith",
            "birth_date": "1990-02-15",
            "sex": 1,
            "geo": GeoChoise[2][0],
        },
        "player": {
            "playing_hand": 2,
            "blade": "honda civic",
            "rubber_forehand": "bmw x5",
            "rubber_backhand": "audi a6",
            "rating": 100
        }
    },
    {
        "user": {
            "email": "user2@example.com",
            "password": "Password2**B2",
            "first_name": "Emma",
            "second_name": "Johnson",
            "birth_date": "1988-11-21",
            "sex": 0,
            "geo": GeoChoise[1][0],
        },
        "player": {
            "playing_hand": 1,
            "blade": "tesla model s",
            "rubber_forehand": "mercedes g-class",
            "rubber_backhand": "ford mustang",
            "rating": 50
        }
    },
    {
        "user": {
            "email": "user3@example.com",
            "password": "Password3**C3",
            "first_name": "Michael",
            "second_name": "Williams",
            "birth_date": "1992-06-30",
            "sex": 1,
            "geo": GeoChoise[3][0],
        },
        "player": {
            "playing_hand": 2,
            "blade": "chevrolet camaro",
            "rubber_forehand": "nissan gtr",
            "rubber_backhand": "subaru impreza",
            "rating": 73
        }
    },
    {
        "user": {
            "email": "user4@example.com",
            "password": "Password4**D4",
            "first_name": "Olivia",
            "second_name": "Brown",
            "birth_date": "1995-09-10",
            "sex": 0,
            "geo": GeoChoise[0][0],
        },
        "player": {
            "playing_hand": 1,
            "blade": "jaguar f-type",
            "rubber_forehand": "porsche 911",
            "rubber_backhand": "land rover defender",
            "rating": 69
        }
    },
    {
        "user": {
            "email": "user5@example.com",
            "password": "Password5**E5",
            "first_name": "Daniel",
            "second_name": "Jones",
            "birth_date": "1985-04-19",
            "sex": 1,
            "geo": GeoChoise[2][0],
        },
        "player": {
            "playing_hand": 2,
            "blade": "lexus lx 570",
            "rubber_forehand": "acura nsx",
            "rubber_backhand": "infiniti qx80",
            "rating": 69
        }
    },
    {
        "user": {
            "email": "user6@example.com",
            "password": "Password6**F6",
            "first_name": "Sophia",
            "second_name": "Garcia",
            "birth_date": "1993-07-25",
            "sex": 0,
            "geo": GeoChoise[3][0],
        },
        "player": {
            "playing_hand": 1,
            "blade": "volkswagen golf",
            "rubber_forehand": "kia stinger",
            "rubber_backhand": "hyundai genesis",
            "rating": 69
        }
    },
    {
        "user": {
            "email": "user7@example.com",
            "password": "Password7**G7",
            "first_name": "David",
            "second_name": "Martinez",
            "birth_date": "1991-12-14",
            "sex": 1,
            "geo": GeoChoise[3][0],
        },
        "player": {
            "playing_hand": 2,
            "blade": "mini cooper",
            "rubber_forehand": "peugeot 208",
            "rubber_backhand": "renault clio",
            "rating": 1
        }
    },
    {
        "user": {
            "email": "user8@example.com",
            "password": "Password8**H8",
            "first_name": "Ava",
            "second_name": "Davis",
            "birth_date": "1989-03-07",
            "sex": 0,
            "geo": GeoChoise[3][0],
        },
        "player": {
            "playing_hand": 1,
            "blade": "fiat 500",
            "rubber_forehand": "alfa romeo giulia",
            "rubber_backhand": "maserati ghibli",
            "rating": 69
        }
    },
    {
        "user": {
            "email": "user9@example.com",
            "password": "Password9**I9",
            "first_name": "James",
            "second_name": "Rodriguez",
            "birth_date": "1994-08-22",
            "sex": 1,
            "geo": GeoChoise[3][0],
        },
        "player": {
            "playing_hand": 2,
            "blade": "citroen c3",
            "rubber_forehand": "seat leon",
            "rubber_backhand": "skoda superb",
            "rating": 69
        }
    },
    {
        "user": {
            "email": "user10@example.com",
            "password": "Password10**J10",
            "first_name": "Isabella",
            "second_name": "Lopez",
            "birth_date": "1996-01-05",
            "sex": 0,
            "geo": GeoChoise[3][0],
        },
        "player": {
            "playing_hand": 1,
            "blade": "volvo xc90",
            "rubber_forehand": "saab 9-5",
            "rubber_backhand": "opel insignia",
            "rating": 1488
        }
    }
]


DEVELOPMENT_CLUB = {
    "name": "PussyGayClub",
    "state": "Russia",
    "city": "Saint-AbuDabi",
    "address": "Chkalova 37",
    "phone_number": "+79992370953",
    "about": "We love Penis! We hate Tennis!",
    "social_link": "https://instagram.com/table_pennis",
    "link": "https://welovechildrens.com/",
    "opening_hours": {
        "MONDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "TUESDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "WEDNESDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "THURSDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "FRIDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "SATURDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "SUNDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        }
    }
}

DEVELOPMENT_TOURNAMENT = {
    "name": "Men Fusk Mens - it's real sport!",
    "date_time": "2024-07-03T22:14:00+04:00",
    "club": 1
}
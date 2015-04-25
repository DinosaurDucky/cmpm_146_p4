import random

# EXAMPLE STATE MACHINE
class MantisBrain:
    def __init__(self, body):
        self.body = body
        self.state = 'idle'
        self.target = None

    def handle_event(self, message, details):

        if self.state is 'idle':

            if message == 'timer':
                # go to a random point, wake up sometime in the next 10 seconds
                world = self.body.world
                x, y = random.random() * world.width, random.random() * world.height
                self.body.go_to((x, y))
                self.body.set_alarm(random.random() * 10)

            elif message == 'collide' and details['what'] == 'Slug':
                # a slug bumped into us; get curious
                self.state = 'curious'
                self.body.set_alarm(1)  # think about this for a sec
                self.body.stop()
                self.target = details['who']

        elif self.state == 'curious':

            if message == 'timer':
                # chase down that slug who bumped into us
                if self.target:
                    if random.random() < 0.5:
                        self.body.stop()
                        self.state = 'idle'
                    else:
                        self.body.follow(self.target)
                        self.body.set_alarm(1)
            elif message == 'collide' and details['what'] == 'Slug':
                # we meet again!
                slug = details['who']
                slug.amount -= 0.01  # take a tiny little bite


class SlugBrain:
    def __init__(self, body):
        self.body = body
        self.state = 'idle'
        self.has_resource = False
        self.target = None

    def handle_event(self, message, details):
        # TODO: IMPLEMENT THIS METHOD
        # (Use helper methods and classes to keep your code organized where
        #  approprioate.)
        if message is 'order':
            if len(details) > 1:
                self.body.go_to(details)

            elif details is 'a':
                self.state = 'attack'
                self.body.follow(self.body.find_nearest('Mantis'))
                self.target = self.body.find_nearest('Mantis')
                print "i should attack!"

            elif details is 'i':
                self.state = 'idle'
                self.body.stop()
                print "i should idle!"

            elif details is 'h':
                self.state = 'harvest'
                print "i should harvest!"

            elif details is 'b':
                self.state = 'build'
                self.body.go_to(self.body.find_nearest('Nest'))
                print "i should build!"

            else:
                print "i don't know the order {", details, "}."

        if self.body.amount < 0.5 or self.state == 'flee':
            self.state = 'flee'
            self.body.go_to(self.body.find_nearest('Nest'))
            if message == 'collide' and details['what'] == 'Nest':
                self.body.amount += 0.10

        if self.state == 'attack':
            self.target = self.body.find_nearest('Mantis')
            if message == 'timer':
                self.body.follow(self.target)
                self.body.set_alarm(1)
            elif message == 'collide' and details['what'] == 'Mantis':
                # we meet again!
                mantis = details['who']
                self.body.set_alarm(1)
                mantis.amount -= 0.05  # take a tiny little bite

        if self.state == 'build':
            if message == 'collide' and details['what'] == 'Nest':
                nest = details['who']
                nest.amount += 0.01

        if self.state == 'harvest':
            if self.has_resource == False:
                self.body.go_to(self.body.find_nearest('Resource'))
            if self.has_resource == True:
                self.body.go_to(self.body.find_nearest('Nest'))
            if message == 'collide' and details['what'] == 'Nest' and self.has_resource == True:
                self.has_resource = False
            if message == 'collide' and details['what'] == 'Resource' and self.has_resource == False:
                self.has_resource = True
                resource = details['who']
                resource.amount -= 0.25


world_specification = {
    'worldgen_seed': 13,  # comment-out to randomize
    'nests': 2,
    'obstacles': 2,
    'resources': 5,
    'slugs': 5,
    'mantises': 10,
}

brain_classes = {
    'mantis': MantisBrain,
    'slug': SlugBrain,
}
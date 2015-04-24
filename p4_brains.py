
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
         x, y = random.random()*world.width, random.random()*world.height
         self.body.go_to((x,y))
         self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
         # a slug bumped into us; get curious
         self.state = 'curious'
         self.body.set_alarm(1) # think about this for a sec
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
         slug.amount -= 0.01 # take a tiny little bite
               
class SlugBrain:

   def __init__(self, body):
      self.body = body
      self.state = 'idle'
      self.has_resource = False
      self.target = None

   def handle_event(self, message, details):
      # TODO: IMPLEMENT THIS METHOD
      #  (Use helper methods and classes to keep your code organized where
      #  approprioate.)
      if message is 'order':
         if len(details) > 1:
            self.body.go_to(details)

         elif details is 'a':
            print "i should attack!"

         elif details is 'i':
            print "i should idle!"

         elif details is 'h':
            print "is hould harvest!"

         elif details is 'b':
            print "i should build!"

         else:
            print "i don't know the order {", details, "}."
      pass    

world_specification = {
   'worldgen_seed': 13, # comment-out to randomize
   'nests': 2,
   'obstacles': 25,
   'resources': 5,
   'slugs': 5,
   'mantises': 5,
}

brain_classes = {
   'mantis': MantisBrain,
   'slug': SlugBrain,
}

# To Do List #    
* Maybe boxes can be pushed onto SunkenMetalBoxes? Or not? Whichever would be more useful for level design.
* Make all objects subclass of BasicObjectType - save like 20-30 lines
```python3 
class basicObject:
  instances = []
  def __init__(self, xy):
    self.x = xy[0]
    self.y = xy[1]
    self.__class__.instances.append(self)
  def place(self):
    grid[self.y][self.x] = self
```
* Make it easier to change the global grid size per level
* Add window transitions (scary thought, I know)
* Add laser going through portals
* Add death animations
* add switch-activated portals
* add pushable lasers
* superclass all, to elim all class instances at end of level